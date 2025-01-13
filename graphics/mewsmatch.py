import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path


class MewsMatchPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        # Calea către fișierele de resurse
        self.OUTPUT_PATH = Path(__file__).parent
        self.ASSETS_PATH = self.OUTPUT_PATH / Path("assets")

        def relative_to_assets(path: str) -> Path:
            return self.ASSETS_PATH / Path(path)

        # Creăm canvas-ul pentru pagina MewsMatch
        canvas = tk.Canvas(self, bg="#FFFFFF", height=735, width=960, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # Salvăm imaginile ca atribute ale clasei pentru a preveni garbage collection-ul
        self.image_image_background = PhotoImage(file=relative_to_assets("background.png"))
        canvas.create_image(480.0, 368.0, image=self.image_image_background)

        self.button_image_try = PhotoImage(file=relative_to_assets("button_try.png"))
        button_try = tk.Button(self, image=self.button_image_try, borderwidth=0, highlightthickness=0, relief="flat",
                               command=lambda: self.app.show_page("choosefeature"))
        button_try.place(x=341.0, y=321.0, width=278.0, height=93.0)

        self.button_image_hover_try = PhotoImage(file=relative_to_assets("button_hover_try.png"))

        def button_try_hover(e):
            button_try.config(image=self.button_image_hover_try)

        def button_try_leave(e):
            button_try.config(image=self.button_image_try)

        button_try.bind('<Enter>', button_try_hover)
        button_try.bind('<Leave>', button_try_leave)

        canvas.create_text(180.0, 226.0, anchor="nw", text="Your guide to identifying cat breeds, one meow at a time",
                           fill="#000000", font=("Petrona SemiBold", 24 * -1))

        self.image_image_title = PhotoImage(file=relative_to_assets("title.png"))
        canvas.create_image(480.0, 132.0, image=self.image_image_title)
