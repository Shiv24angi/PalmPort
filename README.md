# 🖐️PalmPort

Teleport files from your laptop to your phone **using just hand gestures** ✊👉📲.  
Close your fist in front of the webcam, and the currently open file will be “teleported” over Wi-Fi to your phone.  

No extra apps are needed on your phone — just open the link in your browser.

---

## ✨ Features
- ✊ Close your fist → active app closes, and its file is sent to your phone  
- 📲 Phone instantly downloads the file via Wi-Fi (no cables, no app install)  
- 🤚 Optional reopen of the file on your PC after sending (configurable)  
- 🛡️ Smart detection avoids temp/cache files (`.db`, `.tmp`)  
- 📂 Fallback file picker if auto-detection fails  
- 🌐 Works on local Wi-Fi, phone only needs a browser  

---

## 📂 Project Structure
```

GestureTeleport/
│── sender.py              # Main script (gesture + file transfer)
│── config.py              # Host/port configuration
│── haarcascades/
│   └── fist.xml           # Haar cascade for fist detection
│── requirements.txt       # Python dependencies
│── README.md              # This file

````

---

## ⚙️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/GestureTeleport.git
   cd GestureTeleport
````

2. Install dependencies (Python 3.9+ recommended):

   ```bash
   pip install -r requirements.txt
   ```

   If `mediapipe` doesn’t install, downgrade Python (e.g., 3.10 or 3.9).

---

## ▶️ Usage

1. Start the sender:

   ```bash
   python sender.py
   ```

2. You’ll see something like:

   ```
   🌐 Open on phone: http://192.168.1.34:8000
   ```

3. Open that link in your phone’s browser (make sure both devices are on same Wi-Fi).

4. Open any file (Word, PDF, Image, Notepad, etc.) on your laptop.

5. ✊ Close your fist → the file closes on laptop and downloads on your phone.

---

## 🛠️ Requirements

* Windows laptop (tested)
* Python 3.9–3.10 (newer Python may break `mediapipe`)
* Webcam (built-in or USB)
* Phone with a browser (Chrome/Safari/Edge/Firefox)
* Wi-Fi network (both devices must be on same network)

---

## ⚠️ Notes

* File detection isn’t perfect: some apps (like Word) hide file paths in caches.
  → If auto-detection fails, you’ll be prompted to pick the file manually.
* Currently optimized for **Windows**. Linux/Mac may need tweaks for process detection.

---

## 🔮 Future Ideas

* 📡 Add **Bluetooth** or **Wi-Fi Direct** support (no network needed)
* 🖼️ Add **hand-pose tracking with MediaPipe** for more gestures (like two-hand swipe = multi-file transfer)
* 🔐 Add optional encryption when sending over Wi-Fi
* 🪄 Real “teleport effect” animation on both devices

---



