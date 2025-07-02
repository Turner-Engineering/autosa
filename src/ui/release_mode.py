import customtkinter as ctk
from PIL import Image
from ui.get_resource_path import resource_path

class ReleaseMode(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        inst_found,
        inst,
        frame_color="transparent",
        label_color="transparent",
    ):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.inst_found = inst_found
        self.inst = inst
        self.frame_color = frame_color
        self.label_color = label_color
        self.panel_img = resource_path("./images/N9010B_front_panel.png")

        self.create_widgets()

    def create_widgets(self):
        frame1 = self.init_frame1()
        self.fill_frame1(frame1)

    def init_frame1(self):
        frame1 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame1.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        frame1.columnconfigure(0, weight=1)
        return frame1

    def fill_frame1(self, frame1):
        ctk.CTkLabel(
            frame1,
            text="Instrument Released!\nYou can now control the instrument using the front panel.",
            fg_color=self.label_color,
            width=80,
            anchor="center",
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        panel_img = ctk.CTkImage(Image.open(self.panel_img), size=(600, 250))
        label_img = ctk.CTkLabel(self, text="", image=panel_img)
        label_img.grid(row=1, column=0, padx=5, pady=5, sticky="ew")