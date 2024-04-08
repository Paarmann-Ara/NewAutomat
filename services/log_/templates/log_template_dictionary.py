class LogTemplateDictionary():

    def __call__(self) -> dict:
        self.dictionary = {
            'Pipeline':"""str(datetime.datetime.now().strftime("%m-%d-%Y, %H:%M:%S")), f" {message}".ljust(8, ' ')""",
            'Error':"""str(datetime.datetime.now().strftime("%m-%d-%Y, %H:%M:%S")), f" {message}".ljust(8, ' ')""",
        }

        return self.dictionary