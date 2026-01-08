# Watermark Studio

**Watermark Studio** is a professional-grade branding toolkit available as both a **High-Performance Desktop Application** and an **Instant Web Studio**. Designed for creators, it provides a sleek dark-themed interface to brand images with precision text or logos.

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

---

## 🚀 Deployment Options

### 1. 🌐 Web Studio (Online)
Brand your images instantly in your browser without any installation.
* **Live App:** [Launch Watermark Studio Online](https://share.streamlit.io/)

### 2. 💻 Desktop Edition (Windows)
Native Windows application for high-performance offline processing.
* **Download:** [Get the Latest Installer (.exe)](https://github.com/muthu17ks/Watermark-Studio/releases)
* **Best for:** Professional local use and privacy.

---

## ✨ Features

* **Dual Modes:** Seamlessly switch between **Text Mode** and **Logo Mode**.
* **No-Scroll Workspace:** An optimized 100vh canvas ensures your image and controls are always perfectly framed.
* **Precision Control UI:**
    * **Arrow-Adjust Sliders:** Fine-tune Size and Opacity pixel-by-pixel with `◀` and `▶` buttons.
    * **Smart Positioning:** Quickly snap watermarks to corners or the center.
* **Dynamic Sizing:** Watermark scale is intelligently calculated relative to image height for consistent branding.
* **Instant Export:** High-resolution JPEG saving directly to your computer.

---

## 🛠️ Installation

### Prerequisites
* Python 3.8 or higher
* Pillow (Python Imaging Library)

### Setup Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/muthu17ks/Watermark-Studio.git
    cd Watermark-Studio
    ```

2.  **Run the Desktop App (Tkinter):**
    ```bash
    pip install Pillow
    python desktop/main.py
    ```

3.  **Run the Web App (Streamlit):**
    ```bash
    pip install streamlit Pillow
    streamlit run web/watermarker_studio.py
    ```

---

## 🚀 Usage

1.  Click **📂 Open Image** to load your base photo.
2.  Choose your **Watermark Type** (Text or Logo).
3.  Use the **Smart Sliders** (or arrow buttons) to adjust Size and Opacity.
4.  Select a **Position** (e.g., Bottom Right).
5.  Click **💾 Save Result** (Desktop) or **EXPORT** (Web) to save your branded image.

---

## 📦 Technologies Used

* **Language:** [Python](https://www.python.org/)
* **Web UI:** [Streamlit](https://streamlit.io/)
* **GUI Framework:** [Tkinter](https://docs.python.org/3/library/tkinter.html)
* **Image Processing:** [Pillow (PIL)](https://pillow.readthedocs.io/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Created by Muthukumaran*