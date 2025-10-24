from typing import List

import customtkinter as ctk

from ui.get_resource_path import resource_path
from ui.ui_logger import LoggingButton
from utils.warnings import Warning


class WarningsWindow(ctk.CTkToplevel):
    """Popup window to display all warnings in a table format"""

    def __init__(
        self, parent, warnings: List[Warning], frame_color: str, label_color: str
    ):
        super().__init__(parent)
        self.title("Autosa Warnings")
        self.logo = resource_path("images/alert.ico")
        self.after(200, lambda: self.iconbitmap(self.logo))
        self.transient(parent)
        self.window_width = 1000
        self.window_height = 400
        self.geometry(f"{self.window_width}x{self.window_height}")
        self.resizable(True, True)

        self.frame_color = frame_color
        self.label_color = label_color
        self.warnings = warnings

        self.create_widgets()

    def create_widgets(self):
        """Create the table with warnings"""
        # Main frame
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Header
        header_label = ctk.CTkLabel(
            main_frame,
            text="Autosa Warnings",
            font=("Arial", 16, "bold"),
            fg_color=self.label_color,
        )
        header_label.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Create table frame
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.columnconfigure(1, weight=0, minsize=80)
        table_frame.columnconfigure(2, weight=2)

        # Table headers
        headers = ["Message", "Severity", "Recommended Action"]
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                fg_color=self.label_color,
            )
            header_label.grid(row=0, column=col, sticky="ew", padx=2, pady=2)

        # Display warnings sorted by severity (highest first)
        severity_order = {"High": 3, "Medium": 2, "Low": 1}
        sorted_warnings = sorted(
            self.warnings, key=lambda w: severity_order[w.severity.value], reverse=True
        )

        for i, warning in enumerate(sorted_warnings):
            row = i + 1

            # Message column
            message_label = ctk.CTkLabel(
                table_frame,
                text=warning.message,
                font=("Arial", 10),
                justify="left",
                anchor="w",
                wraplength=300,  # Wrap text at 300 pixels
            )
            message_label.grid(row=row, column=0, sticky="ew", padx=2, pady=2)

            # Severity column
            severity_label = ctk.CTkLabel(
                table_frame,
                text=warning.get_severity_text(),
                font=("Arial", 10),
            )
            severity_label.grid(row=row, column=1, sticky="ew", padx=2, pady=2)

            # Recommended action column
            action_text = (
                warning.recommended_action if warning.recommended_action else ""
            )
            action_label = ctk.CTkLabel(
                table_frame,
                text=action_text,
                font=("Arial", 10),
                justify="left",
                anchor="w",
                wraplength=400,  # Wrap text at 400 pixels
            )
            action_label.grid(row=row, column=2, sticky="ew", padx=2, pady=2)

        # Close button
        close_button = LoggingButton(self, text="Close", command=self.destroy)
        close_button.pack(pady=10)
