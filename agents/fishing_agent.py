import cv2 as cv
import numpy as np
import pyautogui
import time
import logging
import sys
import os
import Quartz

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from screen_agent import ScreenAgent

# Logging initialisieren
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_scaling_factors():
    main_display_id = Quartz.CGMainDisplayID()
    # Physische Bildschirmgröße in Pixeln
    physical_width = Quartz.CGDisplayPixelsWide(main_display_id)
    physical_height = Quartz.CGDisplayPixelsHigh(main_display_id)
    # Logische Bildschirmgröße in Punkten
    bounds = Quartz.CGDisplayBounds(main_display_id)
    logical_width = bounds.size.width
    logical_height = bounds.size.height
    # Skalierungsfaktoren berechnen
    scale_factor_x = physical_width / logical_width
    scale_factor_y = physical_height / logical_height
    return scale_factor_x, scale_factor_y

class FishingAgent:
    def __init__(self, main_agent, audio_agent, screen_agent):
        self.main_agent = main_agent
        self.audio_agent = audio_agent
        self.screen_agent = screen_agent
        self.fishing_target = cv.imread("/Users/magnus/Desktop/fancybuddy/resources/images/fishing_template.png")
        self.device_index = 1  # Device index for audio input
        logging.info("FishingAgent initialized")
        self.running = False  # Control flag
            
    def start(self):
        self.running = True
        logging.info('Fishing Agent Started')
        self.cast_lure()

    def cast_lure(self):
        time.sleep(2)
        pyautogui.press('1')  # Simulates pressing the fishing key
        print("Casting!...")
        time.sleep(2)
        center_loc = self.find_lure()
        if center_loc:
            self.move_to_lure(center_loc)
            print("center_loc", center_loc)
        else:
            print("Lure nicht gefunden")

    def find_lure(self):
        cur_img = self.main_agent.get_cur_img()
        if cur_img is None or self.fishing_target is None:
            logging.error("Current image or fishing target template is not available.")
            return None

        try:
            result = cv.matchTemplate(cur_img, self.fishing_target, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            threshold = 0.2
            if max_val < threshold:
                return None

            top_left = max_loc
            w, h = self.fishing_target.shape[1], self.fishing_target.shape[0]
            center_loc = (top_left[0] + w // 2, top_left[1] + h // 2)
            return center_loc
        except Exception as e:
            logging.error(f"Error during template matching: {e}")
            return None

    def move_to_lure(self, center_loc):
        # Hole die physische Bildschirmauflösung direkt vom primären Monitor
        primary_monitor = self.screen_agent.get_primary_monitor()
        if not primary_monitor:
            logging.error("No primary monitor found.")
            return

        screen_width = primary_monitor['width']
        screen_height = primary_monitor['height']
        print(f"Physical screen resolution: {screen_width} x {screen_height}")

   

        # Hole die Auflösung des Screenshots
        cur_img = self.main_agent.get_cur_img()
        if cur_img is None:
            logging.error("Current image is not available.")
            return
        screenshot_height, screenshot_width = cur_img.shape[:2]
        print(f"Screenshot resolution: {screenshot_width} x {screenshot_height}")

        # Berechne die Skalierungsfaktoren
        scale_x = screenshot_width / screen_width
        scale_y = screenshot_height / screen_height
        print(f"Scale factors - X: {scale_x}, Y: {scale_y}")

        # Justiere die Koordinaten basierend auf den Skalierungsfaktoren
        adjusted_x = int(center_loc[0] / scale_x)
        adjusted_y = int(center_loc[1] / scale_y)
        print(f"Adjusted coordinates: ({adjusted_x}, {adjusted_y})")

        # Bewege die Maus zur angepassten Position
        pyautogui.moveTo(adjusted_x, adjusted_y, duration=0.1, tween=pyautogui.easeOutQuad)
        print(f"Cursor moved to ({adjusted_x}, {adjusted_y})")

        # Warte auf den Biss und führe einen Rechtsklick aus
        if self.audio_agent.listen_for_bite():
            pyautogui.click(button='right')  # Rechtsklick ausführen
            time.sleep(0.5)
            self.cast_lure()




    def stop(self):
        logging.info("FishingAgent stopped.")
