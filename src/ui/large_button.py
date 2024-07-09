import customtkinter as ctk


class LargeButton(ctk.CTkButton):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(
            parent,
            *args,
            **kwargs,
        )
        self.configure(height=60, font=("", 18))
