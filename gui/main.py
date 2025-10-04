import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

from serial_handler import SerialHandler
from transmitter_mode import TransmitterMode
from receiver_mode import ReceiverMode


def create_image_button(parent, image_path, label_text, command, size=(220, 220)):
    container = ttk.Frame(parent)
    
    img = Image.open(image_path).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    root = parent.winfo_toplevel()
    if not hasattr(root, "images"):
        root.images = []
    root.images.append(photo)

    bg = root.cget("bg")

    img_label = tk.Label(container, image=photo, bd=0, bg=bg,
                         highlightthickness=2, highlightbackground=bg, cursor="hand2")
    img_label.pack()

    text_label = ttk.Label(container, text=label_text, font=("Montserrat", 11),
                           anchor="center", justify="center", wraplength=380)
    text_label.pack(pady=(8, 0))

    hover_color = "#5dade2" 

    def on_enter(e):
        img_label.config(highlightbackground=hover_color)

    def on_leave(e):
        img_label.config(highlightbackground=bg)

    def on_click(e=None):
        try:
            command()
        except Exception as ex:
            print("Ошибка при выполнении команды:", ex)

    for w in (container, img_label, text_label):
        w.bind("<Enter>", on_enter)
        w.bind("<Leave>", on_leave)
        w.bind("<Button-1>", on_click)

    return container


def start_main_menu(root, serial_handler):
    for widget in root.winfo_children():
        widget.destroy()

    ttk.Label(root, text="Выберите режим работы", font=("Montserrat", 18, "bold")).pack(pady=16)

    assets_path = os.path.join(os.path.dirname(__file__), "assets")
    tx_path = os.path.join(assets_path, "siora-photography-bNVEo2HvMSE-unsplash.jpg")
    rx_path = os.path.join(assets_path, "wei-jiaheng-vdrERZCO_Oc-unsplash.jpg")

    frame = ttk.Frame(root)
    frame.pack(expand=True)

    tx_btn = create_image_button(
        frame,
        tx_path,
        "Передатчик — введите текст в приложении, Arduino будет мигать диодом по коду Морзе",
        lambda: TransmitterMode(root, serial_handler),
        size=(220, 220)
    )
    tx_btn.grid(row=0, column=0, padx=20, pady=10)

    rx_btn = create_image_button(
        frame,
        rx_path,
        "Приёмник — Arduino читаeт RGB-сенсором мигание и отправляет распознанный текст в приложение",
        lambda: ReceiverMode(root, serial_handler),
        size=(220, 220)
    )
    rx_btn.grid(row=0, column=1, padx=20, pady=10)


def main():
    root = ttk.Window(themename="darkly")
    root.title("LED Transreceiver")
    root.geometry("900x500")

    serial_handler = SerialHandler()
    serial_handler.connect()

    start_main_menu(root, serial_handler)

    def on_closing():
        serial_handler.disconnect()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
