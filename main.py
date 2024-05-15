import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


# TODO 1: Upload Image
def upload_image():
    global file_path, image_label
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        display_image(image)


def upload_logo():
    global logo_path, logo_label
    logo_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if logo_path:
        logo = Image.open(logo_path)
        display_logo(logo)



# TODO 2: Display Image
def display_image(image_new):
    global imagenew, image_label
    imagenew = image_new
    imagenew.thumbnail((300, 300))
    img = ImageTk.PhotoImage(imagenew)
    image_label = tk.Label(root)
    image_label.config(image=img)
    image_label.image = img
    image_label.grid(row=0, column=0, padx=10, pady=10)


def display_logo(logo):
    global logonew, logo_label
    logonew = logo
    logonew.thumbnail((300, 300))
    log = ImageTk.PhotoImage(logonew)
    logo_label = tk.Label(root)
    logo_label.config(image=log)
    logo_label.image = log
    logo_label.grid(row=0, column=1, padx=10, pady=10)



# TODO 3: Add Watermark
def add_watermark():
    watermark_text = entry.get()
    if watermark_text:
        with Image.open(file_path).convert("RGBA") as base:
            txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
            fnt = ImageFont.truetype("arial.ttf", 40)
            d = ImageDraw.Draw(txt)
            color = colorchooser.askcolor()[0]
            if color:
                fill_color = tuple(int(c) for c in color) + (128,)  
                d.text((10, 70), watermark_text, font=fnt, fill=fill_color)
                out = Image.alpha_composite(base, txt)
                display_image(out)


def add_watermark_img():
    with Image.open(file_path).convert("RGBA") as base:
        logo = Image.open(logo_path).convert("RGBA")  
        logo_width, logo_height = logo.size
        scale_factor = min(base.width / logo_width, base.height / logo_height)
        new_logo_width = int((logo_width * scale_factor)/2)
        new_logo_height = int((logo_height * scale_factor)/2)
        logo = logo.resize((new_logo_width, new_logo_height))
        translucent_logo = logo.copy()
        translucent_logo.putalpha(128)  
        position = ((base.width - new_logo_width)//2, ((base.height - new_logo_height))//2)
        base.paste(translucent_logo, position, logo)  
        display_logo(base)
        return base


# TODO 4: Save New Image
def save_text():
    file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file:
        imagenew.save(file)


def save_logo():
    file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file:
        logonew.save(file)


# TODO 5: Run Program
root = tk.Tk()
root.title("Image Watermark")

upload_image_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_image_button.grid(row=1, column=0, padx=5, pady=5)

entry = tk.Entry(root, width=30)
entry.grid(row=2, column=0, padx=5, pady=5)

watermark_button = tk.Button(root, text="Add Watermark", command=add_watermark)
watermark_button.grid(row=3, column=0, padx=5, pady=5)

upload_logo_button = tk.Button(root, text="Upload Logo", command=upload_logo)
upload_logo_button.grid(row=1, column=1, padx=5, pady=5)

file_label = tk.Label(root, text="Upload 'PNG' logo file")
file_label.grid(row=2, column=1, padx=5, pady=5)

watermark_logo_button = tk.Button(root, text="Add Watermark Logo", command=add_watermark_img)
watermark_logo_button.grid(row=3, column=1, padx=5, pady=5)

save_button_text = tk.Button(root, text="Save Image with Text", command=save_text)
save_button_text.grid(row=4, column=0, padx=5, pady=5)

save_button_logo = tk.Button(root, text="Save Image with Logo", command=save_logo)
save_button_logo.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()
