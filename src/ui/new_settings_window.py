import customtkinter as ctk


def get_folder_frame(settings_window):
    """creates and sets up the frame for the folders"""
    folder_frame = ctk.CTkFrame(settings_window, fg_color="pink")
    folder_frame.grid(row=1, column=0, sticky="EW")
    folder_frame.rowconfigure([0, 1, 2, 3, 4], weight=1)

    frame_header1 = ctk.CTkLabel(folder_frame, text="Folders", justify="left")
    frame_header1.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    folder_texts = [
        ("State Files Folder:", "D:/Users/Instrument/Desktop/State Files"),
        ("Correction Files Folder:", "D:/Users/Instrument/Desktop/Correction Files"),
        ("Instrument Output Folder:", "D:/Users/Instrument/Desktop/Test Data"),
        ("Local Output Folder:", ""),
    ]

    for i, (folder_labels, folder_paths) in enumerate(folder_texts, start=1):
        folder_label = ctk.CTkLabel(folder_frame, text=folder_labels, justify="left")
        folder_label.grid(row=i, column=0, padx=10, pady=2, sticky="W")

        folder_path = ctk.CTkTextbox(folder_frame, width=500, height=10)
        folder_path.insert("0.0", folder_paths)
        folder_path.grid(row=i, column=2, padx=10, pady=2, sticky="EW")

    browse_button = ctk.CTkButton(folder_frame, text="Browse")
    browse_button.grid(row=4, column=3, padx=10, pady=2, sticky="W")


def get_other_frame(settings_window):
    """creates and sets up the frame with the sweep duration and run note"""
    other_frame = ctk.CTkFrame(settings_window, fg_color="orange")
    other_frame.grid(row=2, column=0, sticky="EW")
    # other_frame.rowconfigure([0, 1, 2, 3, 4], weight=1)
    # other_frame.columnconfigure([0, 1], weight=1)

    frame_header2 = ctk.CTkLabel(other_frame, text="Other", justify="left")
    frame_header2.grid(row=0, column=0, padx=10, pady=2, sticky="W")

    sweep_dur_label = ctk.CTkLabel(
        other_frame, text="Sweep Duration(s):", justify="left"
    )
    sweep_dur_label.grid(row=1, column=0, padx=10, pady=2, sticky="W")

    sweep_dur_text = ctk.CTkTextbox(other_frame, width=50, height=10)
    sweep_dur_text.insert("0.0", "5")
    sweep_dur_text.grid(row=1, column=1, padx=10, pady=2, sticky="EW")

    run_note_text = ctk.CTkLabel(
        other_frame,
        text=(
            "The run note is the text placed after the run id and band name in filename.\n"
            'Files will be saved as "808-13 B3 [run note].csv" and "808-13 B3 [run note].png"\n'
            "This can be used for location, test type, or any other information."
        ),
        justify="left",
    )
    run_note_text.grid(row=2, column=0, padx=10, pady=2, sticky="W", columnspan=2)


def get_button_frame(settings_window):
    """Creates the save and cancel buttons"""
    button_frame = ctk.CTkFrame(settings_window, fg_color="blue")
    button_frame.grid(row=3, column=0, sticky="EW")

    save_button = ctk.CTkButton(
        button_frame, text="Save", command=lambda: print("SAVED!")
    )
    save_button.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    cancel_button = ctk.CTkButton(
        button_frame, text="Cancel", command=lambda: settings_window.destroy
    )
    cancel_button.grid(row=0, column=1, padx=10, pady=10, sticky="W")


def get_settings_window(window):
    """opens a new window and sets it up for settings"""
    settings_window = ctk.CTkToplevel(window)
    settings_window.title("Settings")
    settings_window.iconbitmap("images/autosa_logo.ico")
    settings_window.columnconfigure(0, weight=1)
    settings_window.rowconfigure([0, 1, 2, 3], weight=1)

    # title frame
    settings_header = ctk.CTkLabel(settings_window, text="Settings", justify="left")
    settings_header.grid(row=0, column=0, padx=5, pady=5, sticky="W")

    # Folder Frame
    get_folder_frame(settings_window)

    # Other Frame
    get_other_frame(settings_window)

    # Button frame
    get_button_frame(settings_window)
