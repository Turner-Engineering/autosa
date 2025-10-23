from enum import Enum
from typing import List

from instrument.instrument import compare_datetime
from utils.logger import autosa_logger
from utils.settings import is_settings_valid, read_settings_from_file


class WarningSeverity(Enum):
    """Warning severity levels in order of priority (highest to lowest)"""

    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Warning:
    """Represents a single warning with message, severity, and recommended action"""

    def __init__(
        self, message: str, severity: WarningSeverity, recommended_action: str = ""
    ):
        self.message = message
        self.severity = severity
        self.recommended_action = recommended_action

    def get_severity_text(self) -> str:
        """Returns the severity level as text"""
        return self.severity.value


class WarningManager:
    """Manages multiple warnings and determines which to display"""

    def __init__(self):
        self.warnings: List[Warning] = []

    def add_warning(self, warning: Warning):
        """Add a warning to the manager"""
        # Remove any existing warning with the same message to avoid duplicates
        self.warnings = [w for w in self.warnings if w.message != warning.message]
        self.warnings.append(warning)
        autosa_logger.debug(f"Added Autosa warning: {warning.message}")

    def remove_warning(self, warning: Warning):
        """Remove a warning by message"""
        self.warnings = [w for w in self.warnings if w.message != warning.message]
        autosa_logger.debug(f"Removed Autosa warning: {warning.message}")

    def get_primary_warning(self) -> Warning:
        """Get the highest priority warning (highest severity)"""
        if not self.warnings:
            return None
        severity_order = {"High": 3, "Medium": 2, "Low": 1}
        return max(self.warnings, key=lambda w: severity_order[w.severity.value])

    def get_all_warnings(self) -> List[Warning]:
        """Get all warnings sorted by severity"""
        severity_order = {"High": 3, "Medium": 2, "Low": 1}
        return sorted(
            self.warnings, key=lambda w: severity_order[w.severity.value], reverse=True
        )

    def has_warnings(self) -> bool:
        """Check if there are any warnings"""
        return len(self.warnings) > 0

    def has_multiple_warnings(self) -> bool:
        """Check if there are multiple warnings"""
        return len(self.warnings) > 1

    def count(self) -> int:
        """Get the number of warnings"""
        return len(self.warnings)

    def check_datetime_warning(self, inst, inst_name):
        """Check if instrument and laptop clocks match"""
        time_diff, times_match = compare_datetime(inst, inst_name)
        if not times_match:
            self.add_warning(MISMATCHED_CLOCK_WARNING)
        else:
            self.remove_warning(MISMATCHED_CLOCK_WARNING)

    def check_settings_warning(self, inst):
        """Check if settings are valid"""
        if not is_settings_valid(inst):
            self.add_warning(SETTINGS_WARNING)
        else:
            self.remove_warning(SETTINGS_WARNING)

    def check_correction_warning(self):
        """Check if any corrections are set to 'No Correction'"""
        try:
            settings = read_settings_from_file()
            corr_choices = settings.get("-CORR CHOICES-", {})

            # Check if any band has "No Correction" set
            has_no_correction = any(
                choice == "No Correction" for choice in corr_choices.values()
            )

            if has_no_correction:
                self.add_warning(CORRECTION_NONE_WARNING)
            else:
                self.remove_warning(CORRECTION_NONE_WARNING)
        except Exception as e:
            autosa_logger.error(f"Error checking correction warning: {e}")
            # If there's an error reading settings, don't show the warning
            self.remove_warning(CORRECTION_NONE_WARNING)


# Warning constants
SETTINGS_WARNING = Warning(
    message="Settings Invalid. Please change settings.",
    severity=WarningSeverity.HIGH,
    recommended_action="Open Settings and ensure all entries are valid (invalid entries will be highlighted in red). Save the settings when done.",
)

MISMATCHED_CLOCK_WARNING = Warning(
    message="Instrument and test laptop device clocks do not match.",
    severity=WarningSeverity.MEDIUM,
    recommended_action="Ensure that the instrument and test laptop device clocks are both set to the same correct time. They must be within 5 minutes of each other. You may need to restart Autosa after adjusting the clocks.",
)

CORRECTION_NONE_WARNING = Warning(
    message="One or more corrections are set to 'No Correction'.",
    severity=WarningSeverity.MEDIUM,
    recommended_action="Go to Settings > Amplitude Correction and ensure each band has a correction file selected. If no correction files are listed, copy the required correction files to a folder on the instrument and set the 'Correction Files Folder' to the new folder.",
)
