# import cv2 as cv
# import os

# def test_image_loading(image_path):
#     # Überprüfe, ob die Datei existiert
#     if not os.path.exists(image_path):
#         print(f"Error: The file at {image_path} does not exist.")
#         return

#     # Versuche, das Bild zu laden
#     image = cv.imread(image_path)

#     if image is None:
#         print(f"Error: Failed to load image from {image_path}.")
#     else:
#         print(f"Success: Image loaded successfully from {image_path}.")
#         # Zeige das Bild in einem Fenster an (optional)
#         cv.imshow('Loaded Image', image)
#         cv.waitKey(0)  # Warte auf eine Tasteneingabe, bevor das Fenster geschlossen wird
#         cv.destroyAllWindows()

# if __name__ == "__main__":
#     # Pfad zu deinem Bild
#     image_path = "/Users/magnus/Desktop/fancybuddy/resources/images/fishing_template.png"
#     test_image_loading(image_path)
import pyaudio
import wave
import numpy as np
import time
from scipy.signal import correlate
import sys
def list_input_devices():
    p = pyaudio.PyAudio()
    print("Available audio input devices:")
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print(f"Index {i}: {dev['name']}")
    p.terminate()
# Pfad zur Referenzsounddatei (.wav)
REFERENCE_SOUND_PATH = '/Users/magnus/Desktop/fancybuddy/resources/sounds/bitesound.wav'

# Audio-Einstellungen
CHUNK = 1024          # Anzahl der Frames pro Puffer
FORMAT = pyaudio.paInt16  # 16-Bit-Auflösung
CHANNELS = 1          # Mono
RATE = 44100          # Abtastrate

def load_reference_sound(path):
    # Lade die .wav-Datei und konvertiere sie in ein numpy-Array
    wf = wave.open(path, 'rb')
    reference_frames = wf.readframes(wf.getnframes())
    reference_signal = np.frombuffer(reference_frames, dtype=np.int16)
    wf.close()
    return reference_signal

def main():
    # Lade den Referenzsound
    try:
        reference_signal = load_reference_sound(REFERENCE_SOUND_PATH)
        print("Referenzsound geladen.")
    except FileNotFoundError:
        print(f"Die Datei {REFERENCE_SOUND_PATH} wurde nicht gefunden.")
        sys.exit(1)

    # Initialisiere PyAudio
    p = pyaudio.PyAudio()

    # Öffne den Stream für die Audioeingabe
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Audio-Stream gestartet. Warte auf den Zielsound...")

    try:
        while True:
            # Lese Daten aus dem Stream
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Überprüfung der Länge des Referenzsignals
            if len(audio_data) < len(reference_signal):
                continue  # Warte, bis genügend Daten gesammelt wurden

            # Kreuzkorrelation durchführen
            correlation = correlate(audio_data, reference_signal, mode='valid')
            peak = np.max(np.abs(correlation))

            # Schwellenwert für Erkennung (muss ggf. angepasst werden)
            threshold = 1e7

            if peak > threshold:
                print("Zielsound erkannt!")
                # Hier kannst du weitere Aktionen hinzufügen
                break

    except KeyboardInterrupt:
        print("Erkennung beendet.")

    finally:
        # Beende den Stream und PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == '__main__':
    main()
