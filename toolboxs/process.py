from Toolboxs.mDelay import cDelay
import subprocess

# --
# ...
# --


class cProcess():
    def __init__(self) -> None:
        pass

# --
# ...
# --

    @staticmethod
    def run(AppAdress):
        subprocess.Popen(AppAdress)
# --
# ...
# --

    @staticmethod
    def terminat(Appexecute):
        while cProcess.IsRunnigProcesByName(Appexecute):
            subprocess.call("TASKKILL /F /IM " + Appexecute, shell=True)
            cDelay(5)
# --
# ...
# --

    @staticmethod
    def IsRunnigProcesByName(Appexecute) -> bool:
        return True if cProcess.ProcessIdByName(Appexecute, False) else False
# --
# ...
# --

    @staticmethod
    def ListOfAllProcess():
        # [HandleCount Name Priority ProcessId ThreadCount WorkingSetSize]
        allProcess = []

        Data = subprocess.check_output(['wmic', 'process', 'list', 'brief'])

        a = str(Data).split("\\r\\r\\n")

        for b in a:
            allProcess.append(",".join(b.split()).split(","))

        return allProcess
# --
# ...
# --

    @staticmethod
    def ProcessIdByName(ProcessName, IsHex=True):
        for process in cProcess.ListOfAllProcess():
            if len(process) > 1 and process[1] == ProcessName:
                return hex(int(process[3])) if IsHex else int(process[3])

        return False