import qrcode
from tkinter import Tk, Label, Entry, Button, StringVar, filedialog
from PIL import ImageTk, Image
import io

def generate_qr(event=None):  # Добавлен необязательный параметр event для привязки к клавише Enter
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
        qr_label.image = qr_image  # Сохраняем ссылку на изображение
        status_label.config(text="QR-код успешно сгенерирован!")
    else:
        status_label.config(text="Введите данные для создания QR-кода.")

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
            status_label.config(text=f"QR-код успешно сохранен в {file_path}")
    else:
        status_label.config(text="Введите данные для создания QR-кода.")

root = Tk()
root.title("Генератор QR-кодов")
root.geometry("400x400")
root.resizable(False, False)

data_label = Label(root, text="Введите данные для QR-кода:")
data_label.pack()

data_input = StringVar()
data_entry = Entry(root, textvariable=data_input)
data_entry.pack()
data_entry.bind("<Return>", generate_qr)  # Привязка нажатия Enter к функции generate_qr

generate_button = Button(root, text="Сгенерировать QR-код", command=generate_qr)
generate_button.pack()

save_button = Button(root, text="Сохранить QR-код", command=save_qr)
save_button.pack()

qr_label = Label(root)
qr_label.pack()

status_label = Label(root, text="")
status_label.pack()

root.mainloop()