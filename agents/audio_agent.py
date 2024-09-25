import pyaudio
import numpy as np
import time
import logging
from scipy.signal import correlate

class AudioAgent:
    def __init__(self, main_agent, sample_rate=44100, chunk=1024):
        self.main_agent = main_agent
        self.bite_sound_path = '/Users/magnus/Desktop/fancybuddy/resources/sounds/bitesound.wav'
        self.chunk = chunk
        self.sample_rate = sample_rate
        self.format = pyaudio.paInt16
        self.channels = 1  # Verwende Mono für einfachere Verarbeitung
        self.p = pyaudio.PyAudio()
        self.device_index = None
        self.running = False
        self.thread = None
        logging.info("AudioAgent initialized")

        # Lade den Templatesound
        self.template_signal = self.load_template_sound(self.bite_sound_path)

        # Finde den Index des BlackHole-Geräts
        self.find_blackhole_device()

    def load_template_sound(self, path):
        import wave
        wf = wave.open(path, 'rb')
        if wf.getnchannels() != self.channels:
            print("Der Templatesound muss mono sein.")
            raise ValueError("Der Templatesound muss mono sein.")
        if wf.getframerate() != self.sample_rate:
            print(f"Der Templatesound muss eine Abtastrate von {self.sample_rate} Hz haben.")
            raise ValueError(f"Der Templatesound muss eine Abtastrate von {self.sample_rate} Hz haben.")
        template_frames = wf.readframes(wf.getnframes())
        template_signal = np.frombuffer(template_frames, dtype=np.int16).astype(np.float64)
        wf.close()
        # Mittelwert subtrahieren und normalisieren
        template_signal -= np.mean(template_signal)
        template_signal /= np.max(np.abs(template_signal))
        return template_signal

    def find_blackhole_device(self):
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if 'BlackHole' in dev['name']:
                self.device_index = i
                print(f"Found BlackHole device at index {i}")
                break
        if self.device_index is None:
            logging.error("BlackHole device not found.")
            raise ValueError("BlackHole device not found.")

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
        MAX_DURATION = 28  # Maximale Laufzeit in Sekunden
        max_peak = 0  # Variable zur Speicherung des maximalen Peaks

        try:
            stream = self.p.open(format=self.format,
                                channels=self.channels,
                                rate=self.sample_rate,
                                input=True,
                                input_device_index=self.device_index,
                                frames_per_buffer=self.chunk)
            logging.debug("Audio stream opened successfully.")
            print("Listening for bite...")

            buffer_size = len(self.template_signal)
            audio_buffer = np.zeros(buffer_size, dtype=np.float64)
            start_time = time.time()

            while not bite_detected and (time.time() - start_time) < MAX_DURATION:
                data = stream.read(self.chunk, exception_on_overflow=False)
                audio_chunk = np.frombuffer(data, dtype=np.int16).astype(np.float64)

                # Falls erforderlich, Stereo zu Mono konvertieren
                if self.channels == 2:
                    audio_chunk = audio_chunk.reshape(-1, 2)
                    audio_chunk = audio_chunk.mean(axis=1)

                # Aktualisiere den Puffer
                if len(audio_buffer) >= len(audio_chunk):
                    audio_buffer = np.concatenate((audio_buffer[len(audio_chunk):], audio_chunk))
                else:
                    print("Fehler: audio_chunk ist größer als audio_buffer")
                    break

                # Mittelwert subtrahieren und normalisieren
                audio_buffer_centered = audio_buffer - np.mean(audio_buffer)
                audio_buffer_centered /= np.max(np.abs(audio_buffer_centered) + 1e-10)  # Vermeidung von Division durch Null

                # Kreuzkorrelation durchführen
                correlation = correlate(audio_buffer_centered, self.template_signal, mode='valid')
                if len(correlation) == 0:
                    continue
                correlation_normalized = correlation / (np.linalg.norm(audio_buffer_centered) * np.linalg.norm(self.template_signal) + 1e-10)
                peak = np.max(correlation_normalized)

                # Aktualisiere den maximalen Peak-Wert
                max_peak = max(max_peak, peak)

                # Schwellenwert für die Erkennung
                threshold = 0.02  # Angepasster Schwellenwert
                if peak > threshold:
                    print("Bite detected!")
                    bite_detected = True
                    break  # Schleife abbrechen, wenn der Bite erkannt wurde
                else: False    
        except Exception as e:
            logging.error(f"Error during audio processing: {e}")

        finally:
            if stream is not None:
                stream.stop_stream()
                stream.close()
            logging.debug("Audio stream closed.")

            # Den maximalen Peak-Wert nach Beendigung des Programms ausgeben
            print(f"Maximaler Peak-Wert während der Aufnahme: {max_peak}")

        return bite_detected

