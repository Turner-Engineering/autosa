class LoggedInstrument:
    def __init__(self, inst, logger):
        self._inst = inst
        self._logger = logger

    def write(self, *args, **kwargs):
        # This is called instead of the original write method
        command = args[0] if args else ""
        self._logger.debug(f">>> INST WRITE >>>: {repr(command)}")
        try:
            # this is the original write method
            self._inst.write(*args, **kwargs)
        except Exception as e:
            self._logger.error(f"[INST ERROR]: {e}")
            raise e

    def query(self, *args, **kwargs):
        # This is called instead of the original query method
        command = args[0] if args else ""
        self._logger.debug(f">>> INST QUERY >>>: {repr(command)}")
        try:
            # this is the original query method
            response = self._inst.query(*args, **kwargs)
            self._logger.debug(f"<<< INST RESPN <<<: {repr(response)}")
            return response
        except Exception as e:
            self._logger.error(f"[INST ERROR]: {e}")
            raise e

    def __getattr__(self, item):
        # This is called when any other attribute is accessed
        attr = getattr(self._inst, item)

        if callable(attr):
            # If the attribute is callable (like a method), we wrap it in a logging function

            def wrapper(*args, **kwargs):
                self._logger.debug(f"[INST CALL] {item} args={args}, kwargs={kwargs}")
                try:
                    return attr(*args, **kwargs)
                except Exception as e:
                    self._logger.error(f"[INST ERROR in {item}]: {e}")
                    raise e

            return wrapper
        else:
            self._logger.debug(f"[INST ATTR] {item} -> {repr(attr)}")
            return attr

    def __str__(self):
        return str(self._inst)
