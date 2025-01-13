import tkinter as tk
from mewsmatch import MewsMatchPage
from choose_feature import ChooseFeaturePage
from identify_breed import IdentifyBreedPage
from describe_breed import DescribeBreedPage
from compare_breed import CompareBreedPage


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Catology App")
        self.root.geometry("960x735")

        self.container = tk.Frame(self.root)
        self.container.pack(expand=True, fill="both")

        self.pages = {}
        self.add_page("mewsmatch", MewsMatchPage(self.container, self))
        self.add_page("choosefeature", ChooseFeaturePage(self.container, self))
        self.add_page("identifybreed", IdentifyBreedPage(self.container, self))
        self.add_page("describebreed", DescribeBreedPage(self.container, self))
        self.add_page("comparebreed", CompareBreedPage(self.container, self))


        self.show_page("mewsmatch")

    def add_page(self, name, page):
        self.pages[name] = page

    def show_page(self, page_name):
        for page in self.pages.values():
            page.pack_forget()

        page = self.pages[page_name]
        page.pack(expand=True, fill="both")



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
