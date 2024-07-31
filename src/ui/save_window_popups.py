import customtkinter as ctk
from instrument.instrument import create_run_filename
from ui.get_resource_path import resource_path


class CompletedWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Completion Status")
        window_width = 350
        window_height = 150
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.transient(parent)

        self.create_widgets()

    def create_widgets(self):
        self.popup_window()

    def popup_window(self):
        ctk.CTkLabel(self, text="Run(s) Complete!").grid(
            row=0, column=0, padx=10, pady=10
        )
        ctk.CTkButton(self, text="Okay", command=lambda: self.destroy()).grid(
            row=1, column=0, padx=10, pady=10
        )


class PopupWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Invalid")
        window_width = 350
        window_height = 150
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.transient(parent)

        self.create_widgets()

    def create_widgets(self):
        self.popup_window()

    def popup_window(self):
        ctk.CTkLabel(self, text="Please enter a Run Note!").grid(
            row=0, column=0, padx=10, pady=10
        )
        ctk.CTkButton(self, text="Okay", command=lambda: self.destroy()).grid(
            row=1, column=0, padx=10, pady=10
        )


class ManualSaveWindow(ctk.CTkToplevel):
    """opens a new window and sets it up for settings"""

    def __init__(
        self,
        parent,
        run_filename,
        inst,
        run_id,
        frame_color,
        label_color,
    ):
        super().__init__(parent)
        self.title("Save Trace and Screen")
        window_width = 900
        window_height = 250
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.transient(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure([0, 1, 2], weight=1)

        self.frame_color = frame_color
        self.label_color = label_color

        self.run_filename = run_filename
        self.inst = inst
        self.run_id = run_id

        self.run_note_var = ctk.StringVar()
        self.band_var = ctk.StringVar()
        self.trace_file_var = ctk.StringVar()
        self.screen_file_var = ctk.StringVar()
        self.run_note_var.trace_add("write", self.trace_screen_filename)
        self.band_var.trace_add("write", self.trace_screen_filename)

        self.create_widgets()

    def create_widgets(self):
        frame1 = self.init_frame1()
        frame2 = self.init_frame2()
        frame3 = self.init_frame3()

        self.fill_frame1(frame1)
        self.fill_frame2(frame2)
        self.fill_frame3(frame3)

    def init_frame1(self):
        frame1 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame1.grid(row=0, column=0, padx=2, sticky="ew")
        frame1.columnconfigure([0, 1, 2, 3], weight=1)
        return frame1

    def init_frame2(self):
        frame2 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame2.grid(row=1, column=0, padx=2, sticky="ew")
        frame2.columnconfigure([0, 1], weight=0)
        return frame2

    def init_frame3(self):
        frame3 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame3.grid(row=2, column=0, padx=2, sticky="ew")
        frame3.columnconfigure([0, 1], weight=1)
        return frame3

    def fill_frame1(self, frame1):
        """first frame is the run id info"""
        # Run ID
        ctk.CTkLabel(frame1, text="Run ID:", width=75).grid(
            row=0, column=0, padx=5, sticky="W"
        )

        run_id_label = ctk.CTkLabel(frame1, text=self.run_id, width=75)
        run_id_label.grid(row=1, column=0, padx=5, sticky="W")

        # Run Note
        ctk.CTkLabel(frame1, text="Run Note:").grid(row=0, column=1, padx=5, sticky="W")

        self.run_note_entry = ctk.CTkEntry(
            frame1, textvariable=self.run_note_var, width=250
        )
        self.run_note_entry.grid(row=1, column=1, padx=5, sticky="W")

        # Band
        ctk.CTkLabel(frame1, text="Band:", width=50).grid(
            row=0, column=2, padx=2, sticky="W"
        )

        self.band_entry = ctk.CTkEntry(frame1, textvariable=self.band_var, width=50)
        self.band_entry.grid(row=1, column=2, padx=2, sticky="W")

        # Extension
        ctk.CTkLabel(frame1, text="Extension:", width=75).grid(
            row=0, column=3, padx=2, sticky="W"
        )

        extnsn_label = ctk.CTkLabel(frame1, text=".csv/.png", width=75)
        extnsn_label.grid(row=1, column=3, padx=2, sticky="W")

    def fill_frame2(self, frame2):
        """second frame is the trace/screen filename"""
        # Filename
        ctk.CTkLabel(frame2, text="Trace Filename:").grid(
            row=0, column=0, padx=5, sticky="W"
        )

        trace_label = ctk.CTkLabel(frame2, textvariable=self.trace_file_var)
        trace_label.grid(row=0, column=1, padx=5, sticky="W")

        ctk.CTkLabel(frame2, text="Screen Filename:").grid(
            row=1, column=0, padx=5, sticky="W"
        )

        screen_label = ctk.CTkLabel(frame2, textvariable=self.screen_file_var)
        screen_label.grid(row=1, column=1, padx=5, sticky="W")

    def fill_frame3(self, frame3):
        """third frame is the save/cancel button"""
        # Save/Cancel
        save_button = ctk.CTkButton(
            frame3,
            text="Save",
            command=lambda: self.save_run(self.run_note_entry, self.band_entry),
        )
        save_button.grid(row=0, column=2, padx=5, sticky="W")

        cancel_button = ctk.CTkButton(
            frame3, text="Cancel", command=lambda: self.destroy()
        )
        cancel_button.grid(row=0, column=3, padx=5, sticky="W")

    def trace_screen_filename(self, *args):
        run_note = self.run_note_var.get()
        band = self.band_var.get()
        filename = create_run_filename(self.run_id, run_note, band)

        self.trace_file_var.set(f"{filename}.csv")
        self.screen_file_var.set(f"{filename}.png")

    def save_run(self, run_note_entry, band_entry):
        run_note = run_note_entry.get().strip()
        band = band_entry.get().strip()

        if (run_note == "") or (band == ""):
            self.lower()
            PopupWindow(self)
        else:
            self.run_filename = create_run_filename(self.run_id, run_note, band)
            self.destroy()

    def get_filename(self):
        return self.run_filename
