import math
import random
from pathlib import Path

# --
# ...
# --


class Toolbox():

    @staticmethod
    def str_(input_):

        try:
            
            if isinstance(input_, str):
                return input_

            elif isinstance(input_, float) or isinstance(input_, int):
                return str(input_)

        except Exception as exp:
            print(str(exp))
            
# --
# ...
# --

    @staticmethod
    def get_random(start_string='RND ', type='string', limit=10000):

        try:
            
            result = 0
            
            if type == 'string':
                rand_ = math.ceil(random.random()*limit)
                if rand_ < 10:
                    rand_ += 10
                result = start_string + str(rand_)

            elif type == 'int':
                result = math.ceil(random.random()*limit)
                if result < 10:
                    result += 10
                    
            return result

        except Exception as exp:
            print(str(exp))
            
# --
# ...
# --

    @staticmethod
    def get_root_path() -> str:

        try:
            
            return str(Path(__file__).parent.parent)

        except Exception as exp:
            print(str(exp))