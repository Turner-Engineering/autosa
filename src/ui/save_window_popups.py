import customtkinter as ctk
from instrument.instrument import get_run_filename
from ui.get_resource_path import resource_path
import datetime


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
        inst,
        autosa_logger,
        discon_btn_st,
        frame_color,
        label_color,
        run_filename,
        run_id,
        sweep_dur,
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

        self.inst = inst
        self.autosa_logger = autosa_logger
        self.discon_btn_st = discon_btn_st
        self.run_filename = run_filename
        self.run_id = run_id
        self.sweep_dur = int(sweep_dur)

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
        frame1.columnconfigure([0, 1, 2, 3, 4, 5], weight=0)
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
        ctk.CTkLabel(frame1, text="Run ID:", width=50).grid(
            row=0, column=0, padx=5, sticky="w"
        )

        run_id_label = ctk.CTkLabel(frame1, text=self.run_id, width=50)
        run_id_label.grid(row=1, column=0, padx=5, sticky="w")

        # Run Note
        ctk.CTkLabel(frame1, text="Run Note:").grid(row=0, column=1, padx=5, sticky="w")

        self.run_note_entry = ctk.CTkEntry(
            frame1, textvariable=self.run_note_var, width=250
        )
        self.run_note_entry.grid(row=1, column=1, padx=5, sticky="w")

        # Sweep Duration
        ctk.CTkLabel(frame1, text="Sweep Dur", width=50).grid(
            row=0, column=2, padx=5, sticky="w"
        )
        self.sweep_dur_label = ctk.CTkLabel(frame1, text=f"{self.sweep_dur}s", width=50)
        self.sweep_dur_label.grid(row=1, column=2, padx=5, sticky="w")

        # Band
        ctk.CTkLabel(frame1, text="Band:", width=40).grid(
            row=0, column=3, padx=2, sticky="w"
        )

        self.band_entry = ctk.CTkEntry(frame1, textvariable=self.band_var, width=40)
        self.band_entry.grid(row=1, column=3, padx=2, sticky="w")

        # Time
        ctk.CTkLabel(frame1, text="Time:", width=50).grid(
            row=0, column=4, padx=5, sticky="w"
        )

        cur_time = datetime.datetime.now().strftime("%H_%M_%S")
        self.cur_time_label = ctk.CTkLabel(frame1, text=cur_time, width=50)
        self.cur_time_label.grid(row=1, column=4, padx=5, sticky="w")

        # Extension
        ctk.CTkLabel(frame1, text="Extension:", width=75).grid(
            row=0, column=5, padx=2, sticky="w"
        )

        extnsn_label = ctk.CTkLabel(frame1, text=".csv/.png", width=75)
        extnsn_label.grid(row=1, column=5, padx=2, sticky="w")

    def fill_frame2(self, frame2):
        """second frame is the trace/screen filename"""
        # Filename
        ctk.CTkLabel(frame2, text="Trace Filename:").grid(
            row=0, column=0, padx=5, sticky="w"
        )

        trace_label = ctk.CTkLabel(frame2, textvariable=self.trace_file_var)
        trace_label.grid(row=0, column=1, padx=5, sticky="w")

        ctk.CTkLabel(frame2, text="Screen Filename:").grid(
            row=1, column=0, padx=5, sticky="w"
        )

        screen_label = ctk.CTkLabel(frame2, textvariable=self.screen_file_var)
        screen_label.grid(row=1, column=1, padx=5, sticky="w")

    def fill_frame3(self, frame3):
        """third frame is the save/cancel button"""
        # Save/Cancel
        save_button = ctk.CTkButton(
            frame3,
            text="Save",
            state=self.discon_btn_st,
            command=lambda: self.save_run(self.run_note_entry, self.band_entry),
        )
        save_button.grid(row=0, column=2, padx=5, sticky="w")

        cancel_button = ctk.CTkButton(
            frame3, text="Cancel", command=lambda: self.cancel_save()
        )
        cancel_button.grid(row=0, column=3, padx=5, sticky="w")

    def trace_screen_filename(self, *args):
        run_note = self.run_note_var.get()
        band = self.band_var.get()
        # filename = get_run_filename(self.run_id, run_note, band)
        filename = get_run_filename(self.inst, band, run_note, self.sweep_dur)

        self.trace_file_var.set(f"{filename}.csv")
        self.screen_file_var.set(f"{filename}.png")

    def save_run(self, run_note_entry, band_entry):
        run_note = run_note_entry.get().strip()
        band = band_entry.get().strip()

        if (run_note == "") or (band == ""):
            self.autosa_logger.error("Manual Mode: Entry fields were empty.")
            self.lower()
            PopupWindow(self)
        else:
            self.run_filename = get_run_filename(
                self.inst, band, run_note, self.sweep_dur
            )
            self.destroy()

    def get_filename(self):
        return self.run_filename

    def get_band(self):
        return self.band_var.get().strip()

    def cancel_save(self):
        self.autosa_logger.warning("Manual Mode: Save canceled.")
        self.destroy()
