path = "extractedProject/Sprite1/sounds/Pop.wav"
import wave

# Open the WAV file
with wave.open(path, "rb") as wav_file:
    # Get the frame rate and number of frames
    frame_rate = wav_file.getframerate()
    n_frames = wav_file.getnframes()

    # Calculate the duration
    duration = n_frames / float(frame_rate)
    print(f"Length: {duration:.6f} seconds")
