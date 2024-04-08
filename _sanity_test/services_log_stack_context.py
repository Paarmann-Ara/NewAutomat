from services.log_.stack_context_provider import StackContextProvider
from services.log_.log_provider import LogProvider

info = LogProvider(template='Pipeline',config='Pipeline').info_instance
stack = StackContextProvider().stack

stack(object_name='smple Object')
info(stack())
info(stack())
info(stack())