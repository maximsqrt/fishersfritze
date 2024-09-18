### FUNCTIONALITY ###
#CAST LURE - FIND LURE - MOVE TO LURE - LISTEN FOR BYTE (defined in audio_agent)
import sys
import os
import cv2 as cv
import numpy as np
import pyautogui
import time
import logging


from agents.screen_agent import get_primary_monitor

# Initialisiere das Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class FishingAgent:
    def __init__(self, main_agent, audio_agent):
        self.main_agent = main_agent
        self.audio_agent = audio_agent
        self.fishing_target = cv.imread("/Users/magnus/Desktop/fancybuddy/resources/images/fishing_template.png")
        self.device_index = 1  # Device index for audio input
        logging.info("FishingAgent initialized")
        self.running = False  # Control flag
        
        
    def start(self):
        self.running = True
        logging.info('Fishing Agent Started')
        pass

    def cast_lure(self):
        time.sleep(2)
        pyautogui.press('1')  # Simulates pressing the fishing key
        print("Casting!...")
        time.sleep(2)
        center_loc = self.find_lure()
        if center_loc:
            self.move_to_lure(center_loc)
        else:
            print("Lure nicht gefunden")

    def find_lure(self):
        cur_img = self.main_agent.get_cur_img()
        if cur_img is None or self.fishing_target is None:
            logging.error("Current image or fishing target template is not available.")
            return None

        # Apply template matching to find the lure
        try:
            result = cv.matchTemplate(cur_img, self.fishing_target, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if max_val < 0.6:
                return None

            top_left = max_loc
            w, h = self.fishing_target.shape[1], self.fishing_target.shape[0]
            center_loc = (top_left[0] + w // 2, top_left[1] + h // 2)
            return center_loc
        except Exception as e:
            logging.error(f"Error during template matching: {e}")
            return None

    def move_to_lure(self, center_loc):
        primary_monitor = get_primary_monitor()
        screen_width, screen_height = primary_monitor.width, primary_monitor.height
        scale_x = screen_width / self.main_agent.get_cur_img().shape[1]
        scale_y = screen_height / self.main_agent.get_cur_img().shape[0]

        # Adjust coordinates based on scaling factors
        adjusted_x = int(center_loc[0] * scale_x)
        adjusted_y = int(center_loc[1] * scale_y)
        pyautogui.moveTo(adjusted_x, adjusted_y, duration=0.1, tween=pyautogui.easeOutQuad)
        print(f"Cursor moved to ({adjusted_x}, {adjusted_y})")
        self.listen_for_bite()

    
    
    def stop(self):
        # Add any cleanup code here if needed
        logging.info("FishingAgent stopped.")
    
    
    

