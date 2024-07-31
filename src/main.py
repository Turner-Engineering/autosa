import pyvisa
from ui.invalid_frame import PyVisaError
from ui.main_window import MainApp
from instrument.instrument import get_inst


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


def main():
    # Assert that NI-VISA is installed, else throw error dialog
    ni_visa_installed = assert_ni_visa_installed(pyvisa)
    if not ni_visa_installed:
        return

    inst, inst_found = get_inst()

    app = MainApp(inst_found, inst)
    app.resizable(False, False)
    app.mainloop()


if __name__ == "__main__":
    main()
