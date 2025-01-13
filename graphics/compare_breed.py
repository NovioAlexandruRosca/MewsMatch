import tkinter as tk
from tkinter import PhotoImage, Text, Entry, Frame, Scrollbar, Listbox, VERTICAL, Label
from pathlib import Path
import tkinter.font as tkfont
from project.two_cats_distinctions import generate_cats_comparison

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class CompareBreedPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        canvas = tk.Canvas(self, bg="#F7F8BB", height=735, width=960, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        canvas.create_text(
            103.0, 446.0, anchor="nw", text="Comparison:", fill="#000000", font=("Century Gothic", 24 * -1)
        )

        self.selected_races1 = []
        self.selected_races2 = []

        # Scrollable frame 1
        self.frame1 = Frame(self, bg="#F5F5F5", width=200, height=300)
        self.frame1.place(x=180, y=100)

        scrollbar1 = Scrollbar(self.frame1, orient=VERTICAL)
        scrollbar1.pack(side="right", fill="y")

        self.listbox1 = Listbox(self.frame1, yscrollcommand=scrollbar1.set, width=20, height=11)
        races = ["Birman", "European", "Maine Coon", "Bengal", "Persian", "Siamese", "British Shorthair",
                 "Chartreux", "Ragdoll", "Turkish Angora", "Sphynx", "Savannah"]

        self.listbox1.config(font=("Century Gothic", 13))

        for race in races:
            self.listbox1.insert("end", race)
        self.listbox1.pack(side="left", fill="both")

        scrollbar1.config(command=self.listbox1.yview)
        self.listbox1.bind("<<ListboxSelect>>", lambda e: self.breed_select(e, self.frame1, self.listbox1, self.selected_races1))

        # Scrollable frame 2
        self.frame2 = Frame(self, bg="#F5F5F5", width=200, height=300)
        self.frame2.place(x=480, y=100)

        scrollbar2 = Scrollbar(self.frame2, orient=VERTICAL)
        scrollbar2.pack(side="right", fill="y")

        self.listbox2 = Listbox(self.frame2, yscrollcommand=scrollbar2.set, width=20, height=11)
        self.listbox2.config(font=("Century Gothic", 13))
        for race in races:
            self.listbox2.insert("end", race)
        self.listbox2.pack(side="left", fill="both")

        scrollbar2.config(command=self.listbox2.yview)
        self.listbox2.bind("<<ListboxSelect>>", lambda e: self.breed_select(e, self.frame2, self.listbox2, self.selected_races2))

        self.entry_image_compare = PhotoImage(file=relative_to_assets("entry_compare.png"))
        self.entry_bg_compare = canvas.create_image(378.0, 599.0, image=self.entry_image_compare)

        custom_font = tkfont.Font(family="Century Gothic", size=10)
        self.entry_compare = Text(self, bd=0, bg="#F5F5F5", fg="#000716", highlightthickness=0, padx=10, pady=10, font=custom_font, wrap="word")
        self.entry_compare.place(x=109.0, y=487.0, width=538.0, height=222.0)

        self.button_image_compare2 = PhotoImage(file=relative_to_assets("button_compare2.png"))
        self.button_compare2 = tk.Button(
            self,
            image=self.button_image_compare2,
            borderwidth=0,
            highlightthickness=0,
            command=self.compare_races,
            relief="flat"
        )
        self.button_compare2.place(x=334.0, y=368.0, width=180.0, height=79.11111450195312)

        self.button_image_hover_compare2 = PhotoImage(file=relative_to_assets("button_hover_compare2.png"))

        def button_compare2_hover(e):
            self.button_compare2.config(image=self.button_image_hover_compare2)

        def button_compare2_leave(e):
            self.button_compare2.config(image=self.button_image_compare2)

        self.button_compare2.bind('<Enter>', button_compare2_hover)
        self.button_compare2.bind('<Leave>', button_compare2_leave)

        # Back button
        self.button_image_back = PhotoImage(file=relative_to_assets("button_back.png"))
        self.button_back = tk.Button(
            self,
            image=self.button_image_back,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.app.show_page("choosefeature"),
            relief="flat"
        )
        self.button_back.place(x=26.0, y=20.0, width=55.0, height=48.0)

        self.image_image_compare = PhotoImage(file=relative_to_assets("title_compare.png"))
        self.image_compare = canvas.create_image(480.0, 52.0, image=self.image_image_compare)

        self.image_image_cat5 = PhotoImage(file=relative_to_assets("cat5.png"))
        self.image_cat5 = canvas.create_image(839.0, 85.0, image=self.image_image_cat5)

        self.image_image_cat6 = PhotoImage(file=relative_to_assets("cat6.png"))
        self.image_cat6 = canvas.create_image(814.0, 575.0, image=self.image_image_cat6)

        self.image_title_compare = self.image_image_compare
        self.image_cat5 = self.image_image_cat5
        self.image_cat6 = self.image_image_cat6
        self.button_image_compare2 = self.button_image_compare2
        self.button_image_hover_compare2 = self.button_image_hover_compare2
        self.button_image_back = self.button_image_back

        self.text_length = tk.DoubleVar(value=0.6)

        length_label = Label(self, text="Text Length:", font=("Century Gothic", 12), bg="#F7F8BB")
        length_label.place(x=750, y=160)

        length_options = [
            ("Very Small", 0.3),
            ("Small", 0.4),
            ("Normal", 0.6),
            ("Medium", 0.8),
            ("Long", 1.0),
        ]

        y_offset = 190
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
            radio.place(x=750, y=y_offset)
            y_offset += 25

        self.text_speed = tk.IntVar(value=15)

        speed_label = Label(self, text="Text Speed:", font=("Century Gothic", 12), bg="#F7F8BB")
        speed_label.place(x=750, y=340)

        speed_options = [
            ("Slow", 30),
            ("Normal", 15),
            ("Fast", 5),
            ("Instant", 1),
        ]

        y_offset = 370
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
            radio.place(x=750, y=y_offset)
            y_offset += 25

    def breed_select(self, event, frame, listbox, selected_list):
        selected_index = listbox.curselection()
        if selected_index:
            selected_race = listbox.get(selected_index)
            selected_list.clear()
            selected_list.append(selected_race)
            print(f"Selected breed: {selected_race}")

            frame.place_forget()

            small_frame = Frame(self, bg="#26b99a", width=200, height=50, highlightbackground="black", highlightthickness=1)
            small_frame.place(x=frame.winfo_x(), y=frame.winfo_y() + 125)

            text_button_frame = Frame(small_frame, bg="#26b99a")
            text_button_frame.pack(expand=True, fill="both", padx=10, pady=5)

            label = Label(text_button_frame, text=selected_race, font=("Century Gothic", 14), bg="#26b99a")
            label.pack(side="left", padx=5)

            back_image = PhotoImage(file=relative_to_assets("arrow.png"))

            back_button = tk.Button(
                text_button_frame,
                image=back_image,
                borderwidth=0,
                highlightthickness=0,
                command=lambda: self.go_back(small_frame, frame),
                bg="#E0E0E0",
                activebackground="#F5F5F5"
            )
            back_button.image = back_image
            back_button.pack(side="right", padx=5)

    def go_back(self, small_frame, frame):
        small_frame.place_forget()
        frame.place(x=frame.winfo_x(), y=frame.winfo_y())

    def compare_races(self):
        if self.selected_races1 and self.selected_races2:
            race1 = self.selected_races1[0]
            race2 = self.selected_races2[0]

            length_factor = self.text_length.get()

            self.entry_compare.delete("1.0", "end")

            text = generate_cats_comparison(race1, race2, length_factor)

            self.display_text_gradually(text)
        else:
            self.entry_compare.delete("1.0", "end")
            self.display_text_gradually("Select a breed from each list to compare.")

    def display_text_gradually(self, text, index=0):
        if index < len(text):
            current_text = self.entry_compare.get("1.0", "end-1c")
            self.entry_compare.delete("1.0", "end")
            self.entry_compare.insert("1.0", current_text + text[index])
            self.entry_compare.see("end")
            self.after(self.text_speed.get(), self.display_text_gradually, text, index + 1)
