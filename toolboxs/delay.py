import time

class Delay():
    def __init__(self, delay_) -> None:
        print(f'I am waiting for {delay_} sec...')
        time.sleep(delay_)