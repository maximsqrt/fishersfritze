import cv2 as cv
import numpy as np
import mss
import time
import logging
from threading import Thread, Lock
from screeninfo import get_monitors








class ScreenAgent:
    def __init__(self, main_agent):
        self.main_agent = main_agent
        self.lock = Lock()
        self.running = False
        self.thread = None  # Initialisiere thread mit None
    def get_primary_monitor(self):
        """Returns the primary monitor's details as a dictionary for MSS."""
        primary_monitor = None
        for monitor in get_monitors():
            if monitor.is_primary:
                primary_monitor = {
                    "left": monitor.x,
                    "top": monitor.y,
                    "width": monitor.width,
                    "height": monitor.height
                }
                break
        if not primary_monitor:
            logging.error("No primary monitor found.")
        return primary_monitor
   
    def capture_screen(self):
        with mss.mss() as sct:
            # Use the primary monitor from sct.monitors
            monitor = sct.monitors[0]  # sct.monitors[0] is usually the primary monitor

            t0 = time.time()
            fps_report_time = t0
            fps_report_delay = 5

            while self.running:
                screenshot = np.array(sct.grab(monitor))
                # Rest of your code...


            while self.running:
                # Debugging: Print monitor type
                logging.debug(f"Monitor type: {type(monitor)}, monitor: {monitor}")

                screenshot = np.array(sct.grab(monitor))
                if screenshot.size == 0:
                    logging.debug("Invalid screenshot captured.")
                    continue

                shared_screenshot = cv.cvtColor(screenshot, cv.COLOR_BGRA2BGR)
                self.main_agent.set_cur_img(shared_screenshot)
                del screenshot, shared_screenshot

                if time.time() - fps_report_time >= fps_report_delay:
                    self.report_fps(t0)
                    fps_report_time = time.time()

                t0 = time.time()
                time.sleep(0.005)  # Adjust as needed



    def report_fps(self, t0, last_report_time):
        ex_time = time.time() - t0
        if ex_time > 0:
            logging.info(f"FPS: {1 / ex_time:.2f}")

    def start(self):
        if not self.running:
            self.running = True
            self.thread = Thread(target=self.capture_screen)
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            if self.thread is not None:
                self.thread.join()
                self.thread = None

    def __del__(self):
        self.stop()