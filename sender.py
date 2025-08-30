import cv2, os, time, socket, threading, psutil
import win32gui, win32process
from flask import Flask, send_file, Response, render_template_string
import tkinter as tk
from tkinter import filedialog
from config import HOST, PORT

# Haar cascades
fist_cascade = cv2.CascadeClassifier("haarcascades/fist.xml")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
last_action = None
cooldown = 3
last_time = time.time()
event_triggered = False
file_to_send = None

# Flask app
app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>Teleport Receiver</title>
  <script>
    function connectSSE() {
      const evtSource = new EventSource("/events");
      evtSource.onmessage = function(event) {
        if (event.data === "teleport") {
          window.location.href = "/download";
        }
      };
    }
    window.onload = connectSSE;
  </script>
</head>
<body>
  <h2>📲 Waiting for teleport...</h2>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/download")
def download():
    global file_to_send
    if file_to_send and os.path.exists(file_to_send):
        filename = os.path.basename(file_to_send)
        return send_file(
            file_to_send,
            as_attachment=True,
            download_name=filename
        )
    return "❌ No file detected to send", 500

@app.route("/events")
def events():
    def stream():
        global event_triggered
        while True:
            if event_triggered:
                yield "data: teleport\n\n"
                event_triggered = False
            time.sleep(0.5)
    return Response(stream(), mimetype="text/event-stream")


# -------------------------
# Helpers for file detection
# -------------------------
def search_file_in_common_dirs(filename):
    """Search for a file in common user folders"""
    common_dirs = [
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Pictures"),
    ]
    for d in common_dirs:
        for root, _, files in os.walk(d):
            if filename in files:
                return os.path.join(root, filename)
    return None

def ask_user_for_file():
    """Open a file picker dialog as last resort"""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select the file to teleport")
    return file_path if file_path else None

def get_active_file():
    """Return (process_name, file_path) for active window if possible"""
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return None, None

    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    try:
        proc = psutil.Process(pid)
        app = proc.name()
        title = win32gui.GetWindowText(hwnd)

        filepath = None

        # 1. Try open_files()
        try:
            for f in proc.open_files():
                if f.path and os.path.exists(f.path):
                    if f.path.lower().endswith((".docx", ".txt", ".pdf", ".png", ".jpg", ".jpeg")):
                        filepath = f.path
                        break
        except Exception:
            pass

        # 2. Parse window title (e.g., "Report.docx - Word")
        if not filepath and "-" in title:
            candidate = title.split("-")[0].strip()
            if "." in candidate:  # looks like a filename
                found = search_file_in_common_dirs(candidate)
                if found:
                    filepath = found

        # 3. Manual file picker if still not found
        if not filepath:
            print("⚠️ Could not auto-detect file, please select it manually.")
            filepath = ask_user_for_file()

        return app, filepath
    except Exception:
        return None, None


def close_app(app):
    os.system(f"taskkill /im {app} /f")


# Start Flask server
def run_server():
    app.run(host=HOST, port=PORT, debug=False, use_reloader=False)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

threading.Thread(target=run_server, daemon=True).start()
server_ip = get_ip()
print(f"🌐 Open on phone: http://{server_ip}:{PORT}")


# -------------------------
# Main loop
# -------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fists = fist_cascade.detectMultiScale(gray, 1.3, 5)

    now = time.time()
    if len(fists) > 0 and (now - last_time > cooldown):
        if last_action != "fist":
            app_name, filepath = get_active_file()
            print("Active app:", app_name, "file:", filepath)
            if app_name:
                close_app(app_name)
                print(f"✊ Closed {app_name}")
            if filepath:
                file_to_send = filepath
                print(f"📤 Teleporting file {filepath}")
                event_triggered = True
            else:
                print("⚠️ No file path detected, only app closed")
            last_action = "fist"
            last_time = now

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
