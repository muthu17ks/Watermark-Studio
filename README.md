# 🌊 Watermark Studio

**Watermark Studio** is a sleek, professional-grade desktop application designed to streamline the process of branding your images. Built with **Python** and **Tkinter**, it offers a modern dark-themed UI, real-time high-DPI previews, and robust controls for both text and logo watermarking.

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

## ✨ Features

* **Dual Modes:** Seamlessly switch between **Text Mode** (with custom colors) and **Logo Mode** (supports PNG/JPG).
* **Real-Time Preview:** See changes instantly as you type or adjust sliders.
* **Smart Positioning:** Quickly snap watermarks to corners or the center.
* **Precision Control:**
    * **Size Scale:** Adjustable from 1% to 100% relative to the image size.
    * **Opacity:** Full transparency control (0-100%).
    * **Fine-Tune Buttons:** "Plus" and "Minus" buttons for pixel-perfect adjustments.
* **Format Support:** Automatically handles JPEG (non-transparent) and PNG (transparent) outputs.
* **Modern UI:** A clean, dark-themed interface optimized for Windows High DPI displays.

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

2.  **Install dependencies:**
    ```bash
    pip install Pillow
    ```

3.  **Run the application:**
    ```bash
    python main.py
    ```

## 🚀 Usage

1.  Click **📂 Open Image** to load your base photo.
2.  Choose your **Watermark Type** (Text or Logo).
    * *Text Mode:* Type your text and pick a color.
    * *Logo Mode:* Upload a transparent PNG logo.
3.  Use the **Smart Sliders** to adjust Size and Opacity.
4.  Select a **Position** (e.g., Bottom Right).
5.  Click **💾 Save Result** to export your branded image. The app automatically suggests a filename like `original_name_watermarked.png`.

## 📦 Technologies Used

* **Language:** [Python](https://www.python.org/)
* **GUI Framework:** [Tkinter](https://docs.python.org/3/library/tkinter.html) (Standard Python GUI)
* **Image Processing:** [Pillow (PIL)](https://pillow.readthedocs.io/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Created by Muthukumaran*