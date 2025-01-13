import tkinter as tk
from tkinter import PhotoImage
from pathlib import Path

# Definim calea către asset-uri
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class ChooseFeaturePage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        canvas = tk.Canvas(self, bg="#BB9ED6", height=735, width=960, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        # Butonul Identify
        button_image_identify = PhotoImage(file=relative_to_assets("button_identify.png"))
        button_identify = tk.Button(
            self,
            image=button_image_identify,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.app.show_page("identifybreed")  # Apelează metoda show_page cu numele paginii dorite
        )
        button_identify.place(x=345.0, y=77.0, width=294.0, height=93.0)

        button_image_hover_identify = PhotoImage(file=relative_to_assets("button_hover_identify.png"))

        def button_identify_hover(e):
            button_identify.config(image=button_image_hover_identify)

        def button_identify_leave(e):
            button_identify.config(image=button_image_identify)

        button_identify.bind('<Enter>', button_identify_hover)
        button_identify.bind('<Leave>', button_identify_leave)

        # Butonul Describe
        button_image_describe = PhotoImage(file=relative_to_assets("button_describe.png"))
        button_describe = tk.Button(
            self,
            image=button_image_describe,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.app.show_page("describebreed")  # Tranziție spre pagina Describe
        )
        button_describe.place(x=341.0, y=216.0, width=294.0, height=93.0)

        button_image_hover_describe = PhotoImage(file=relative_to_assets("button_hover_describe.png"))

        def button_describe_hover(e):
            button_describe.config(image=button_image_hover_describe)

        def button_describe_leave(e):
            button_describe.config(image=button_image_describe)

        button_describe.bind('<Enter>', button_describe_hover)
        button_describe.bind('<Leave>', button_describe_leave)

        # Butonul Compare
        button_image_compare = PhotoImage(file=relative_to_assets("button_compare.png"))
        button_compare = tk.Button(
            self,
            image=button_image_compare,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            command=lambda: self.app.show_page("comparebreed")  # Tranziție spre pagina Compare
        )
        button_compare.place(x=341.0, y=355.0, width=294.0, height=93.0)

        button_image_hover_compare = PhotoImage(file=relative_to_assets("button_hover_compare.png"))

        def button_compare_hover(e):
            button_compare.config(image=button_image_hover_compare)

        def button_compare_leave(e):
            button_compare.config(image=button_image_compare)

        button_compare.bind('<Enter>', button_compare_hover)
        button_compare.bind('<Leave>', button_compare_leave)

        self.image_backgroundd = PhotoImage(file=relative_to_assets("backgroundd.png"))
        canvas.create_image(480.0, 603.0, image=self.image_backgroundd)



