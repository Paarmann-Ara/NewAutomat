import win32gui
import win32process

class chwnd():
#--
#...
#--
        @staticmethod
        def get_hwndsbyProcessid (pid, IsHe5x = True):
                
                def callback (hwnd, hwnds):
                        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                                if found_pid == pid:
                                        hwnds.append (hwnd)
                        return True
            
                hwnds = []
                win32gui.EnumWindows (callback, hwnds)
          
                return_hwnds = []
                for hwnd in hwnds:
                        return_hwnds.append(hex(hwnd) if IsHex else hwnd)
                  
                return return_hwnds
        