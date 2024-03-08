import wave
import numpy as np

# Function to embed the watermark ID into the audio file
def embed_watermark(audio_file, watermark_id, output_file):
    with wave.open(audio_file, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        num_channels = wav_file.getnchannels()
        num_samples = wav_file.getnframes()
        audio_data = wav_file.readframes(num_samples)
        audio_buffer = np.frombuffer(audio_data, dtype=np.int16)
        audio_buffer = audio_buffer.reshape((num_samples, num_channels))

        # Convert the watermark ID to binary
        watermark_binary = ''.join(format(ord(char), '08b') for char in watermark_id)

        # Embed the watermark bits into the least significant bits of the audio samples
        watermark_index = 0
        for i in range(num_samples):
            for j in range(num_channels):
                if watermark_index < len(watermark_binary):
                    bit = int(watermark_binary[watermark_index])
                    audio_buffer[i, j] = (audio_buffer[i, j] & ~1) | bit
                    watermark_index += 1

        # Write the watermarked audio to the output file
        with wave.open(output_file, 'wb') as output_wav_file:
            output_wav_file.setparams(wav_file.getparams())
            output_wav_file.writeframes(audio_buffer.reshape((-1)).tobytes())

# Function to extract the watermark ID from the audio file
def extract_watermark(audio_file):
    with wave.open(audio_file, 'rb') as wav_file:
        num_channels = wav_file.getnchannels()
        num_samples = wav_file.getnframes()
        audio_data = wav_file.readframes(num_samples)
        audio_buffer = np.frombuffer(audio_data, dtype=np.int16)
        audio_buffer = audio_buffer.reshape((num_samples, num_channels))

        watermark_binary = ''
        for i in range(num_samples):
            for j in range(num_channels):
                bit = audio_buffer[i, j] & 1
                watermark_binary += str(bit)

        # Convert the binary watermark to ASCII characters
        watermark_id = ''
        for i in range(0, len(watermark_binary), 8):
            byte = watermark_binary[i:i+8]
            if len(byte) == 8:
                watermark_id += chr(int(byte, 2))

        return watermark_id

# Usage example
input_audio_file = 'input.wav'
output_audio_file = 'output.wav'
watermark_id = 'ExampleWatermarkID'

embed_watermark(input_audio_file, watermark_id, output_audio_file)
print('Watermark embedded successfully.')

extracted_watermark_id = extract_watermark(output_audio_file)
print('Extracted watermark ID:', extracted_watermark_id)