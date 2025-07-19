import pyvisa
import os
from ui.invalid_frame import PyVisaError
from ui.main_window import MainApp
from instrument.instrument import get_inst
from utils.log_config import autosa_logger
from utils.settings import (
    DEFAULT_SETTINGS,
    get_autosa_version,
    get_settings_path,
    read_settings_from_file,
    write_settings_to_file,
)


def assert_ni_visa_installed(pyvisa):
    try:
        pyvisa.ResourceManager()
        autosa_logger.debug("NI-VISA successfully found. Launching Autosa...")
        return True
    except pyvisa.errors.VisaIOError as e:
        PyVisaError.handle_py_visa_error(e)
        autosa_logger.exception("NI-VISA not found.")
        return False
    except Exception as e:
        PyVisaError.handle_py_visa_error(e)
        autosa_logger.exception(
            "An unexpected error occurred while checking NI-VISA installation."
        )
        return False


def make_json_valid():
    unchecked_settings = read_settings_from_file()
    valid_settings = {}

    for label, default_val in DEFAULT_SETTINGS.items():
        if label in unchecked_settings:
            value = unchecked_settings[label]
            if isinstance(value, str):
                autosa_logger.debug(f"Cleaning {label}.")
                value = value.strip()
            elif isinstance(value, dict) and isinstance(default_val, dict):
                # Clean nested dict keys and values
                value = {
                    k.strip(): v.strip() if isinstance(v, str) else v
                    for k, v in value.items()
                }
                # Fill missing subkeys from default
                for subkey, subval in default_val.items():
                    if subkey not in value:
                        autosa_logger.debug(
                            f"{label} {subkey} missing. Create and set to default value."
                        )
                        value[subkey] = subval
            valid_settings[label] = value
        else:
            valid_settings[label] = default_val
            autosa_logger.debug(f"{label} missing. Set to default value.")

    return valid_settings


def log_start():
    open_message = f"Autosa {get_autosa_version()} Started"
    padding = 10
    open_message = " " * padding + open_message + " " * padding
    autosa_logger.info("=" * len(open_message))
    autosa_logger.info(open_message)
    autosa_logger.info("=" * len(open_message))


def main():
    # Assert that NI-VISA is installed, else throw error dialog
    ni_visa_installed = assert_ni_visa_installed(pyvisa)
    if not ni_visa_installed:
        return

    # Assert that settings JSON file exists correctly
    settings_path = get_settings_path()
    if os.path.exists(settings_path):
        autosa_logger.info("Settings file found. Validating...")
        valid_settings = make_json_valid()
        write_settings_to_file(valid_settings)  # overwrite settings json
    else:
        autosa_logger.info("No settings file found. Created a default settings file.")
        write_settings_to_file(DEFAULT_SETTINGS)  # make default settings

    inst, inst_found, inst_name = get_inst()

    app = MainApp(inst, inst_found, inst_name)
    app.resizable(False, False)
    app.mainloop()


if __name__ == "__main__":
    try:
        log_start()
        main()
    except KeyboardInterrupt:
        autosa_logger.info("Autosa stopped by keyboard interrupt")
    except Exception as e:
        autosa_logger.exception(f"An error occurred: {e}")
    finally:
        autosa_logger.info("Autosa stopped")
