# main.py
import tkinter as tk
from ui import PyNoteApp

def main():
    root = tk.Tk()
    
    # Initialize the Notepad++ inspired UI
    app = PyNoteApp(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
