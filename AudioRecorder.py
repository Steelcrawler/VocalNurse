import sounddevice as sd
import numpy as np
from pydub import AudioSegment

recording = False

def record_audio(sample_rate=44100):
    global recording

    if recording:
        print("Recording... Press spacebar to stop.")
        audio_data = sd.rec(samplerate=sample_rate, channels=1, dtype=np.int16)
        sd.wait()  # Wait for the recording to finish
        print("Recording complete.")

        audio_segment = AudioSegment(
            audio_data.tobytes(),
            sample_width=audio_data.dtype.itemsize,
            frame_rate=sample_rate,
            channels=1
        )

        return audio_segment

    return None

if __name__ == "__main__":
    duration = 0  # Initialize duration to 0

    while True:
        key_input = input("Press spacebar to start/stop recording ('q' to quit): ").lower()

        if key_input == ' ':
            recording = not recording

            if recording:
                print("Start recording... Press spacebar to stop.")
            else:
                audio_segment = record_audio()
                if audio_segment:
                    output_path = "recorded_audio.mp3"
                    print(f"Saving as MP3: {output_path}")
                    audio_segment.export(output_path, format="mp3")
                    print(f"MP3 file saved at: {output_path}")

        elif key_input == 'q':
            break
