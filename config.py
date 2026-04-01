# config.py

# Color Palettes (Notepad++ Inspired)
LIGHT_THEME = {
    'bg': '#f0f0f0',
    'fg': '#000000',
    'text_bg': '#ffffff',
    'text_fg': '#000000',
    'cursor': '#000000',
    'select_bg': '#c1f2c1',        # Green selection as requested
    'status_bg': '#f0f0f0',
    'line_num_bg': '#e4e4e4',
    'line_num_fg': '#2b91af',
    'active_line': '#e8e8ff',      # Light purple active line highlight
    'active_tab_bg': '#ffffff',
    'inactive_tab_bg': '#dcdcdc'
}

DARK_THEME = {
    'bg': '#2d2d2d',
    'fg': '#cccccc',
    'text_bg': '#1e1e1e',
    'text_fg': '#dcdcdc',
    'cursor': '#ffffff',
    'select_bg': '#1b4d1b',        # Dark green selection
    'status_bg': '#252526',
    'line_num_bg': '#333333',
    'line_num_fg': '#858585',
    'active_line': '#2b2b2b'
}

# Zoom settings
MIN_FONT_SIZE = 6
MAX_FONT_SIZE = 50
ZOOM_STEP = 2

# Editor Settings
DEFAULT_FONT_FAMILY = "Consolas"
DEFAULT_FONT_SIZE = 11
DEFAULT_FONT = (DEFAULT_FONT_FAMILY, DEFAULT_FONT_SIZE)
AUTOSAVE_INTERVAL = 30  # seconds
WINDOW_TITLE = "PyNote – Smart Text Editor"
WINDOW_SIZE = "1200x800"
