import win32gui

def list_active_windows():
    """Mencetak semua jendela aktif dan nama-namanya."""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    for hwnd, title in windows:
        print(f"HWND: {hwnd}, Title: '{title}'")

if __name__ == "__main__":
    list_active_windows()
