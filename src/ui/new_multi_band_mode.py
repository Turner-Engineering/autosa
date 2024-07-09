import customtkinter as ctk

from ui.new_utils import read_settings_from_file


class ConfirmWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Confirm Runs")
        self.parent = parent
        self.iconbitmap("images/autosa_logo.ico")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.resizable(False, False)  # disable resizing
        self.attributes("-topmost", True)  # always on top
        self.center()  # center on screen, otherwise it will be in the top left corner
        self.create_widgets()

    def create_widgets(self):
        frame = self.init_frame()
        self.fill_frame(frame)

    def init_frame(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        return frame

    def fill_frame(self, frame):
        text = self.get_confirmation_text()

        # Confirmation Text
        ctk.CTkLabel(
            frame,
            text=text,
            justify="left",
        ).grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Okay Button
        ctk.CTkButton(
            frame,
            text="Okay",
            command=lambda: self.confirmation_callback(),
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cancel Button
        ctk.CTkButton(
            frame,
            text="Cancel",
            command=lambda: self.destroy(),
            fg_color="#939ba2",
            hover_color="#646a6e",
        ).grid(row=1, column=1, padx=5, pady=5, sticky="e")

    def get_confirmation_text(self):
        band_range = self.parent.band_range_var.get()
        run_count = self.get_run_count(band_range)
        run_note = self.parent.run_note_var.get()
        sweep_dur = read_settings_from_file()["sweep_dur"]
        run_id = "XYZ-AB"

        text = (
            "Please confirm that you would like to run bands\n"
            f"{band_range} ({run_count} runs total)\n"
            f"for {sweep_dur} seconds each\n"
            "and that the first filename should be:\n"
            f"{run_id} {run_note} B0\n"
            "(the rest will be numbered sequentially)"
        )
        return text

    def get_run_count(self, band_range):
        if band_range == "B0 - B4 (monopole)":
            run_count = 5
        elif band_range == "B5 - B7 (bilogical)":
            run_count = 3
        elif band_range == "B0 - B7 (calibration)":
            run_count = 8
        else:
            raise ValueError("Invalid band range")
        return run_count

    def confirmation_callback(self):
        print("STARTING MULTI BAND MODE SWEEPS...")
        self.destroy()  # close confirm window

    def center(self):
        # roughly center the popup
        x = self.winfo_screenwidth() // 2 - 200
        y = self.winfo_screenheight() // 2 - 300
        self.geometry("{}+{}".format(x, y))


class MultiModeFrame(ctk.CTkFrame):
    def __init__(self, parent, frame_color="transparent", label_color="transparent"):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.frame_color = frame_color
        self.label_color = label_color

        self.band_ranges = [
            "B0 - B4 (monopole)",
            "B5 - B7 (bilogical)",
            "B0 - B7 (calibration)",
        ]

        # Tkinter Variables
        self.band_range_var = ctk.StringVar(value=self.band_ranges[0])
        self.run_note_var = ctk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        frame1 = self.init_frame1()
        frame2 = self.init_frame2()

        self.fill_frame1(frame1)
        self.fill_frame2(frame2)

    def init_frame1(self):
        frame1 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame1.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        return frame1

    def init_frame2(self):
        frame2 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame2.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        frame2.columnconfigure([1], weight=1)
        frame2.rowconfigure(0, weight=1)
        return frame2

    def fill_frame1(self, frame1):
        # Run Note Label
        ctk.CTkLabel(
            frame1,
            text="Run Note: ",
            fg_color=self.label_color,
            width=80,
            anchor="w",
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Run Note Entry
        ctk.CTkEntry(
            frame1,
            textvariable=self.run_note_var,
            width=300,
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Band Range Label
        ctk.CTkLabel(
            frame1,
            text="Band Range: ",
            fg_color=self.label_color,
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Band Range Dropdown
        ctk.CTkOptionMenu(
            frame1,
            values=self.band_ranges,
            variable=self.band_range_var,
            command=lambda event: self.update_ori_dropdown(),
            width=180,
        ).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Orientation Label
        ctk.CTkLabel(
            frame1,
            text="Orientation: ",
            fg_color=self.label_color,
        ).grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Orientation Dropdown
        self.ori_dropdown = ctk.CTkOptionMenu(
            frame1,
            values=["Horizontal", "Vertical"],
            width=180,
        )
        self.ori_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.update_ori_dropdown()

    def fill_frame2(self, frame2):
        # Run Button
        ctk.CTkButton(
            frame2,
            text="Run Sweeps",
            command=lambda: ConfirmWindow(self),
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Progress Bar
        progress_bar = ctk.CTkProgressBar(frame2, height=15, corner_radius=0)
        progress_bar.set(0)  # start at 0
        progress_bar.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Progress Amount Label
        ctk.CTkLabel(
            frame2,
            text="0/5",
            fg_color=self.label_color,
        ).grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Cancel Button
        ctk.CTkButton(
            frame2,
            text="Cancel",
            command=lambda: progress_bar.stop(),
            fg_color="#939ba2",
            hover_color="#646a6e",
        ).grid(row=0, column=3, padx=5, pady=5, sticky="e")

    def update_ori_dropdown(self):
        """disables and enables the orientation based on the selected range"""
        band_range = self.band_range_var.get()
        if band_range == "B5 - B7 (bilogical)":
            self.ori_dropdown.configure(state="normal")
            self.ori_dropdown.set("Horizontal")
        else:
            self.ori_dropdown.configure(state="disabled")
            self.ori_dropdown.set("None")
