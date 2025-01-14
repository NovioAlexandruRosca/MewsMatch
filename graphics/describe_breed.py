import tkinter as tk
from tkinter import PhotoImage, Text, Entry
from pathlib import Path
import tkinter.font as tkfont
from project.cat_description import get_breed_description
from project.cat_description_manual import get_breed_description_manual

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


races = ["Birman", "European", "Maine Coon", "Bengal", "Persian", "Siamese", "British Shorthair",
                 "Chartreux", "Ragdoll", "Turkish Angora", "Sphynx", "Savannah"]


class DescribeBreedPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        canvas = tk.Canvas(self, bg="#F7F8BB", height=735, width=960, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        canvas.create_text(
            109.0, 152.0, anchor="nw", text="Cat breed:", fill="#000000", font=("Century Gothic", 30 * -1)
        )
        canvas.create_text(
            109.0, 368.0, anchor="nw", text="Description:", fill="#000000", font=("Century Gothic", 30 * -1)
        )

        entry_image_description = PhotoImage(file=relative_to_assets("entry_description.png"))
        canvas.create_image(398.5, 543.0, image=entry_image_description)
        custom_font = tkfont.Font(family="Century Gothic", size=10)
        self.entry_description = Text(self, bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0, padx=10, pady=10, font=custom_font, wrap="word")
        self.entry_description.place(x=101.0, y=418.0, width=595.0, height=248.0)

        entry_image_race = PhotoImage(file=relative_to_assets("entry_race.png"))
        canvas.create_image(223.5, 238.0, image=entry_image_race)
        self.entry_race = Entry(self, bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0, font=tkfont.Font(family="Century Gothic", size=18))
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
        canvas.create_image(843.0, 550.0, image=image_cat3)

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

        self.text_length = tk.DoubleVar(value=0.6)

        length_label = tk.Label(self, text="Text Length:", font=("Century Gothic", 12), bg="#F7F8BB")
        length_label.place(x=720, y=200)

        length_options = [
            ("Very Small", 0.3),
            ("Small", 0.4),
            ("Normal", 0.6),
            ("Medium", 0.8),
            ("Long", 1.0),
        ]

        y_offset = 230
        for text, value in length_options:
            radio = tk.Radiobutton(
                self,
                text=text,
                variable=self.text_length,
                value=value,
                font=("Century Gothic", 10),
                bg="#F7F8BB",
                anchor="w",
                padx=5,
                pady=2
            )
            radio.place(x=720, y=y_offset)
            y_offset += 25

        self.text_speed = tk.IntVar(value=15)

        speed_label = tk.Label(self, text="Text Speed:", font=("Century Gothic", 12), bg="#F7F8BB")
        speed_label.place(x=840, y=200)

        speed_options = [
            ("Slow", 30),
            ("Normal", 15),
            ("Fast", 5),
            ("Instant", 1),
        ]

        y_offset = 230
        for text, value in speed_options:
            radio = tk.Radiobutton(
                self,
                text=text,
                variable=self.text_speed,
                value=value,
                font=("Century Gothic", 10),
                bg="#F7F8BB",
                anchor="w",
                padx=5,
                pady=2
            )
            radio.place(x=840, y=y_offset)
            y_offset += 33

        self.mode_var = tk.IntVar(value=1)

        mode_label = tk.Label(self, text="Gen Mode:", font=("Century Gothic", 12), bg="#F7F8BB")
        mode_label.place(x=780, y=360)

        mode_options = [
            ("Manual", 1),
            ("Llama", 2),
        ]

        y_offset = 390
        for text, value in mode_options:
            radio = tk.Radiobutton(
                self,
                text=text,
                variable=self.mode_var,
                value=value,
                font=("Century Gothic", 10),
                bg="#F7F8BB",
                anchor="w",
                padx=5,
                pady=2
            )
            radio.place(x=780, y=y_offset)
            y_offset += 25

    def describe_breed(self):
        breed = self.entry_race.get().strip()

        if breed not in races:
            self.display_text_gradually("The chosen cat breed doesn't exist. Please choose a valid cat breed")
            return

        if self.mode_var.get() == 2:
            description = get_breed_description(breed)
        else:
            description = get_breed_description_manual(breed, self.text_length.get())

        self.entry_description.delete("1.0", "end")
        self.display_text_gradually(description)

    def display_text_gradually(self, text, index=0):
        if index < len(text):
            current_text = self.entry_description.get("1.0", "end-1c")
            self.entry_description.delete("1.0", "end")
            self.entry_description.insert("1.0", current_text + text[index])
            self.entry_description.see("end")
            self.after(self.text_speed.get(), self.display_text_gradually, text, index + 1)

