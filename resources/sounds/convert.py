import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import correlate
import time
import sys

# Pfad zum Templatesound
TEMPLATE_SOUND_PATH = '/Users/magnus/Desktop/fancybuddy/resources/sounds/bitesound.wav'

# Audio-Einstellungen
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 60  # 1 Minute Aufnahme

def load_template_sound(path):
    # Lade die .wav-Datei und konvertiere sie in ein numpy-Array
    wf = wave.open(path, 'rb')
    if wf.getnchannels() != CHANNELS:
        print("Der Templatesound muss mono sein.")
        sys.exit(1)
    template_frames = wf.readframes(wf.getnframes())
    template_signal = np.frombuffer(template_frames, dtype=np.int16)
    wf.close()
    return template_signal

def main():
    # Lade den Templatesound
    try:
        template_signal = load_template_sound(TEMPLATE_SOUND_PATH)
        print("Templatesound geladen.")
    except FileNotFoundError:
        print(f"Die Datei {TEMPLATE_SOUND_PATH} wurde nicht gefunden.")
        sys.exit(1)

    # Initialisiere PyAudio
    p = pyaudio.PyAudio()

    # Wähle das Eingabegerät (falls nötig, den Index des gewünschten Geräts hier angeben)
    INPUT_DEVICE_INDEX = None  # Oder z.B. 1, wenn du ein bestimmtes Gerät verwenden möchtest

    # Öffne den Stream für die Audioeingabe
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=INPUT_DEVICE_INDEX,
                    frames_per_buffer=CHUNK)

    print("Aufnahme gestartet. Bitte den Sound manuell erzeugen...")
    frames = []
    timestamps = []
    detections = []

    start_time = time.time()
    try:
        while time.time() - start_time < RECORD_SECONDS:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
            audio_chunk = np.frombuffer(data, dtype=np.int16)

            # Kreuzkorrelation durchführen
            correlation = correlate(audio_chunk, template_signal, mode='valid')
            peak = np.max(np.abs(correlation))

            # Schwellenwert für Erkennung (muss ggf. angepasst werden)
            threshold = 1e7  # Passe diesen Wert an deine Bedürfnisse an

            if peak > threshold:
                detection_time = time.time() - start_time
                print(f"Templatesound erkannt bei {detection_time:.2f} Sekunden")
                detections.append(detection_time)

            # Zeitstempel für die grafische Darstellung speichern
            timestamps.append(time.time() - start_time)

    except KeyboardInterrupt:
        print("Aufnahme beendet.")

    finally:
        # Beende den Stream und PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()

    print("Aufnahme abgeschlossen.")

    # Konvertiere die aufgenommenen Frames in ein numpy-Array
    audio_data = b''.join(frames)
    audio_signal = np.frombuffer(audio_data, dtype=np.int16)

    # Grafische Darstellung erstellen
    plt.figure(figsize=(15, 5))

    # Wellenform darstellen
    times = np.linspace(0, RECORD_SECONDS, num=len(audio_signal))
    plt.plot(times, audio_signal, label='Aufgenommenes Audio')

    # Erkennungszeitpunkte markieren
    for detection_time in detections:
        plt.axvline(x=detection_time, color='r', linestyle='--', label='Erkannte Templatesounds')

    plt.title('Aufgenommene Audio-Wellenform mit Erkennungsmarkierungen')
    plt.xlabel('Zeit (Sekunden)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
