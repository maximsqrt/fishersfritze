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

            frame_count = 0
            fps_report_time = time.time()  # Zeitstempel für FPS-Report
            fps_report_interval = 10  # Wie oft FPS gemeldet werden (in Sekunden)

            while self.running:
                # Screenshot des Monitors machen
                screenshot = np.array(sct.grab(monitor))

                # Sicherstellen, dass der Screenshot valide ist
                if screenshot.size == 0:
                    logging.debug("Invalid screenshot captured.")
                    continue

                # Screenshot in BGR umwandeln
                shared_screenshot = cv.cvtColor(screenshot, cv.COLOR_BGRA2BGR)

                # Aktuelles Bild an MainAgent weitergeben
                self.main_agent.set_cur_img(shared_screenshot)
                
                # Speicher freigeben
                del screenshot, shared_screenshot

                frame_count += 1

                # FPS jede Sekunde berechnen
                if time.time() - fps_report_time >= fps_report_interval:
                    self.report_fps(frame_count, fps_report_time)
                    frame_count = 0  # Frame-Zähler zurücksetzen
                    fps_report_time = time.time()  # Zeitstempel aktualisieren

                # Kurze Pause, um CPU-Auslastung zu minimieren
                time.sleep(0.005)

    def report_fps(self, frame_count, last_report_time):
        elapsed_time = time.time() - last_report_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
            logging.info(f"FPS: {fps:.2f}")

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
