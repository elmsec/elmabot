class JobResult:
    """
    Simple model to save state of a job.
    """
    def __init__(
            self, parser, successful=0, unsuccessful=0, return_value=None):
        self._parser = parser
        self._successful = successful
        self._unsuccessful = unsuccessful
        self._return_value = return_value

    def increase_succesful(self):
        self._successful += 1

    def increase_unsuccesful(self):
        self._unsuccessful += 1

    def set_return_value(self, value):
        self._return_value = value

    @property
    def successful(self):
        return self._successful
