# import pyaudio
# import numpy as np
# from pydub import AudioSegment
# import time
# import logging
# import matplotlib.pyplot as plt
# from scipy.fftpack import fft

# def test_bite_detection():
#     bite_sound = AudioSegment.from_file('/Users/magnus/Desktop/fancybuddy/resources/sounds/bitesound.wav')
#     bite_sound_np = np.array(bite_sound.get_array_of_samples()).astype(np.float32)
#     sample_rate = bite_sound.frame_rate
#     chunk = 2048
#     format = pyaudio.paInt16
#     channels = 2
#     device_index = 1
#     p = pyaudio.PyAudio()

#     all_correlations = []  # List to store correlations for plotting
#     all_frequencies = []  # List to store frequency data for plotting

#     try:
#         stream = p.open(format=format,
#                         channels=channels,
#                         rate=sample_rate,
#                         input=True,
#                         input_device_index=device_index,
#                         frames_per_buffer=chunk)
#         print("Listening for sound...")

#         start_time = time.time()

#         while time.time() - start_time < 30:  # Collect data for 30 seconds
#             data = stream.read(chunk, exception_on_overflow=False)
#             current_sound = np.frombuffer(data, dtype=np.int16).astype(np.float32)

#             # Perform FFT and store results
#             correlation, frequencies = compare_sounds_fft(bite_sound_np, current_sound, sample_rate)
#             all_correlations.append(correlation)
#             all_frequencies.append(frequencies)

#     except Exception as e:
#         logging.error(f"Error during audio processing: {e}")

#     finally:
#         if stream is not None:
#             stream.stop_stream()
#             stream.close()
#         p.terminate()

#         # Plot all collected data
#         plot_results(all_frequencies, all_correlations)
#         print("Stream closed.")

# def compare_sounds_fft(sound1_data, sound2_data, sample_rate):
#     min_len = min(len(sound1_data), len(sound2_data))
#     sound1_data = sound1_data[:min_len]
#     sound2_data = sound2_data[:min_len]

#     fft_sound1 = np.abs(fft(sound1_data))
#     fft_sound2 = np.abs(fft(sound2_data))

#     # Calculate frequencies for plotting
#     freqs = np.fft.fftfreq(min_len, 1/sample_rate)
    
#     # Calculate correlation
#     correlation = np.correlate(fft_sound1, fft_sound2, mode='valid')[0]
#     denominator = np.sqrt(np.correlate(fft_sound1, fft_sound1, mode='valid')[0] * np.correlate(fft_sound2, fft_sound2, mode='valid')[0])
#     if denominator == 0:
#         return 0, freqs
#     return correlation / denominator, freqs

# def plot_results(all_frequencies, all_correlations):
#     plt.figure(figsize=(10, 5))
#     for freqs, correlation in zip(all_frequencies, all_correlations):
#         plt.plot(freqs[:len(freqs)//2], correlation, label='Correlation over Time')
#     plt.title('Correlation of Frequencies Over Time')
#     plt.xlabel('Frequencies (Hz)')
#     plt.ylabel('Correlation')
#     plt.grid(True)
#     plt.show()

# if __name__ == "__main__":
#     test_bite_detection()
import pyautogui
import time

# def test_mouse_movement():
#     # Fail-Safe aktiviert lassen
#     pyautogui.FAILSAFE = False
#     time.sleep(3)
#     # Größe des Bildschirms ermitteln
#     screen_width, screen_height = pyautogui.size()
#     print(f"Screen width: {screen_width}, Screen height: {screen_height}")

#     # Bewege den Cursor in die obere linke Ecke
#     print("Moving to the top-left corner...")
#     pyautogui.moveTo(0, 0, duration=2)  # Langsame Bewegung über 2 Sekunden
#     time.sleep(2)  # Warte 2 Sekunden

#     # Bewege den Cursor in die untere rechte Ecke
#     print("Moving to the bottom-right corner...")
#     pyautogui.moveTo(screen_width - 1, screen_height - 1, duration=2)  # Langsame Bewegung über 2 Sekunden
#     time.sleep(2)  # Warte 2 Sekunden

#     # Zusätzlich kannst du den Cursor in die Mitte des Bildschirms bewegen
#     print("Moving to the center...")
#     pyautogui.moveTo(screen_width // 2, screen_height // 2, duration=2)  # Langsame Bewegung über 2 Sekunden
#     time.sleep(2)  # Warte 2 Sekunden

#     print("Test completed.")

# if __name__ == "__main__":
#     test_mouse_movement()
