import tkinter as tk
from tkinter import PhotoImage, Text, Entry
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class DescribeBreedPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        canvas = tk.Canvas(self, bg="#F7F8BB", height=735, width=960, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        canvas.create_text(
            109.0, 152.0, anchor="nw", text="Cat breed:", fill="#000000", font=("Petrona Regular", 30 * -1)
        )
        canvas.create_text(
            109.0, 368.0, anchor="nw", text="Description:", fill="#000000", font=("Petrona Regular", 30 * -1)
        )

        entry_image_description = PhotoImage(file=relative_to_assets("entry_description.png"))
        canvas.create_image(398.5, 543.0, image=entry_image_description)
        self.entry_description = Text(self, bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0, padx=10, pady=10)
        self.entry_description.place(x=101.0, y=418.0, width=595.0, height=248.0)

        entry_image_race = PhotoImage(file=relative_to_assets("entry_race.png"))
        canvas.create_image(223.5, 238.0, image=entry_image_race)
        self.entry_race = Entry(self, bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0)
        self.entry_race.place(x=101.0, y=202.0, width=245.0, height=70.0)

        # Buton Describe
        button_image_describe2 = PhotoImage(file=relative_to_assets("button_describe2.png"))
        self.button_describe2 = tk.Button(
            self,
            image=button_image_describe2,
            borderwidth=0,
            highlightthickness=0,
            command=self.describe_breed,
            relief="flat"
        )
        self.button_describe2.place(x=437.0, y=193.0, width=217.0, height=89.0)

        button_image_hover_describe2 = PhotoImage(file=relative_to_assets("button_hover_describe2.png"))

        def button_describe2_hover(e):
            self.button_describe2.config(image=button_image_hover_describe2)

        def button_describe2_leave(e):
            self.button_describe2.config(image=button_image_describe2)

        self.button_describe2.bind('<Enter>', button_describe2_hover)
        self.button_describe2.bind('<Leave>', button_describe2_leave)

        # Buton Back
        button_image_backkk = PhotoImage(file=relative_to_assets("button_backkk.png"))
        button_backkk = tk.Button(
            self,
            image=button_image_backkk,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.app.show_page("choosefeature"),
            relief="flat"
        )
        button_backkk.place(x=26.0, y=20.0, width=55.0, height=48.0)

        image_title_explore = PhotoImage(file=relative_to_assets("title_explore.png"))
        canvas.create_image(477.0, 80.0, image=image_title_explore)

        image_cat3 = PhotoImage(file=relative_to_assets("cat3.png"))
        canvas.create_image(843.0, 466.0, image=image_cat3)

        image_cat4 = PhotoImage(file=relative_to_assets("cat4.png"))
        canvas.create_image(801.0, 112.0, image=image_cat4)

        self.image_title_explore = image_title_explore
        self.entry_image_description = entry_image_description
        self.entry_image_race = entry_image_race
        self.button_image_describe2 = button_image_describe2
        self.button_image_hover_describe2 = button_image_hover_describe2
        self.button_image_backkk = button_image_backkk
        self.image_cat3 = image_cat3
        self.image_cat4 = image_cat4

    def describe_breed(self):
        breed = self.entry_race.get().strip()
        description = self.get_breed_description(breed)
        self.entry_description.delete("1.0", "end")
        self.entry_description.insert("1.0", description)

    def get_breed_description(self, breed):
        descriptions = {
            "Persian": "The Persian cat is known for its long, luxurious coat and round face.",
            "Maine Coon": "The Maine Coon is one of the largest domesticated cat breeds, with tufted ears and a bushy tail.",
        }

        return descriptions.get(breed, "Description not available for this breed.")
