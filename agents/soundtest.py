import pyaudio
import numpy as np
from pydub import AudioSegment
import time
import logging
import librosa
import matplotlib.pyplot as plt
from scipy.fftpack import fft

def test_bite_detection():
    # Setup für AudioAgent-ähnliche Funktionalität
    bite_sound = AudioSegment.from_file('/Users/magnus/Desktop/fancybuddy/resources/sounds/bitesound.wav')
    bite_sound_np = np.array(bite_sound.get_array_of_samples()).astype(np.float32)  # Konvertiere AudioSegment in NumPy-Array
    sample_rate = bite_sound.frame_rate  # Nimm die Abtastrate von bite_sound
    chunk = 2048
    format = pyaudio.paInt16
    channels = 2
    device_index = 1  # Standard device index
    p = pyaudio.PyAudio()

    try:
        # Öffne den Audio-Stream
        stream = p.open(format=format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        input_device_index=device_index,
                        frames_per_buffer=chunk)
        print("Listening for sound...")

        # Startzeit für Timeout
        watch_time = time.time()

        while time.time() - watch_time < 30:  # 30 Sekunden Timeout für Test
            data = stream.read(chunk, exception_on_overflow=False)
            current_sound = np.frombuffer(data, dtype=np.int16).astype(np.float32)  # Konvertiere in float32 für FFT
            
            # Visualisiere den Vergleich und berechne die Fourier-Transformation
            correlation = compare_sounds_fft_visual(bite_sound_np, current_sound, sample_rate)
            if correlation > 0.5:  # Schwellwert für den Vergleich
                print("sound gefunden!")
                break

    except Exception as e:
        logging.error(f"Error during audio processing: {e}")

    finally:
        # Schließe den Stream
        if stream is not None:
            stream.stop_stream()
            stream.close()
        p.terminate()
        print("Stream closed.")

def compare_sounds_fft_visual(sound1_data, sound2_data, sample_rate):
    """Vergleich zweier Sounddaten im Frequenzbereich mit FFT und Visualisierung"""
    
    # Angleiche der Länge der Sounds
    min_len = min(len(sound1_data), len(sound2_data))
    sound1_data = sound1_data[:min_len]
    sound2_data = sound2_data[:min_len]

    # Fourier-Transformation durchführen
    fft_sound1 = np.abs(fft(sound1_data))
    fft_sound2 = np.abs(fft(sound2_data))

    # Frequenzen für das Plotten
    freqs = np.fft.fftfreq(min_len, 1/sample_rate)

    # Visualisiere die Spektren
    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(freqs[:min_len//2], fft_sound1[:min_len//2], label='bite_sound')
    plt.title('Frequenzspektrum von bite_sound')
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.subplot(2, 1, 2)
    plt.plot(freqs[:min_len//2], fft_sound2[:min_len//2], label='current_sound', color='r')
    plt.title('Frequenzspektrum von current_sound')
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    # Berechne die Korrelation der Fourier-transformierten Signale
    correlation = np.correlate(fft_sound1, fft_sound2, mode='valid')[0]
    
    # Normierung der Korrelation
    denominator = np.sqrt(np.correlate(fft_sound1, fft_sound1, mode='valid')[0] * np.correlate(fft_sound2, fft_sound2, mode='valid')[0])
    
    if denominator == 0:
        return 0

    return correlation / denominator


if __name__ == "__main__":
    test_bite_detection()
