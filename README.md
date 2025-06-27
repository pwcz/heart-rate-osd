
# ❤️ Heart Rate OSD 

This script overlays **heart rate data** from a `.fit` file onto a video by adding on-screen display (OSD) information to each frame.

The resulting video will include a heart rate indicator rendered in the top-right corner.

![Sample OSD](images/sample_osd.jpg)

---

## 🎬 What It Does

- Parses a `.fit` file containing heart rate telemetry (e.g. from a Garmin device).
- Reads the input video file frame by frame.
- Draws heart rate OSD info using platform-specific fonts.
- Writes a new video file (`heart_rate_osd.MOV`) with the OSD.

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

You will also need:

- A `.MOV` video file placed in the `data/` directory.
- A corresponding `.fit` heart rate file in the same folder.

> **Note:** The script expects exactly **one `.MOV`** and **one `.fit`** file in the `data/` folder.

---

## 🚀 Usage

### ▶️ Generate video with OSD:

```bash
python heart_rate_osd.py
```

The result will be saved as `heart_rate_osd.MOV`.

### 👁️ Preview a single frame:

To preview OSD rendering before generating the full video:

```bash
python heart_rate_osd.py --preview
```

It will display the first frame with a sample heart rate and save it as `test_frame.png`.

---

## 📜 License

MIT License — feel free to use and adapt.


## 🧪 Environment Setup

### 1. Install Python requirements:

Make sure you have Python 3.8+ installed. Then install dependencies with:

```bash
pip install -r requirements.txt
```

### 2. Folder setup:

Place your files like this:

```
project/
├── heart_rate_osd.py
├── fit_reader.py
├── requirements.txt
├── data/
│   ├── your_video.MOV     # From your phone (e.g., iPhone)
│   └── your_data.fit      # From Garmin watch
```

> The script expects **one** `.MOV` file and **one** `.fit` file in the `data/` directory.

---

## ▶️ Run the script

### Generate full video with OSD:

```bash
python heart_rate_osd.py
```

### Preview just one frame:

```bash
python heart_rate_osd.py --preview
```

