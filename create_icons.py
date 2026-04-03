# create_icons.py
from PIL import Image, ImageDraw

def create_close_icon():
    # Simple 12x12 close icon
    img = Image.new('RGBA', (12, 12), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Draw a simple X
    draw.line([2, 2, 9, 9], fill=(150, 150, 150, 255), width=2)
    draw.line([2, 9, 9, 2], fill=(150, 150, 150, 255), width=2)
    img.save('close_icon.png')

if __name__ == "__main__":
    create_close_icon()
