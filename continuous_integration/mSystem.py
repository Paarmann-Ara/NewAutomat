import ctypes

#--
#...
#--
class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong), 
        ("dwMemoryLoad", ctypes.c_ulong), 
        ("ullTotalPhys", ctypes.c_ulonglong), 
        ("ullAvailPhys", ctypes.c_ulonglong), 
        ("ullTotalPageFile", ctypes.c_ulonglong), 
        ("ullAvailPageFile", ctypes.c_ulonglong), 
        ("ullTotalVirtual", ctypes.c_ulonglong), 
        ("ullAvailVirtual", ctypes.c_ulonglong), 
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong), 
    ]

    def __init__(self):
        self.dwLength = ctypes.sizeof(self)
        super(MEMORYSTATUSEx, self).__init__()
#--
#...
#--    

class GetStatus():
#--
#...
#--
        @staticmethod
        def GetAll():
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(MEMORYSTATUSEX()))

                return 'MemLoad' + IntToStr(MEMORYSTATUSEX().dwMemoryLoad) + '%, of ' + IntToStr(MEMORYSTATUSEX().ullAvailPhys)
        
        
def g():

    mem = GetStatus.GetAll()
    Log.Warning("MemoryLoad:" + mem )