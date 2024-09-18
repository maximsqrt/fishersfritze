import pyaudio
import numpy as np
from pydub import AudioSegment
import time
import logging

class AudioAgent:
    def __init__(self, main_agent, sample_rate=48000, chunk=2048):
        self.main_agent = main_agent
        self.bite_sound = AudioSegment.from_file('/Users/magnus/Desktop/fancybuddy/resources/sounds/bitesound.wav')
        self.chunk = chunk
        self.sample_rate = sample_rate
        self.format = pyaudio.paInt16
        self.channels = 2
        self.p = pyaudio.PyAudio()
        self.device_index = 1  # Standard device index
        self.running = False
        self.thread = None
        logging.info("AudioAgent initialized")

    def start(self):
        logging.info("AudioAgent started.")

    def stop(self):
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()
                logging.info("AudioAgent stopped.")

    def listen_for_bite(self):
        bite_detected = False
        watch_time = time.time()

        try:
            stream = self.p.open(format=self.format,
                                 channels=self.channels,
                                 rate=self.sample_rate,
                                 input=True,
                                 input_device_index=self.device_index,
                                 frames_per_buffer=self.chunk)
            logging.debug("Audio stream opened successfully.")
            print("Listening for bite...")

            while not bite_detected and time.time() - watch_time < 20:  # 20 seconds timeout
                data = stream.read(self.chunk, exception_on_overflow=False)
                current_sound = np.frombuffer(data, dtype=np.int16)
                current_sound = AudioSegment(current_sound.tobytes(), sample_width=2, frame_rate=self.sample_rate, channels=self.channels)
                
                correlation = self.compare_sounds(self.bite_sound, current_sound)
                if correlation > 0.1:  # Threshold to detect a bite
                    print("Bite detected!")
                    bite_detected = True

        except Exception as e:
            logging.error(f"Error during audio processing: {e}")

        finally:
            if stream is not None:
                stream.stop_stream()
                stream.close()
            self.p.terminate()
            logging.debug("Audio stream closed.")

    def compare_sounds(self, sound1, sound2):
        sound1_data = np.array(sound1.get_array_of_samples()).astype(np.float32)
        sound2_data = np.array(sound2.get_array_of_samples()).astype(np.float32)

        min_len = min(len(sound1_data), len(sound2_data))
        sound1_data = sound1_data[:min_len]
        sound2_data = sound2_data[:min_len]

        numerator = np.correlate(sound1_data, sound2_data, mode='valid')[0]
        denominator = np.sqrt(np.correlate(sound1_data, sound1_data, mode='valid')[0] * np.correlate(sound2_data, sound2_data, mode='valid')[0])
        if denominator == 0:
            return 0
        return numerator / denominator
