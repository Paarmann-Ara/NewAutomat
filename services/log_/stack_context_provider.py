from services.log_.core.stack.stack_context import StackContext

# --
# ...
# --


class StackContextProvider:
    def __init__(self) -> None:
        self.stack = StackContext().StackOperation