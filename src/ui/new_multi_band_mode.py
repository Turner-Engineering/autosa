import customtkinter as ctk


def confirm_run(window, range_var, run_progress, prog_amt, header_frame):
    """Creates and opens a new window to confirm the run."""
    run_window = ctk.CTkToplevel(window)
    run_window.title("Confirm Runs")
    run_window.iconbitmap("images/autosa_logo.ico")

    selected_range = range_var.get()

    # variable to hold number of run
    run_num = (
        5
        if selected_range == "B0 - B4 (monopole)"
        else 3 if selected_range == "B5 - B7 (bilogical)" else 8
    )

    # TODO fix this call
    # run_note = get_run_note(header_frame).get("1.0", "end-1c")

    confirm_label = ctk.CTkLabel(
        run_window,
        text=(
            "Please confirm that you would like to run bands\n"
            f"{selected_range} ({run_num} runs total)\n"
            "and that the first filename should be:\n"
            f"mdd [run note] B#\n"
            "(the rest will be numbered sequentially)"
        ),
    )
    confirm_label.grid(row=0, column=0, padx=10, pady=10)

    button_frame = ctk.CTkFrame(run_window)
    button_frame.grid(row=1, column=0, padx=20, pady=20)

    ok_button = ctk.CTkButton(
        button_frame,
        text="Ok",
        command=lambda: measure_progress_bar(run_progress, prog_amt),
    )
    ok_button.grid(row=0, column=0, padx=10, pady=10)
    # TODO "ok_button" - should close window after hitting ok

    cancel_button = ctk.CTkButton(
        button_frame, text="Cancel", command=lambda: run_window.destroy
    )
    cancel_button.grid(row=0, column=1, padx=10, pady=10)
    # TODO - should close window after hitting ok


def measure_progress_bar(run_progress, prog_amt):
    """presents the progress bar of runs"""
    run_progress.start()
    if (int(run_progress.get() * 100)) == 100:
        run_progress.stop()
    prog_amt.configure(text=(int(run_progress.get() * 100)))
    # TODO should stop at the end.


def orient_callback(range_var, orientation_range):
    """disables and enables the orientation based on the selected range"""
    selected_range = range_var.get()
    (
        orientation_range.configure(state="disabled")
        if selected_range != "B5 - B7 (bilogical)"
        else orientation_range.configure(state="normal")
    )


def get_run_note(header_frame):
    """get the run note to call when text is needed."""
    run_note_text = ctk.CTkEntry(header_frame, placeholder_text="[run note]")
    run_note_text.grid(row=0, column=1, padx=5, pady=5, sticky="E")

    return run_note_text


def get_multi_band_layout(multi_tab, window):
    """creates and sets up the multiband mode"""
    multi_tab.columnconfigure(0, weight=1)

    # FRAME 1: header and run note
    header_frame = ctk.CTkFrame(multi_tab, fg_color="yellow")
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

    get_run_note(header_frame)

    # FRAME 2:
    dropdown_frame = ctk.CTkFrame(multi_tab, fg_color="orange")
    dropdown_frame.grid(row=1, column=0, padx=10, pady=10, sticky="W")

    #   Orientation:
    orient_range_label = ctk.CTkLabel(dropdown_frame, text="Orientation: ")
    orient_range_label.grid(row=1, column=0, padx=5, pady=5)

    orient_range = ctk.CTkOptionMenu(dropdown_frame, values=["Horizontal", "Vertical"])
    # disable orientation for b0-b4 range
    orient_range.grid(row=1, column=1, padx=2, pady=2, sticky="EW")

    #   Band Range:
    band_range_label = ctk.CTkLabel(dropdown_frame, text="Band Range: ")
    band_range_label.grid(row=0, column=0, padx=5, pady=5)

    range_var = ctk.StringVar(value="B5 - B7 (bilogical")
    range_menu = ctk.CTkOptionMenu(
        dropdown_frame,
        values=["B0 - B4 (monopole)", "B5 - B7 (bilogical)", "B0 - B7 (calibration)"],
        variable=range_var,
        command=lambda event: orient_callback(range_var, orient_range),
    )
    range_menu.grid(row=0, column=1, padx=2, pady=2)

    # FRAME 3:
    run_frame = ctk.CTkFrame(multi_tab, fg_color="orange")
    run_frame.grid(row=2, column=0, padx=10, pady=10, sticky="EW")
    run_frame.columnconfigure([0, 1], weight=1)
    run_frame.rowconfigure(0, weight=1)

    run_sweep = ctk.CTkButton(
        run_frame,
        text="Run Sweeps",
        command=lambda: confirm_run(
            window, range_var, progress_bar, prog_amt, header_frame
        ),
    )
    run_sweep.grid(row=0, column=0, padx=5, pady=5, sticky="W")

    cancel_sweep = ctk.CTkButton(
        run_frame, text="Cancel Sweep", command=lambda: progress_bar.stop()
    )
    cancel_sweep.grid(row=0, column=2, padx=5, pady=5, sticky="W")

    # FRAME 3.1: Prog bar
    prog_frame = ctk.CTkFrame(run_frame, fg_color="transparent")
    prog_frame.grid(row=0, column=1, padx=5, pady=5, sticky="E")

    progress_bar = ctk.CTkProgressBar(prog_frame, orientation="horizontal")
    progress_bar.set(0)  # start at 0
    progress_bar.grid(row=0, column=1, padx=5, pady=5, sticky="E")

    prog_amt = ctk.CTkLabel(prog_frame, text="num")
    prog_amt.grid(row=0, column=2, padx=10, pady=5, sticky="W")
