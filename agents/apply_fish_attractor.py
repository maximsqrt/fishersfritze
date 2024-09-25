# button_press.py

import time
import threading
import pyautogui

def press_buttons(interval_minutes=5):
    """
    Drückt alle `interval_minutes` Minuten die Tasten "2" und "4" mit einer Pause von 0,5 Sekunden dazwischen.
    Die Funktion läuft in einem separaten Thread.
    """
    def button_press_loop():
        time.sleep(.1)
        while True:
            pyautogui.press('2')
            time.sleep(0.5)
            pyautogui.press('4')
            time.sleep(interval_minutes * 60 - 0.5)  # Subtrahiere die bereits gewarteten 0,5 Sekunden

    # Starte die Schleife in einem separaten Thread
    threading.Thread(target=button_press_loop, daemon=True).start()
