import tkinter as tk
from tkinter import PhotoImage, Text, Entry
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class IdentifyBreedPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        canvas = tk.Canvas(self, bg="#F7F8BB", height=735, width=960, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        image_image_title_identify = PhotoImage(file=relative_to_assets("title_identify.png"))
        canvas.create_image(479.0, 89.0, image=image_image_title_identify)

        canvas.create_text(
            121.0, 152.0, anchor="nw", text="Cat description:", fill="#000000", font=("Petrona Regular", 30 * -1)
        )
        canvas.create_text(
            121.0, 625.0, anchor="nw", text="Breed:", fill="#000000", font=("Petrona Regular", 30 * -1)
        )

        entry_image_describe = PhotoImage(file=relative_to_assets("entry_describe.png"))
        canvas.create_image(412.0, 338.0, image=entry_image_describe)
        self.entry_describe = Text(self, bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0, padx=10, pady=10)
        self.entry_describe.place(x=111.0, y=213.0, width=602.0, height=248.0)

        entry_image_breed = PhotoImage(file=relative_to_assets("entry_breed.png"))
        canvas.create_image(385.5, 642.0, image=entry_image_breed)
        self.entry_breed = Entry(self, bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
        self.entry_breed.place(x=244.0, y=606.0, width=283.0, height=70.0)

        # Buton Discover
        button_image_discover = PhotoImage(file=relative_to_assets("button_discover.png"))
        self.button_discover = tk.Button(
            self,
            image=button_image_discover,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=self.identify_breed
        )
        self.button_discover.place(x=303.0, y=490.0, width=217.0, height=89.0)

        button_image_hover_discover = PhotoImage(file=relative_to_assets("button_hover_discover.png"))

        def button_discover_hover(e):
            self.button_discover.config(image=button_image_hover_discover)

        def button_discover_leave(e):
            self.button_discover.config(image=button_image_discover)

        self.button_discover.bind('<Enter>', button_discover_hover)
        self.button_discover.bind('<Leave>', button_discover_leave)

        # Buton Back
        button_image_backk = PhotoImage(file=relative_to_assets("button_backk.png"))
        button_backk = tk.Button(
            self,
            image=button_image_backk,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.app.show_page("choosefeature")
        )
        button_backk.place(x=26.0, y=20.0, width=55.0, height=48.0)

        image_image_cat1 = PhotoImage(file=relative_to_assets("cat1.png"))
        canvas.create_image(812.0, 96.0, image=image_image_cat1)

        image_image_cat2 = PhotoImage(file=relative_to_assets("cat2.png"))
        canvas.create_image(776.0, 586.0, image=image_image_cat2)

        self.image_image_title_identify = image_image_title_identify
        self.entry_image_describe = entry_image_describe
        self.entry_image_breed = entry_image_breed
        self.button_image_discover = button_image_discover
        self.button_image_hover_discover = button_image_hover_discover
        self.button_image_backk = button_image_backk
        self.image_image_cat1 = image_image_cat1
        self.image_image_cat2 = image_image_cat2

    def identify_breed(self):
        descriere = self.entry_describe.get("1.0", "end").strip()
        print("Descriere primită:", descriere)
        self.entry_breed.delete(0, "end")
        self.entry_breed.insert(0, "Identified Breed")
