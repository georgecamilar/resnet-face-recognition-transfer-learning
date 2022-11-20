class AppException(Exception):
    """
        Constructor
        :param message : the error message
        :type message : str
        :param module_name : the module the error occurred and was thrown
        :type message : str
    """
    def __init__(self, message, module_name):
        self.module_name = module_name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.module_name} -> {self.message}'
