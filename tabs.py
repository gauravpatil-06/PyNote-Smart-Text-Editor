# tabs.py
import os
import tkinter as tk
from tkinter import ttk
import config
from utils import highlight_syntax

class LineNumberCanvas(tk.Canvas):
    """Canvas to display line numbers for a text widget."""
    def __init__(self, parent, text_widget, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.text_widget = text_widget
        self.redraw()

    def redraw(self, *args):
        self.delete("all")
        i = self.text_widget.index("@0,0")
        
        is_dark = self.text_widget.cget("bg") == config.DARK_THEME['text_bg']
        theme = config.DARK_THEME if is_dark else config.LIGHT_THEME
        font = self.text_widget.cget("font")
        
        while True :
            dline = self.text_widget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            curr_width = self.winfo_width()
            self.create_text(curr_width - 8, y, anchor="ne", text=linenum, fill=theme['line_num_fg'], font=font)
            i = self.text_widget.index("%s+1line" % i)

class TabManager:
    """Manages the multiple tabs in the PyNote editor."""
    def __init__(self, notebook):
        self.notebook = notebook
        self.tabs = []
        self.new_file_counter = 1

    def add_tab(self, name=None, content="", file_path=None):
        """Creates a new tab with a text area and line numbers."""
        if name is None:
            name = f"new {self.new_file_counter}"
            self.new_file_counter += 1
            
        tab_frame = tk.Frame(self.notebook, bg=config.LIGHT_THEME['bg'])
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(tab_frame, orient=tk.VERTICAL)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_scroll = ttk.Scrollbar(tab_frame, orient=tk.HORIZONTAL)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Text widget
        text_widget = tk.Text(tab_frame, wrap=tk.NONE, undo=True, font=config.DEFAULT_FONT,
                              yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set,
                              padx=5, pady=5, borderwidth=0, highlightthickness=0,
                              selectbackground=config.LIGHT_THEME['select_bg'],
                              selectforeground=config.LIGHT_THEME['fg'])
        
        # Line numbers
        line_numbers = LineNumberCanvas(tab_frame, text_widget, width=65, 
                                        bg=config.LIGHT_THEME['line_num_bg'], highlightthickness=0)
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scroll.config(command=text_widget.yview)
        h_scroll.config(command=text_widget.xview)

        # Sync line numbers with scrolling
        def on_scroll(*args):
            v_scroll.set(*args)
            line_numbers.redraw()

        text_widget.config(yscrollcommand=on_scroll)
        
        # Events
        text_widget.bind("<KeyRelease>", lambda e: self.on_text_event(text_widget, line_numbers))
        text_widget.bind("<Button-1>", lambda e: self.on_text_event(text_widget, line_numbers))
        text_widget.bind("<MouseWheel>", lambda e: line_numbers.redraw())

        text_widget.insert(tk.END, content)
        highlight_syntax(text_widget, content, name)
        
        tab_data = {
            'frame': tab_frame,
            'text_widget': text_widget,
            'line_numbers': line_numbers,
            'file_path': file_path,
            'modified': False
        }
        self.tabs.append(tab_data)
        
        # Icon representation in tabs with Close (✖) symbol
        tab_name = "💾 " + name + "   x"
        self.notebook.add(tab_frame, text=tab_name)
        self.notebook.select(tab_frame)
        
        self.highlight_active_line(text_widget)
        
        # Track modification
        text_widget.bind("<<Modified>>", lambda e: self.on_content_modified(text_widget))
        
        return tab_data

    def on_text_event(self, text_widget, line_numbers):
        line_numbers.redraw()
        self.highlight_active_line(text_widget)

    def highlight_active_line(self, text_widget):
        text_widget.tag_remove("active_line", "1.0", tk.END)
        is_dark = text_widget.cget("bg") == config.DARK_THEME['text_bg']
        theme = config.DARK_THEME if is_dark else config.LIGHT_THEME
        
        text_widget.tag_add("active_line", "insert linestart", "insert lineend+1c")
        text_widget.tag_config("active_line", background=theme['active_line'])

    def on_content_modified(self, text_widget):
        current_index = self.notebook.index("current") if self.notebook.tabs() else -1
        if current_index >= 0:
            current_tab = self.tabs[current_index]
            if not current_tab['modified']:
                current_tab['modified'] = True
                filename = os.path.basename(current_tab['file_path']) if current_tab['file_path'] else f"new {current_index+1}"
                # In Notepad++, untitled tabs are tracked by their names.
                self.update_tab_title(current_index, filename, True)
            highlight_syntax(text_widget, text_widget.get(1.0, tk.END), filename if 'filename' in locals() else "")
            text_widget.edit_modified(False)

    def get_current_tab(self):
        current_index = self.notebook.index("current") if self.notebook.tabs() else -1
        if current_index >= 0 and current_index < len(self.tabs):
            return self.tabs[current_index]
        return None

    def close_current_tab(self):
        current_index = self.notebook.index("current")
        if current_index >= 0:
            self.tabs.pop(current_index)
            self.notebook.forget(current_index)

    def update_tab_title(self, index, name, modified=False):
        title = "💾 " + name + ("" if not modified else " *") + "  ×"
        self.notebook.tab(index, text=title)
