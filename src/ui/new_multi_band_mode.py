import json, os
import customtkinter as ctk
import datetime
from ui.new_utils import read_settings_from_file


DATE = datetime.date.today()


def orient_callback(range_var, orientation_range):
    """disables and enables the orientation based on the selected range"""
    selected_range = range_var.get()
    (
        orientation_range.configure(state="disabled")
        if selected_range != "B5 - B7 (bilogical)"
        else orientation_range.configure(state="normal")
    )


# def measure_prog_bar(run_window, prog_bar, prog_amt, run_num):
#     """presents the progress bar of runs"""
# prog_bar.start()
# if (int(prog_bar.get() * 100)) == 100:
#     prog_bar.stop()
# prog_amt.configure(text=(int(prog_bar.get() * 100)))
# times_run = 0
# is_started = False

# if is_started == False:
#     prog_bar.start()
#     is_started = True

# if times_run < run_num:
#     prog_fract = int(times_run / run_num)
#     prog_bar.set(prog_fract)
#     prog_amt.configure(text=(int(prog_bar.get() * 100)))
#     times_run += 1
#     print(times_run)
# else:
#     print("COMPLETE!")
# run_window.destroy()


# def confirm_run(self, range_var, prog_bar, prog_amt, run_note_entry):
#     """Creates and opens a new window to confirm the run."""
#     run_window = ctk.CTkToplevel(self)
#     run_window.title("Confirm Runs")
#     run_window.iconbitmap("images/autosa_logo.ico")

#     rng_choice = range_var.get()
#     run_note = run_note_entry.get()

#     # file_path = os.path.join(os.getenv("LOCALAPPDATA"), "Autosa", "settings.json")
#     with open(FILE_PATH, "r") as reader:
#         data = json.load(reader)
#         sweep_dur = data[4][
#             "input"
#         ]  # TODO no 4, make key that can be actualy accessible

#     # variable to hold number of run
#     run_num = (
#         5
#         if rng_choice == "B0 - B4 (monopole)"
#         else 3 if rng_choice == "B5 - B7 (bilogical)" else 8
#     )

#     ctk.CTkLabel(
#         run_window,
#         text=(
#             "Please confirm that you would like to run bands\n"
#             f"{rng_choice} ({run_num} runs total)\n"
#             f"for {sweep_dur} seconds each\n"
#             "and that the first filename should be:\n"
#             f"mdd {run_note} B#\n"
#             "(the rest will be numbered sequentially)"
#         ),
#     ).grid(row=0, column=0, padx=10, pady=10)

#     button_frm = ctk.CTkFrame(run_window)
#     button_frm.grid(row=1, column=0, padx=20, pady=20)

#     ctk.CTkButton(
#         button_frm,
#         text="Ok",
#         command=lambda: measure_prog_bar(run_window, prog_bar, prog_amt, run_num),
#     ).grid(row=0, column=0, padx=10, pady=10)
#     # TODO "ok_button" - should close window after hitting ok


#     ctk.CTkButton(button_frm, text="Cancel", command=lambda: run_window.destroy()).grid(
#         row=0, column=1, padx=10, pady=10
#     )


class ConfirmWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Confirm Runs")
        window_width = 600
        window_height = 275
        self.geometry(f"{window_width}x{window_height}")
        self.iconbitmap("images/autosa_logo.ico")
        self.columnconfigure(0, weight=1)

        # vars:
        band_range = parent.band_range_var.get()
        run_note = parent.run_note_var.get()

        self.create_widgets(band_range, run_note)

    def create_widgets(self, band_range, run_note):
        self.confirm_run(band_range, run_note)

    def confirm_run(self, band_range, run_note):
        # format the date
        year = str(DATE.year)[-2:]  # don't need to abbreviate four letters
        local_date = f"{DATE.month}{DATE.day:02}-{year}"

        settings = read_settings_from_file()

        for keys in settings:
            if "Sweep Duration" in keys:
                sweep_dur = settings["Sweep Duration:"]

        run_num = (
            5
            if band_range == "B0 - B4 (monopole)"
            else 3 if band_range == "B5 - B7 (bilogical)" else 8
        )

        confirm_label = ctk.CTkLabel(
            self,
            text=(
                "Please confirm that you would like to run bands\n"
                f"{band_range} ({run_num} runs total)\n"
                f"for {sweep_dur} seconds each\n"
                "and that the first filename should be:\n"
                f"{local_date} {run_note} B0\n"
                "(the rest will be numbered sequentially)"
            ),
        )
        confirm_label.grid(row=0, column=0, padx=10, pady=10)

        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=1, column=0, padx=10, pady=10)

        okay_button = ctk.CTkButton(
            button_frame,
            text="Okay",
            # command=lambda: measure_prog_bar(self, prog_bar, prog_amt, run_num),
            command=lambda: self.measure_prog_bar(),
        )
        okay_button.grid(row=0, column=0, padx=10, pady=10)

        cancel_button = ctk.CTkButton(
            button_frame, text="Cancel", command=lambda: self.destroy()
        )
        cancel_button.grid(row=0, column=1, padx=10, pady=10)

    def measure_prog_bar(self):
        """presents the progress bar of runs"""
        self.destroy()  # close confirm window

        for i in range(5):
            print("CALL TO PROGRESS BAR")

        self.destroy()  # close window


class MultiModeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.configure(border_width=2)
        self.band_range_var = ctk.StringVar(value="B5 - B7 (bilogical")
        self.run_note_var = ctk.StringVar(value="[run note]")
        self.create_widgets()

    def create_widgets(self):
        # FRAME 1: header and run note
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="EW")
        header_frame.columnconfigure([0, 1], weight=1)

        tab3_label = ctk.CTkLabel(
            header_frame,
            text=(
                "Multi Band Mode allows you to run multiple bands in a row with no intervention.\n"
                "State files, correction files, and file names are set automatically."
            ),
            justify="left",
            anchor="w",
        )
        tab3_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        # get_run_note(header_frame)
        run_note_entry = ctk.CTkEntry(header_frame, textvariable=self.run_note_var)
        run_note_entry.grid(row=0, column=1, padx=5, pady=5, sticky="E")

        # FRAME 2:
        dropdown_frame = ctk.CTkFrame(self, fg_color="transparent")
        dropdown_frame.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        #   Orientation:
        orient_range_label = ctk.CTkLabel(dropdown_frame, text="Orientation: ")
        orient_range_label.grid(row=1, column=0, padx=5, pady=5)

        # subjective again, but "orient" as an abbreviation for orientation has the issue of also being a verb
        # "orient_range" could also mean a function that is orienting something
        # ori is shorter and doesn't have that issue
        ori_dropdown = ctk.CTkOptionMenu(
            dropdown_frame, values=["Horizontal", "Vertical"]
        )
        ori_dropdown.grid(row=1, column=1, padx=2, pady=2, sticky="EW")

        #   Band Range:
        band_range_label = ctk.CTkLabel(dropdown_frame, text="Band Range: ")
        band_range_label.grid(row=0, column=0, padx=5, pady=5)

        band_ranges = [
            "B0 - B4 (monopole)",
            "B5 - B7 (bilogical)",
            "B0 - B7 (calibration)",
        ]

        band_range_dropdown = ctk.CTkOptionMenu(
            dropdown_frame,
            values=band_ranges,
            variable=self.band_range_var,
            command=lambda event: orient_callback(self.band_range_var, ori_dropdown),
        )
        band_range_dropdown.grid(row=0, column=1, padx=2, pady=2)

        # FRAME 3:
        run_frame = ctk.CTkFrame(self, fg_color="transparent")
        run_frame.grid(row=2, column=0, padx=10, pady=10, sticky="EW")
        run_frame.columnconfigure([0, 1], weight=1)
        run_frame.rowconfigure(0, weight=1)

        run_sweeps_button = ctk.CTkButton(
            run_frame,
            text="Run Sweeps",
            # command=lambda: confirm_run(
            #     self, range_var, progress_bar, prog_amt, run_note_entry
            # ),
            command=lambda: self.open_confirm_window(),
        )
        run_sweeps_button.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        progress_bar = ctk.CTkProgressBar(run_frame)
        progress_bar.set(0)  # start at 0
        progress_bar.grid(row=0, column=2, padx=5, pady=5, sticky="E", columnspan=2)

        prog_amt = ctk.CTkLabel(run_frame, text="num")
        prog_amt.grid(row=0, column=4, padx=10, pady=5, sticky="W")

        cancel_button = ctk.CTkButton(
            run_frame, text="Cancel Sweep", command=lambda: progress_bar.stop()
        )
        cancel_button.grid(row=0, column=5, padx=5, pady=5, sticky="W")

    # the main purpose here is to run the sweeps, not check settings
    def open_confirm_window(self):
        ConfirmWindow(self)

    # def measure_prog_bar(self):
    #     """presents the progress bar of runs"""
    #     self.destroy()  # close confirm window
    #     is_started = False

    # if false,
    # if is_started:
    #     is_started = True
    # else:
    #     for i in range(5):
    #         print("CALL TO PROGRESS BAR")

    # if is_started == False:
    #     MultiModeFrame.prog_bar.start()
    #     is_started = True
    # MultiModeFrame.progress_bar.start()


# prog_bar.start()
# if (int(prog_bar.get() * 100)) == 100:
#     prog_bar.stop()
# prog_amt.configure(text=(int(prog_bar.get() * 100)))
# times_run = 0
# is_started = False

# if is_started == False:
#     prog_bar.start()
#     is_started = True

# if times_run < run_num:
#     prog_fract = int(times_run / run_num)
#     prog_bar.set(prog_fract)
#     prog_amt.configure(text=(int(prog_bar.get() * 100)))
#     times_run += 1
#     print(times_run)
# else:
#     print("COMPLETE!")
# run_window.destroy()

# TODO Left off : working on progress bar
# MultiModeFrame.progress_bar.start()
