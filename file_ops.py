# file_ops.py
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import config


class FileOperations:
    """Handles file-related operations and autosave logic."""
    def __init__(self, root, tab_manager, status_labels):
        self.root = root
        self.tab_manager = tab_manager
        self.status_labels = status_labels
        self.autosave_enabled = True
        
        # Start background thread for periodic checks
        self.worker = threading.Thread(target=self.autosave_ticker, daemon=True)
        self.worker.start()

    def autosave_ticker(self):
        """Background thread to wait for autosave interval."""
        while self.autosave_enabled:
            time.sleep(config.AUTOSAVE_INTERVAL)
            # Schedule save logic on the main Tkinter thread
            self.root.after(0, self.autosave_check)

    def new_file(self):
        """Creates a new empty tab."""
        self.tab_manager.add_tab()

    def open_file(self):
        """Opens a file dialog and adds content to a new tab."""
        file_path = filedialog.askopenfilename(defaultextension=".txt", 
                                             filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                filename = os.path.basename(file_path)
                self.tab_manager.add_tab(filename, content, file_path)
                self.status_labels['doc_type'].config(text=f"Opened: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self, event=None):
        """Saves current tab content."""
        current_tab = self.tab_manager.get_current_tab()
        if not current_tab: return
        
        if current_tab['file_path']:
            self._write_to_disk(current_tab)
        else:
            self.save_as_file()

    def save_as_file(self):
        """Saves current tab content as a new file."""
        current_tab = self.tab_manager.get_current_tab()
        if not current_tab: return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            current_tab['file_path'] = file_path
            self._write_to_disk(current_tab)

    def _write_to_disk(self, tab_data):
        """Helper to write tab content to disk."""
        try:
            content = tab_data['text_widget'].get(1.0, tk.END)
            with open(tab_data['file_path'], "w", encoding="utf-8") as f:
                f.write(content)
            tab_data['modified'] = False
            filename = os.path.basename(tab_data['file_path'])
            
            # Find the index of this tab
            for index, t in enumerate(self.tab_manager.tabs):
                if t == tab_data:
                    self.tab_manager.update_tab_title(index, filename, False)
                    break
                    
            from utils import highlight_syntax
            highlight_syntax(tab_data['text_widget'], content, filename)
            
            self.status_labels['doc_type'].config(text=f"Saved: {tab_data['file_path']}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

    def autosave_check(self):
        """Checks and saves all modified tabs that have a file path."""
        for i, tab in enumerate(self.tab_manager.tabs):
            if tab['modified'] and tab['file_path']:
                try:
                    content = tab['text_widget'].get(1.0, tk.END)
                    with open(tab['file_path'], "w", encoding="utf-8") as f:
                        f.write(content)
                    tab['modified'] = False
                    filename = os.path.basename(tab['file_path'])
                    self.tab_manager.update_tab_title(i, filename, False)
                except Exception:
                    pass # Silently fail autosave

    def close_all_tabs(self):
        """Closes all open tabs with save confirmation for each."""
        total = self.tab_manager.notebook.tabs()
        if not total: return
        for i in range(len(total) - 1, -1, -1):
            if not self.confirm_close_tab(i):
                 break 

    def confirm_close_tab(self, index=None):
        """Confirm with user before closing a specific or current tab."""
        if index is not None:
             tab = self.tab_manager.tabs[index]
             self.tab_manager.notebook.select(index)
        else:
             tab = self.tab_manager.get_current_tab()
             index = self.tab_manager.notebook.index("current") if self.tab_manager.notebook.tabs() else -1
        
        if not tab: return True
        
        has_content = len(tab['text_widget'].get(1.0, tk.END)) > 1
        should_prompt = tab['modified'] or (not tab['file_path'] and has_content)

        if should_prompt:
            name = os.path.basename(tab['file_path']) if tab['file_path'] else f"new {index+1}"
            response = messagebox.askyesnocancel("Save", f"Save file \"{name}\" ?")
            
            if response is True: # Yes
                self.save_file()
                self.tab_manager.tabs.pop(index)
                self.tab_manager.notebook.forget(index)
                return True
            elif response is False: # No
                self.tab_manager.tabs.pop(index)
                self.tab_manager.notebook.forget(index)
                return True
            else: # Cancel
                return False
        else:
            if index < len(self.tab_manager.tabs):
                self.tab_manager.tabs.pop(index)
            self.tab_manager.notebook.forget(index)
            return True
