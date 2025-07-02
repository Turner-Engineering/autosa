import pyvisa
import os
from ui.invalid_frame import PyVisaError
from ui.main_window import MainApp
from instrument.instrument import get_inst
from utils.settings import (
    default_settings,
    get_version_path,
    read_settings_from_file,
    write_settings_to_file,
)


def assert_ni_visa_installed(pyvisa):
    try:
        pyvisa.ResourceManager()
        return True
    except pyvisa.errors.VisaIOError as e:
        PyVisaError.handle_py_visa_error(e)
        return False
    except Exception as e:
        PyVisaError.handle_py_visa_error(e)
        return False


def make_json_valid():
    unchecked_settings = read_settings_from_file()
    valid_settings = {}

    for label, default_val in default_settings.items():
        if label in unchecked_settings:
            value = unchecked_settings[label]
            if isinstance(value, str):
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
                        value[subkey] = subval
            valid_settings[label] = value
        else:
            valid_settings[label] = default_val

    return valid_settings


def main():
    # Assert that NI-VISA is installed, else throw error dialog
    ni_visa_installed = assert_ni_visa_installed(pyvisa)
    if not ni_visa_installed:
        return

    # Assert that settings JSON file exists correctly
    filepath = get_version_path()
    if os.path.exists(filepath):
        valid_settings = make_json_valid()
        write_settings_to_file(valid_settings)  # overwrite settings json
    else:
        write_settings_to_file(default_settings)  # make default settings

    inst, inst_found = get_inst()

    app = MainApp(inst_found, inst)
    app.resizable(False, False)
    app.mainloop()


if __name__ == "__main__":
    main()
