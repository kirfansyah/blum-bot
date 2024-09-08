import cv2
import numpy as np
import pyautogui
import win32gui
from PIL import ImageGrab
import keyboard  # Install dengan 'pip install keyboard'

# Hilangkan jeda setelah klik untuk mempercepat
pyautogui.PAUSE = 0

def get_window_coordinates(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    if hwnd:
        rect = win32gui.GetWindowRect(hwnd)
        x1, y1, x2, y2 = rect
        print(f"Koordinat jendela '{window_name}': ({x1}, {y1}, {x2}, {y2})")
        return rect
    else:
        print(f"Jendela dengan nama '{window_name}' tidak ditemukan.")
        return None

def detect_and_click_multiple_points(region, template_paths, max_clicks=5):
    # Ambil screenshot langsung pada region tertentu
    screenshot = ImageGrab.grab(bbox=region)
    img = np.array(screenshot)
    
    # Konversi ke grayscale untuk mempercepat pencocokan template
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Set untuk menyimpan posisi yang sudah diklik
    clicked_positions = set()
    clicked_points = 0
    found_green_dot = False  # Flag untuk menandai apakah green dot ditemukan

    # Loop melalui semua template yang tersedia
    for template_path in template_paths:
        # Load template dan ukurannya
        template = cv2.imread(template_path, 0)
        w, h = template.shape[::-1]
        
        # Template matching dengan metode yang lebih cepat
        res = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        
        # Klik pada titik yang ditemukan
        for pt in zip(*loc[::-1]):
            center = (pt[0] + w // 2 + region[0], pt[1] + h // 2 + region[1])
            
            if center not in clicked_positions:
                pyautogui.click(center)
                print(f"Template {template_path} terdeteksi dan diklik pada {center}")
                clicked_positions.add(center)
                clicked_points += 1
                found_green_dot = True  # Tandai bahwa green dot ditemukan
                
                # Menghilangkan titik yang sudah diklik
                cv2.rectangle(gray_img, (pt[0], pt[1]), (pt[0] + w, pt[1] + h), (0, 0, 0), -1)

            # Klik hanya sampai jumlah maksimum yang ditentukan
            if clicked_points >= max_clicks:
                break

        # Berhenti jika sudah mencapai jumlah klik maksimum
        if clicked_points >= max_clicks:
            break

    return found_green_dot

def move_mouse_to_center(region):
    # Pindahkan mouse ke tengah jendela
    x_center = (region[0] + region[2]) // 2
    y_center = (region[1] + region[3]) // 2
    pyautogui.moveTo(x_center, y_center)
    print(f"Mouse dipindahkan ke tengah jendela: ({x_center}, {y_center})")

def scroll_window_down():
    # Scroll ke bawah di dalam jendela
    scroll_amount = 1000  # Jumlah scroll (atur sesuai kebutuhan)
    pyautogui.scroll(-scroll_amount)
    print("Scroll ke bawah.")

def main():
    window_name = "TelegramDesktop"
    
    # Daftar path untuk gambar template yang berbeda
    template_paths = [
        "green_dot1.png",  # Path untuk template pertama
        "green_dot2.png",  # Path untuk template kedua
        "play.png",        # Path untuk template ketiga
        "play2.png",       # Path untuk template keempat
        "play3.png",       # Path untuk template kelima
        "play4.png",       # Path untuk template keenam
        "continue.png",    # Path untuk template ketujuh
        # Tambahkan path template lain jika diperlukan
    ]
    
    region = get_window_coordinates(window_name)
    
    if region:
        # Pindahkan mouse ke tengah jendela satu kali di awal
        move_mouse_to_center(region)
        
        print("Tekan 'Q' untuk menghentikan program.")
        try:
            while not keyboard.is_pressed('q'):
                found = detect_and_click_multiple_points(region, template_paths, max_clicks=5)
                
                if not found:
                    # Jika tidak menemukan green dot, scroll ke bawah
                    scroll_window_down()
        except KeyboardInterrupt:
            print("Program dihentikan dengan KeyboardInterrupt.")

if __name__ == "__main__":
    main()
