import numpy as np
import wave
import pyaudio
from scipy.signal import fftconvolve

def load_sound(file_path, sample_rate=44100, channels=1):
    wf = wave.open(file_path, 'rb')
    if wf.getframerate() != sample_rate or wf.getnchannels() != channels:
        raise ValueError("Sound file must match the sample rate and channels.")
    frames = wf.readframes(wf.getnframes())
    signal = np.frombuffer(frames, dtype=np.int16)
    wf.close()
    return signal

def normalize_signal(signal):
    signal = signal - np.mean(signal)
    signal = signal / np.max(np.abs(signal))
    return signal

def perform_fft_correlation(data_signal, template_signal):
    # Berechnung der Fourier-Transformierten
    data_fft = np.fft.fft(data_signal, n=(len(data_signal) + len(template_signal) - 1))
    template_fft = np.fft.fft(template_signal, n=(len(data_signal) + len(template_signal) - 1))
    # Kreuzkorrelation im Frequenzbereich und Rücktransformation
    correlation = np.fft.ifft(data_fft * np.conj(template_fft)).real
    return correlation

def test_bite_detection(audio_input_path, bite_sound_path, sample_rate=44100, chunk_size=1024):
    # Lade den Biss-Sound
    bite_sound = load_sound(bite_sound_path, sample_rate)
    bite_sound = normalize_signal(bite_sound)

    # Konfiguration des Audio-Streams
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)

    print("Starting bite sound detection test...")
    try:
        # Aufnehmen eines kurzen Audio-Segments zum Testen
        frames = []
        for _ in range(0, int(sample_rate / chunk_size * 2)):  # Nehme für 2 Sekunden auf
            data = stream.read(chunk_size)
            frames.append(data)
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        audio_data = normalize_signal(audio_data)

        # FFT-basierte Korrelation durchführen
        correlation = perform_fft_correlation(audio_data, bite_sound)
        # Finde den höchsten Peak in der Korrelation
        peak = np.max(correlation)
        print(f"Max correlation peak: {peak}")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

# Pfade zu den Audiodateien
audio_input_path = '/path/to/real_time_captured_audio.wav'  # Pfad zur Echtzeitaufnahme
bite_sound_path = '/Users/magnus/Desktop/fancybuddy/resources/sounds/bitesound.wav'

test_bite_detection(audio_input_path, bite_sound_path)
