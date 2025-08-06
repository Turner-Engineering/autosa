import customtkinter as ctk

from utils.logger import autosa_logger


### INTEGRATING LOGGING WITH CTK
class LoggingTopLevel(ctk.CTkToplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.window_name = kwargs.pop("window_name", self.__class__.__name__)
        autosa_logger.info(f'[WINDOW] "{self.window_name}" opened.')

    def destroy(self):
        autosa_logger.info(f'[WINDOW] "{self.window_name}" closed.')
        super().destroy()


class LoggingButton(ctk.CTkButton):
    def __init__(self, parent, *args, **kwargs):
        self.log_label = kwargs.pop("log_label", None)  # buttons without text
        # TODO: is there a way to remind to put label
        super().__init__(parent, *args, **kwargs)

        button_cmd = kwargs.get("command", lambda: None)

        def on_click():
            button_text = self.cget("text")

            # check if log_label first, then text
            if self.log_label:
                button_name = self.log_label
            elif button_text and button_text.isascii():
                button_name = button_text
            else:
                button_name = "Unlabeled"
            # if no label or no text, button name is "Unknown"

            autosa_logger.info(f'[BUTTON] User clicked "{button_name}" button.')
            button_cmd()

        self.configure(command=on_click)


### VISUAL CUSTOMIZING TO LOGGING WITH CTK
class ArrowButton(LoggingButton):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(
            parent,
            *args,
            **kwargs,
        )
        self.configure(
            height=30, width=30, font=("", 16), text_color="black", anchor="center"
        )


class LargeButton(LoggingButton):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(
            parent,
            *args,
            **kwargs,
        )
        self.configure(height=60, font=("", 18))


class OutlineButton(LoggingButton):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(
            parent,
            *args,
            **kwargs,
        )
        self.configure(
            # text_color="#0F3A5D",
            text_color="#1C4363",
            border_width=1,
            border_color="#3B8ED0",
            fg_color="transparent",
            bg_color="transparent",
        )
