# utils.py
import re
import hashlib
import tkinter as tk
from tkinter import simpledialog, messagebox

KEYWORDS = {

    "python": [
        "False","None","True","and","as","assert","async","await","break","class","continue",
        "def","del","elif","else","except","finally","for","from","global","if","import","in",
        "is","lambda","nonlocal","not","or","pass","raise","return","try","while","with","yield",
        "__init__","__name__","self","print","input","len","range","open","str","int","float","list",
        "dict","set","tuple","super","type","dir","help","map","filter","zip","enumerate"
    ],

    "java": [
        "abstract","assert","boolean","break","byte","case","catch","char","class","const","continue",
        "default","do","double","else","enum","extends","final","finally","float","for","goto","if",
        "implements","import","instanceof","int","interface","long","native","new","package","private",
        "protected","public","return","short","static","strictfp","super","switch","synchronized","this",
        "throw","throws","transient","try","void","volatile","while",
        "String","System","out","println","Scanner","Integer","Double","Float","Boolean"
    ],

    "cpp": [
        "#include","#define","alignas","alignof","and","and_eq","asm","auto","bitand","bitor","bool",
        "break","case","catch","char","char16_t","char32_t","class","compl","const","constexpr",
        "const_cast","continue","decltype","default","delete","do","double","dynamic_cast","else",
        "enum","explicit","export","extern","false","float","for","friend","goto","if","inline",
        "int","long","mutable","namespace","new","noexcept","not","not_eq","nullptr","operator",
        "or","or_eq","private","protected","public","register","reinterpret_cast","return","short",
        "signed","sizeof","static","static_assert","static_cast","struct","switch","template","this",
        "thread_local","throw","true","try","typedef","typeid","typename","union","unsigned","using",
        "virtual","void","volatile","wchar_t","while","xor","xor_eq",
        "std","cout","cin","endl","vector","string","map","set"
    ],

    "c": [
        "#include","#define","auto","break","case","char","const","continue","default","do","double",
        "else","enum","extern","float","for","goto","if","int","long","register","return","short",
        "signed","sizeof","static","struct","switch","typedef","union","unsigned","void","volatile",
        "while","printf","scanf","malloc","free","sizeof"
    ],

    "javascript": [
        "break","case","catch","class","const","continue","debugger","default","delete","do","else",
        "export","extends","finally","for","function","if","import","in","instanceof","let","new",
        "return","super","switch","this","throw","try","typeof","var","void","while","with","yield",
        "async","await","true","false","null","undefined",
        "console","log","document","window","Array","Object","String","Number","Boolean","Promise"
    ]
}

def highlight_syntax(text_widget, content, filename=""):
    """Applies basic syntax highlighting based on file extension or content detection."""
    # Detect language - Skip highlighting for unsaved files ('new 1', etc.)
    if '.' not in filename:
        return
        
    ext = filename.split('.')[-1].lower()
    
    # Disable highlighting for plain text files as requested
    if ext == "txt":
        return
    
    lang = None
    if ext == "py": lang = "python"
    elif ext in ["java"]: lang = "java"
    elif ext in ["cpp", "hpp", "cc", "cxx"]: lang = "cpp"
    elif ext in ["c", "h"]: lang = "c"
    elif ext in ["js", "jsx"]: lang = "javascript"
    
    # Fallback content detection if no clear extension
    if not lang:
        if "public class" in content or "import java" in content: lang = "java"
        elif "#include" in content: lang = "cpp"
        elif "def " in content or "import " in content: lang = "python"
        elif "function" in content: lang = "javascript"
    
    # If no language detected at all, do nothing
    if not lang:
        return

    # Remove old tags
    for tag in ['keyword', 'string', 'comment']:
        text_widget.tag_remove(tag, "1.0", tk.END)
    
    # Keyword highlighting
    text_widget.tag_config('keyword', foreground='#000080') # Navy Blue
    for word in KEYWORDS.get(lang, []):
        start = "1.0"
        while True:
            idx = text_widget.search(r'\y' + word + r'\y', start, nocase=False, stopindex=tk.END, regexp=True)
            if not idx: break
            lastidx = '%s+%dc' % (idx, len(word))
            text_widget.tag_add('keyword', idx, lastidx)
            start = lastidx

    # String highlighting
    text_widget.tag_config('string', foreground='#032f62') # Dark blue
    for quote in ['"', "'"]:
        start = "1.0"
        while True:
            idx = text_widget.search(quote, start, stopindex=tk.END)
            if not idx: break
            end = text_widget.search(quote, "%s+1c" % idx, stopindex="%s lineend" % idx)
            if not end: break
            lastidx = "%s+1c" % end
            text_widget.tag_add('string', idx, lastidx)
            start = lastidx

    # Comment highlighting - Disabled as requested
    comment_chars = ["#", "//"]
    # We no longer apply special colors to comments here.

def word_count(text_widget):
    """Calculates word count, characters count, and lines count."""
    content = text_widget.get(1.0, tk.END).strip()
    words = len(content.split())
    chars = len(content)
    lines = int(text_widget.index(tk.END).split('.')[0]) - 1
    return words, chars, lines

def find_replace(text_widget):
    """Find and replace logic."""
    if not text_widget: return
    find_str = simpledialog.askstring("Find", "Enter search query (regex allowed):")
    if not find_str: return
    text_widget.tag_remove('found', '1.0', tk.END)
    text_widget.tag_config('found', background='yellow', foreground='black')
    idx = '1.0'
    count = 0
    while True:
        match_len = tk.IntVar()
        idx = text_widget.search(find_str, idx, nocase=1, stopindex=tk.END, regexp=True, count=match_len)
        if not idx: break
        lastidx = '%s+%dc' % (idx, match_len.get())
        text_widget.tag_add('found', idx, lastidx)
        idx = lastidx
        count += 1
    if count > 0:
        replace_str = simpledialog.askstring("Replace", f"Found {count} occurrences. Replace with:")
        if replace_str is not None:
            try:
                content = text_widget.get(1.0, tk.END)
                new_content = re.sub(find_str, replace_str, content)
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, new_content)
            except Exception: pass
        text_widget.tag_remove('found', '1.0', tk.END)

def calculate_hash(text_widget, algorithm="md5"):
    content = text_widget.get(1.0, tk.END).strip()
    if not content: return
    h = hashlib.new(algorithm)
    h.update(content.encode('utf-8'))
    simpledialog.askstring(f"{algorithm.upper()} Hash", "Hash result:", initialvalue=h.hexdigest())

def show_about():
    messagebox.showinfo("About PyNote", "PyNote – Smart Text Editor\nVersion 1.0\nProfessional Python IDE inspired by Notepad++.\n\nAll features finalized.")
