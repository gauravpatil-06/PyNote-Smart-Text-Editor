# 🚀 PyNote — Smart Text Editor: Built for Speed & Precision

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python%203.x-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/GUI-Tkinter%20%7C%20Ttk-green?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Aesthetics-Dark%20Mode%20%7C%20HCI-orange?style=for-the-badge&logo=visual-studio-code"/>
  <img src="https://img.shields.io/badge/Design-Notepad%2B%2B%20Style-38B2AC?style=for-the-badge&logo=codeforces"/>
</p>

---

## 🌟 Introduction

While building **PyNote**, my goal was to create a lightweight yet powerful alternative to heavy IDEs. I wanted a text editor that feels as familiar as Notepad++ but benefits from the modularity and speed of a modern Python architecture.

PyNote isn't just a simple text box; it's a refined ecosystem designed using **Human-Computer Interaction (HCI)** principles. Whether you're a student writing your first script or a developer needing a quick, distraction-free environment, PyNote is built to provide maximum visibility and control.

---

## 🚀 How It Works: The Flow

1.  **Instant Launch**: A maximized, clean workspace opens immediately, ready for input.
2.  **Multi-Tab Mastery**: Open multiple files simultaneously using the professional tabbed interface. Standard shortcut `Ctrl+N` for new tabs.
3.  **Smart Editing**: Benefit from real-time syntax highlighting, line numbering, and a dedicated status bar showing line/column position.
4.  **Effortless Management**: Use the integrated **Autosave** engine and session persistence to ensure you never lose a single keystroke.
5.  **Security Integration**: Need a quick checksum? Compute **MD5** or **SHA-256** hashes directly within the "Tools" menu.

---

## 🔥 Why PyNote? (Core Features)

| Feature | Description |
| :--- | :--- |
| **🎨 Professional UI** | A Notepad++ inspired interface with support for a sleek **Dark Mode** to reduce eye strain. |
| **📑 Advanced Tab System** | Manage multiple files with a high-precision tab manager, including 'x' icons and modification markers. |
| **⚡ Real-time Analytics** | A dynamic status bar tracking Line, Column, Character Position, and Word Count. |
| **🔍 Precision Search** | Integrated Find & Replace tool to navigate and modify large files instantly. |
| **🛡️ Hash Utility** | Built-in security tools to calculate file integrity using MD5 and SHA-256 algorithms. |
| **📉 Syntax Highlight** | Multi-language support (Python, HTML, CSS, JS, MD) making your code more readable. |
| **⚙️ Accessibility** | Full control over text size with `Ctrl + Zoom` (Mouse Wheel/Keyboard) and word-wrap support. |

---

## 🛠️ Technologies Used

> **The engine behind PyNote**

*   **Logic**: Python 3.x (Standard Library & Custom Modular Architecture).
*   **GUI Engine**: Tkinter + Ttk (Standard library for native performance).
*   **Asset Management**: Pillow (PIL) for high-quality icons and image rendering.
*   **Background Tasks**: Python Threading (enables non-blocking Autosave and UI updates).
*   **Persistence**: Custom File Operations handler with `os` and `sys` integration.
*   **Security**: `hashlib` for industry-standard encryption algorithms.

---

## 📂 Architecture Overview

```text
PyNote/
 ├── images/          # UI Icons and Brand Assets
 ├── main.py          # Entry point (Initializes the app)
 ├── ui.py            # The User Interface Engine (Menus, Toolbars, Themes)
 ├── tabs.py          # High-performance multi-tab management logic
 ├── file_ops.py      # Core I/O operations and background Autosave
 ├── utils.py         # Helper tools (Hashing, Word Count, Search)
 ├── config.py        # Global settings and environment variables
 └── README.md        # System Documentation
```

---

## ⚙️ Installation & Setup

### 1. Repository Setup
```bash
git clone https://github.com/gauravpatil-06/PyNote-Smart-Text-Editor.git
cd PyNote-Smart-Text-Editor
```

### 2. Dependency Management
PyNote is designed to be lightweight. You only need the Pillow library for icons:
```bash
pip install Pillow
```

### 3. Launching the App
Simply run the main entry file:
```bash
python main.py
```

---

## 🛡️ Stability & Reliability

*   **Data Integrity**: Modified tabs are marked with an asterisk (`*`) and prompt for confirmation before closing to prevent data loss.
*   **Performance**: Threaded operations ensure the UI remains responsive even during heavy file I/O.
*   **Cross-Language support**: Pre-configured encoding (UTF-8) ensures your files are compatible across platforms.
*   **Professional Standards**: Follows standard Windows keyboard shortcuts (`Ctrl+S`, `Ctrl+O`, `Ctrl+F`) for zero learning curve.

---

> "I didn't just want a UI; I wanted a working system that feels professional, fast, and reliable. PyNote is the result of applying HCI principles to solve the friction of daily notes and coding."

---

<div align="center">

✨ **Making text editing smarter, faster, and more consistent.**

</div>