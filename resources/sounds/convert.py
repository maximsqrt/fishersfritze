from pydub import AudioSegment

# Replace 'input.m4a' with the path to your .m4a file
input_file = 'bitesound.m4a'
# Replace 'output.wav' with the desired output path for the .wav file
output_file = 'output.wav'

# Load the .m4a file
audio = AudioSegment.from_file(input_file, format='m4a')

# Export the audio in .wav format
audio.export(output_file, format='wav')

print(f"Conversion complete: '{input_file}' has been converted to '{output_file}'")
