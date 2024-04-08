class cTimeDictionary:
    def __call__(self) -> dict:
        self.dictionary = {
            'Nano': 0.05,
            'MicroTime': 0.090,
            'SendErrorToBugReportTime': 0.150,
            'TinyTime': 0.250,
            'SmallTime': 0.350,
            'RefreshingTime': 0.500,
            'RegularTime': 0.700,
            'StartupWarnung': 0.800,
            'ExitError0': 2.500,
            'MediumTime': 3.000,
            'LargTime': 8.000,
            'RestoreDBOnErrorTime': 9.000,
            'VeryLargTime': 11.000,
            'Update': 120.000,
        }
        
        return self.dictionary