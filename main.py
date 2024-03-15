import qrcode
from tkinter import Tk, Label, Entry, Button, StringVar, filedialog, ttk, Menu, Frame
from PIL import ImageTk, Image
import io


# Dictionaries to store strings in different languages
strings = {
    "English": {
        "title": "QR Code Generator",
        "input_label": "Enter data for QR code and press 'Enter':",
        "generate_button": "Generate QR Code",
        "save_button": "Save QR Code",
        "success_gen": "QR code generated successfully!",
        "success_save": "QR code saved successfully at ",
        "enter_data": "Enter data to generate QR code.",
        "copy": "Copy",
        "paste": "Paste",
        "clear": "Clear",
    },
    "Русский": {
        "title": "Генератор QR-кодов",
        "input_label": "Введите данные для QR-кода и нажмите 'Enter':",
        "generate_button": "Сгенерировать QR-код",
        "save_button": "Сохранить QR-код",
        "success_gen": "QR-код успешно сгенерирован!",
        "success_save": "QR-код успешно сохранен в ",
        "enter_data": "Введите данные для создания QR-кода.",
        "copy": "Копировать",
        "paste": "Вставить",
        "clear": "Очистить",
    }
}

# Function to change language
def change_language(event=None):
    lang = lang_combobox.get()
    global current_lang
    current_lang = lang
    root.title(strings[lang]["title"])
    data_label.config(text=strings[lang]["input_label"])
    generate_button.config(text=strings[lang]["generate_button"])
    save_button.config(text=strings[lang]["save_button"])
    copy_button.config(text=strings[lang]["copy"])
    paste_button.config(text=strings[lang]["paste"])
    clear_button.config(text=strings[lang]["clear"])
    create_context_menu()

def generate_qr(event=None):
    data = data_input.get()
    if data:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        qr_image = ImageTk.PhotoImage(Image.open(img_buffer))
        qr_label.config(image=qr_image)
        qr_label.image = qr_image  # Keeping a reference to the image
        status_label.config(text=strings[current_lang]["success_gen"])

        # Adjusting window geometry to fit the image size
        width = img.size[0]
        height = img.size[1]
        root.geometry(f"{width+100}x{height+210}")

    else:
        status_label.config(text=strings[current_lang]["enter_data"])

def save_qr():
    data = data_input.get()
    if data:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if file_path:
            img.save(file_path)
            status_label.config(text=strings[current_lang]["success_save"] + file_path)
    else:
        status_label.config(text=strings[current_lang]["enter_data"])

# Function to copy text from the entry field
def copy_text(event=None):
    data_entry.event_generate("<<Copy>>")

# Function to paste text into the entry field
def paste_text(event=None):
    data_entry.event_generate("<<Paste>>")

# Function to clear text from the entry field
def clear_text(event=None):
    data_input.set("")

# Function to create context menu
def create_context_menu():
    global entry_menu, copy_menu_item, paste_menu_item, clear_menu_item
    entry_menu = Menu(data_entry, tearoff=0)
    copy_menu_item = entry_menu.add_command(label=strings[current_lang]["copy"], command=copy_text)
    paste_menu_item = entry_menu.add_command(label=strings[current_lang]["paste"], command=paste_text)
    clear_menu_item = entry_menu.add_command(label=strings[current_lang]["clear"], command=clear_text)
    data_entry.bind("<Button-3>", lambda event: entry_menu.post(event.x_root, event.y_root))

root = Tk()
root.title(strings["English"]["title"])
root.geometry("390x500")
root.minsize(390, 500)
root.resizable(True, True)  # Allow window resizing

current_lang = "English"

data_label = Label(root, text=strings["English"]["input_label"])
data_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

data_input = StringVar()
data_entry = Entry(root, textvariable=data_input)
data_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
root.grid_columnconfigure(0, weight=1)  # Stretch the width of the Entry as the window width increases
data_entry.bind("<Return>", generate_qr)
create_context_menu()


# Add Copy, Paste, and Clear buttons
button_frame = Frame(root)
button_frame.grid(row=2, column=0, padx=5, pady=5, sticky="w")

copy_button = Button(button_frame, text=strings["English"]["copy"], command=copy_text)
copy_button.pack(side="left", padx=5)

paste_button = Button(button_frame, text=strings["English"]["paste"], command=paste_text)
paste_button.pack(side="left", padx=5)

clear_button = Button(button_frame, text=strings["English"]["clear"], command=clear_text)
clear_button.pack(side="left", padx=5)

# Add Generate and Save buttons
generate_button = Button(root, text=strings["English"]["generate_button"], command=generate_qr)
generate_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

save_button = Button(root, text=strings["English"]["save_button"], command=save_qr)
save_button.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

# Add language selection
lang_label = Label(root, text="Language/Язык")
lang_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")

# Combobox for language selection
lang_combobox = ttk.Combobox(root, values=list(strings.keys()), state="readonly", width=10)
lang_combobox.current(0)
lang_combobox.bind("<<ComboboxSelected>>", change_language)
lang_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="e")

qr_label = Label(root)
qr_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

status_label = Label(root, text="")
status_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

root.mainloop()