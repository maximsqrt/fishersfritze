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
RECORD_SECONDS = 10  # 10 Sekunden Aufnahme

def load_template_sound(path):
    # Lade die .wav-Datei und konvertiere sie in ein numpy-Array
    wf = wave.open(path, 'rb')
    if wf.getnchannels() != CHANNELS:
        print("Der Templatesound muss mono sein.")
        sys.exit(1)
    if wf.getframerate() != RATE:
        print(f"Der Templatesound muss eine Abtastrate von {RATE} Hz haben.")
        sys.exit(1)
    template_frames = wf.readframes(wf.getnframes())
    template_signal = np.frombuffer(template_frames, dtype=np.int16).astype(np.float64)
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

    # Wähle das Eingabegerät (falls nötig)
    INPUT_DEVICE_INDEX = None  # Anpassen, falls erforderlich

    # Öffne den Stream für die Audioeingabe
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=INPUT_DEVICE_INDEX,
                    frames_per_buffer=CHUNK)

    print("Aufnahme gestartet. Bitte den Sound manuell erzeugen...")
    frames = []

    start_time = time.time()
    try:
        while time.time() - start_time < RECORD_SECONDS:
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
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
    audio_signal = np.frombuffer(audio_data, dtype=np.int16).astype(np.float64)

    # Mittelwert von Signalen subtrahieren
    audio_signal -= np.mean(audio_signal)
    template_signal -= np.mean(template_signal)

    # Kreuzkorrelation über das gesamte Signal durchführen
    correlation = correlate(audio_signal, template_signal, mode='valid')

    # Normalisierung der Kreuzkorrelation
    norm_factor = np.sqrt(np.sum(audio_signal**2) * np.sum(template_signal**2))
    if norm_factor == 0:
        norm_factor = 1
    correlation_normalized = correlation / norm_factor

    # Plot der Kreuzkorrelation
    plt.figure(figsize=(15, 5))
    plt.plot(correlation_normalized)
    plt.title('Normalisierte Kreuzkorrelation')
    plt.xlabel('Zeit (Samples)')
    plt.ylabel('Korrelationswert')
    plt.show()

    # Erkennungszeitpunkte ermitteln
    threshold = 0.5  # Anpassen je nach beobachteten Werten
    detections = np.where(correlation_normalized > threshold)[0]
    detection_times = detections / RATE  # Umrechnung in Sekunden

    # Plot der aufgenommenen Audiodaten mit Markierungen
    times = np.linspace(0, len(audio_signal) / RATE, num=len(audio_signal))
    plt.figure(figsize=(15, 5))
    plt.plot(times, audio_signal)
    for dt in detection_times:
        plt.axvline(x=dt, color='r', linestyle='--', label='Erkannter Templatesound')
    plt.title('Aufgenommenes Audio mit Erkennungsmarkierungen')
    plt.xlabel('Zeit (Sekunden)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
