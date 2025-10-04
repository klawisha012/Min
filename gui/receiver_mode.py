import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import END
import threading


class ReceiverMode:
    def __init__(self, root, serial_handler):
        self.root = root
        self.serial_handler = serial_handler

        for widget in root.winfo_children():
            widget.destroy()

        ttk.Label(root, text="Режим приёмника", font=("Montserrat", 18, "bold")).pack(pady=15)

        ttk.Label(root, text="Полученный текст:", font=("Montserrat", 11)).pack(anchor="center", padx=30)

        self.output_field = ttk.Text(root, height=10, width=50, wrap="word", state="disabled")
        self.output_field.pack(padx=30, pady=10)

        clear_button = ttk.Button(
            root,
            text="Очистить",
            bootstyle=WARNING,
            width=20,
            command=self.clear_output
        )
        clear_button.pack(pady=5)

        back_button = ttk.Button(
            root,
            text="Назад",
            bootstyle=SECONDARY,
            width=20,
            command=self.go_back
        )
        back_button.pack(pady=5)

        root.bind("<Escape>", lambda event: self.go_back())
        root.bind("<Control-l>", lambda event: self.clear_output())

        self.running = True
        self.thread = threading.Thread(target=self.read_morse, daemon=True)
        self.thread.start()

    def read_morse(self):
        while self.running:
            line = self.serial_handler.read_line()
            if line:
                self.output_field.config(state="normal")
                self.output_field.insert(END, line + '\n')
                self.output_field.see(END)
                self.output_field.config(state="disabled")

    def clear_output(self):
        self.output_field.config(state="normal")
        self.output_field.delete("1.0", END)
        self.output_field.config(state="disabled")

    def go_back(self):
        self.running = False
        from main import start_main_menu
        self.root.unbind("<Escape>")
        self.root.unbind("<Control-l>")
        self.root.after(0, lambda: start_main_menu(self.root, self.serial_handler))