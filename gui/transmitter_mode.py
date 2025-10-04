import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import END


class TransmitterMode:
    def __init__(self, root, serial_handler):
        self.root = root
        self.serial_handler = serial_handler

        for widget in root.winfo_children():
            widget.destroy()

        ttk.Label(root, text="Режим передатчика", font=("Montserrat", 18, "bold")).pack(pady=15)

        ttk.Label(root, text="Введите текст:", font=("Montserrat", 11)).pack(anchor="center", padx=30)

        self.input_field = ttk.Text(root, height=5, width=50, wrap="word")
        self.input_field.pack(padx=30, pady=10)
        self.input_field.focus()  

        send_button = ttk.Button(
            root,
            text="Отправить",
            bootstyle=SUCCESS,
            width=20,
            command=self.send_text
        )
        send_button.pack(pady=10)

        back_button = ttk.Button(
            root,
            text="Назад",
            bootstyle=SECONDARY,
            width=20,
            command=self.go_back
        )
        back_button.pack(pady=5)

        root.bind("<Return>", lambda event: self.send_text())
        root.bind("<Escape>", lambda event: self.go_back())

    def send_text(self):
        text = self.input_field.get("1.0", END).strip()
        if text:
            self.serial_handler.send_text(text)
            self.input_field.delete("1.0", END)

    def go_back(self):
        from main import start_main_menu
        self.root.unbind("<Return>")
        self.root.unbind("<Escape>")
        self.root.after(0, lambda: start_main_menu(self.root, self.serial_handler))
