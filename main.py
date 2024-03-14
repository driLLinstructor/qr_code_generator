import qrcode
from tkinter import Tk, Label, Entry, Button, StringVar, filedialog, ttk
from PIL import ImageTk, Image
import io

# Dictionaries to store strings in different languages
strings = {
   "English": {
       "title": "QR Code Generator",
       "input_label": "Enter data for QR code:",
       "generate_button": "Generate QR Code",
       "save_button": "Save QR Code",
       "success_gen": "QR code generated successfully!",
       "success_save": "QR code saved successfully at ",
       "enter_data": "Enter data to generate QR code."
   },
   "Русский": {
       "title": "Генератор QR-кодов",
       "input_label": "Введите данные для QR-кода:",
       "generate_button": "Сгенерировать QR-код",
       "save_button": "Сохранить QR-код",
       "success_gen": "QR-код успешно сгенерирован!",
       "success_save": "QR-код успешно сохранен в ",
       "enter_data": "Введите данные для создания QR-кода."
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
       root.geometry(f"{width+100}x{height+150}")

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

root = Tk()
root.title(strings["English"]["title"])  # English language set by default
root.geometry("390x440")  # Increasing window width
root.resizable(False, False)

current_lang = "English"  # Current language set to English by default

data_label = Label(root, text=strings["English"]["input_label"])
data_label.pack()

data_input = StringVar()
data_entry = Entry(root, textvariable=data_input)
data_entry.pack()
data_entry.bind("<Return>", generate_qr)

generate_button = Button(root, text=strings["English"]["generate_button"], command=generate_qr)
generate_button.pack()

save_button = Button(root, text=strings["English"]["save_button"], command=save_qr)
save_button.pack()

lang_label = Label(root, text="Language/Язык")
lang_label.place(relx=0.735, y=10)  # Positioning relative to the right edge of the window

# Combobox for language selection
lang_combobox = ttk.Combobox(root, values=list(strings.keys()), state="readonly", width=10)
lang_combobox.current(0)  # Setting English as the default language
lang_combobox.bind("<<ComboboxSelected>>", change_language)
lang_combobox.place(relx=0.74, y=30)  # Positioning relative to the right edge of the window

qr_label = Label(root)
qr_label.pack()

status_label = Label(root, text="")
status_label.pack()

root.mainloop()