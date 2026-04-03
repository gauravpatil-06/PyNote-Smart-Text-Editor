import sys
import tkinter as tk
from tkinter import ttk, messagebox
import config
import os
from tabs import TabManager
from file_ops import FileOperations
from utils import word_count, find_replace, calculate_hash, show_about

try:
    from PIL import Image, ImageTk
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

class PyNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title(config.WINDOW_TITLE)
        
        # Maximize the window globally on launch
        try:
            self.root.state('zoomed') # Windows specific
        except Exception:
            self.root.geometry(config.WINDOW_SIZE)
        
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.logo_path = os.path.join(base_path, "images", "PyNote – Smart Text Editor.png")
        self.icon_image = None
        self.set_icon()
        
        self.is_dark_mode = False
        self.current_font_size = config.DEFAULT_FONT_SIZE
        
        # 1. Initialize Components
        self.create_status_bar_widgets()
        self.main_container = tk.Frame(self.root)
        
        # UI STYLE: Notepad++ style tabs
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook.Tab', padding=[10, 2], font=('Segoe UI', 9))
        style.map('TNotebook.Tab', background=[('selected', '#ffffff')])
        
        self.notebook = ttk.Notebook(self.main_container)
        self.tab_manager = TabManager(self.notebook)
        
        # 2. Logic initialization
        self.file_ops = FileOperations(self.root, self.tab_manager, self.status_labels)
        
        # 3. Pack UI elements
        self.create_toolbar() # TOP
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X) # BOTTOM
        self.main_container.pack(fill=tk.BOTH, expand=True) # CENTER
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        self.create_menu()
        
        # Initial Tab
        self.tab_manager.add_tab(name="new 1")
        
        # Bindings
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.on_tab_changed())
        self.notebook.bind("<Button-1>", self.on_notebook_click)
        
        # Zoom and Scroll Shortcuts
        self.root.bind("<Control-plus>", lambda e: self.zoom_in())
        self.root.bind("<Control-equal>", lambda e: self.zoom_in())
        self.root.bind("<Control-minus>", lambda e: self.zoom_out())
        self.root.bind("<Control-MouseWheel>", self.on_mouse_wheel_zoom)

        # Apply default theme and Word Wrap
        self.apply_theme()
        
        # Status Bar updates
        self.root.after(100, self.periodic_ui_updates)

    def set_icon(self):
        """Sets the application icon of the window and taskbar."""
        if HAS_PIL and os.path.exists(self.logo_path):
            try:
                # Windows specific trick to show custom icon in taskbar
                import ctypes
                myappid = 'google.pynote.editor.1.0' # unique string
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                
                img = Image.open(self.logo_path)
                self.icon_image = ImageTk.PhotoImage(img)
                self.root.iconphoto(True, self.icon_image)
            except Exception: pass

    def create_menu(self):
        """Creates the full Notepad++ menu structure exactly as requested."""
        self.menubar = tk.Menu(self.root, font=("Segoe UI", 9))
        
      
        menus = [
            ("File", ["New", "Open", "Save", "Save As", "Close Tab", "Exit"]),
            ("Edit", ["Undo", "Redo", "Cut", "Copy", "Paste", "Select All"]),
            ("Search", ["Find & Replace", "Next", "Previous"]),
            ("View", ["Zoom In", "Zoom Out", "Toggle Dark Mode"]),
            ("Encoding", ["UTF-8", "ANSI", "UTF-16"]),
            ("Language", ["Python", "HTML", "CSS", "JavaScript", "Markdown"]),
            ("Settings", ["Preferences", "Style Configurator"]),
            ("Tools", ["Word Count", "MD5", "SHA-256"]),
            ("Macro", ["Start Recording", "Stop Recording"]),
            ("Run", ["Run", "Get Python Path"]),
            ("Plugins", ["Plugins Admin", "About Plugins"]),
            ("Window", ["Close All", "Sort Tabs"]),
            ("?", ["About", "Help Content"])
        ]
        
        for menu_name, items in menus:
            m = tk.Menu(self.menubar, tearoff=0, font=("Segoe UI", 9))
            for item in items:
                cmd = None
                # Mapping logic for menu commands
                if item == "New": cmd = self.file_ops.new_file
                elif item == "Open": cmd = self.file_ops.open_file
                elif item == "Save": cmd = self.file_ops.save_file
                elif item == "Save As": cmd = self.file_ops.save_as_file
                elif item == "Close Tab": cmd = self.file_ops.confirm_close_tab
                elif item == "Exit": cmd = self.on_exit
                elif item == "Undo": cmd = lambda: self.get_text().edit_undo()
                elif item == "Redo": cmd = lambda: self.get_text().edit_redo()
                elif item == "Cut": cmd = lambda: self.get_text().event_generate("<<Cut>>")
                elif item == "Copy": cmd = lambda: self.get_text().event_generate("<<Copy>>")
                elif item == "Paste": cmd = lambda: self.get_text().event_generate("<<Paste>>")
                elif item == "Select All": cmd = self.select_all
                elif item == "Find & Replace": cmd = lambda: find_replace(self.get_text())
                elif item == "Zoom In": cmd = self.zoom_in
                elif item == "Zoom Out": cmd = self.zoom_out
                elif item == "Toggle Dark Mode": cmd = self.toggle_dark_mode
                elif item == "Word Count": cmd = self.show_word_count
                elif item == "Close All": cmd = self.file_ops.close_all_tabs
                # Stubs for additional tools - making it "Fully Functional"
                elif item == "MD5": cmd = lambda: calculate_hash(self.get_text(), "md5")
                elif item == "SHA-256": cmd = lambda: calculate_hash(self.get_text(), "sha256")
                elif item == "About": cmd = show_about
                # Encoding stubs
                elif item in ["UTF-8", "ANSI", "UTF-16"]: 
                    cmd = lambda i=item: self.status_labels['encoding'].config(text=i)
                # Language stubs
                elif item in ["Python", "HTML", "CSS", "JavaScript", "Markdown"]:
                    cmd = lambda i=item: self.status_labels['doc_type'].config(text=f"{i} file")
                
                m.add_command(label=item, command=cmd)
            self.menubar.add_cascade(label=menu_name, menu=m)
            
        self.root.config(menu=self.menubar)

        # Global Shortcuts
        self.root.bind("<Control-n>", lambda e: self.file_ops.new_file())
        self.root.bind("<Control-o>", lambda e: self.file_ops.open_file())
        self.root.bind("<Control-s>", lambda e: self.file_ops.save_file())
        self.root.bind("<Control-w>", lambda e: self.file_ops.confirm_close_tab())
        self.root.bind("<Control-f>", lambda e: find_replace(self.get_text()))
        self.root.bind("<Control-a>", self.select_all)

    def create_toolbar(self):
        self.toolbar_frame = tk.Frame(self.root, bd=1, relief=tk.RAISED, bg="#f0f0f0", pady=0)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        btns = [
            ("📄", self.file_ops.new_file, "New", "#000000"),
            ("📂", self.file_ops.open_file, "Open", "#e6a100"),
            ("💾", self.file_ops.save_file, "Save", "#1e7145"),
            ("🔙", self.safe_undo, "Undo", "#404040"),
            ("🔜", self.safe_redo, "Redo", "#404040"),
            ("✂️", lambda: self.get_text().event_generate("<<Cut>>"), "Cut", "#d83b01"),
            ("📋", lambda: self.get_text().event_generate("<<Copy>>"), "Copy", "#0078d7"),
            ("📝", lambda: self.get_text().event_generate("<<Paste>>"), "Paste", "#5c2d91"),
            ("🔍", lambda: find_replace(self.get_text()), "Search", "#0078d7"),
            ("➕", self.zoom_in, "Zoom In", "#404040"),
            ("➖", self.zoom_out, "Zoom Out", "#404040"),
            ("🌙", self.toggle_dark_mode, "Toggle Theme", "#404040")
        ]
        for text, cmd, hint, color in btns:
            btn = tk.Button(self.toolbar_frame, text=text, command=cmd, relief=tk.FLAT, 
                           bg="#f0f0f0", fg=color, padx=1, pady=0, overrelief=tk.RAISED,
                           font=("Segoe UI Emoji", 10))
            btn.pack(side=tk.LEFT, padx=0)

    def create_status_bar_widgets(self):
        self.status_bar = tk.Frame(self.root, bd=0, bg="#f0f0f0")
        self.status_labels = {}
        specs = [
            ("doc_type", "Normal text file", 25, tk.LEFT),
            ("ins", "INS", 5, tk.RIGHT),
            ("encoding", "UTF-8", 10, tk.RIGHT),
            ("eol", "Windows (CR LF)", 16, tk.RIGHT),
            ("pos", "Ln: 1   Col: 1   Pos: 0", 28, tk.RIGHT),
            ("stats", "length: 0   lines: 1", 22, tk.RIGHT)
        ]
        for key, default, width, side in specs:
            lbl = tk.Label(self.status_bar, text=default, anchor=tk.W if side==tk.LEFT else tk.CENTER, 
                           borderwidth=1, relief=tk.GROOVE, width=width, font=("Segoe UI", 9), bg="#f0f0f0")
            lbl.pack(side=side, fill=tk.Y, padx=0, pady=0, ipadx=4)
            self.status_labels[key] = lbl

    def get_text(self):
        tab = self.tab_manager.get_current_tab()
        return tab['text_widget'] if tab else None

    def select_all(self, event=None):
        tw = self.get_text()
        if tw:
            tw.tag_add("sel", "1.0", tk.END)
            tw.mark_set(tk.INSERT, "1.0")
            tw.see("1.0")
        return "break"

    def safe_undo(self):
        try:
            tw = self.get_text()
            if tw: tw.edit_undo()
        except Exception: pass

    def safe_redo(self):
        try:
            tw = self.get_text()
            if tw: tw.edit_redo()
        except Exception: pass

    def zoom_in(self):
        if self.current_font_size < 50:
            self.current_font_size += 2
            self.apply_font()

    def zoom_out(self):
        if self.current_font_size > 6:
            self.current_font_size -= 2
            self.apply_font()

    def on_mouse_wheel_zoom(self, event):
        if event.state & 0x0004: # Control key is held
            if event.delta > 0: self.zoom_in()
            else: self.zoom_out()

    def apply_font(self):
        font = ("Consolas", self.current_font_size)
        for tab in self.tab_manager.tabs:
            tab['text_widget'].config(font=font)
            if 'line_numbers' in tab:
                tab['line_numbers'].redraw()

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        sel_bg = "#8fdb8f" if not self.is_dark_mode else "#2d7a2d"
        sel_fg = "#000000" if not self.is_dark_mode else "#ffffff"
        text_bg = "#ffffff" if not self.is_dark_mode else "#1e1e1e"
        text_fg = "#000000" if not self.is_dark_mode else "#d4d4d4"

        self.root.config(bg="#f0f0f0" if not self.is_dark_mode else "#2d2d2d")
        
        for tab in self.tab_manager.tabs:
            tw = tab['text_widget']
            tw.config(
                bg=text_bg, fg=text_fg,
                selectbackground=sel_bg, selectforeground=sel_fg,
                font=("Consolas", self.current_font_size),
                wrap=tk.WORD,
                insertbackground=text_fg
            )
            if 'line_numbers' in tab:
                tab['line_numbers'].redraw()

    def show_word_count(self):
        tab = self.tab_manager.get_current_tab()
        if tab:
            content = tab['text_widget'].get(1.0, tk.END)
            words = len(content.split())
            messagebox.showinfo("Word Count", f"Words: {words}")

    def on_exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

    def on_tab_changed(self):
        tab = self.tab_manager.get_current_tab()
        if tab:
            self.update_status()

    def on_notebook_click(self, event):
        """Detect click on the 'X' symbol in tabs."""
        element = self.notebook.identify(event.x, event.y)
        if element == "label":
            index = self.notebook.index(f"@{event.x},{event.y}")
            try:
                rect = self.notebook.bbox(index)
                if rect:
                    # Precise hit zone for '×' symbol (last 15 pixels of the tab)
                    if event.x > (rect[0] + rect[2] - 15):
                        self.file_ops.confirm_close_tab(index)
                    # Clicking elsewhere on the label naturally selects the tab via Tkinter defaults
            except Exception: pass

    def update_status(self):
        tab = self.tab_manager.get_current_tab()
        if not tab: return
        tw = tab['text_widget']
        content = tw.get(1.0, tk.END)
        length = len(content)-1
        lines = int(tw.index(tk.END).split('.')[0])-1
        cur = tw.index(tk.INSERT)
        ln, col = cur.split('.')
        pos = len(tw.get("1.0", tk.INSERT))
        self.status_labels['stats'].config(text=f"length: {length}   lines: {lines}")
        self.status_labels['pos'].config(text=f"Ln: {ln}   Col: {int(col)+1}   Pos: {pos}")

    def periodic_ui_updates(self):
        self.update_status()
        self.root.after(100, self.periodic_ui_updates)