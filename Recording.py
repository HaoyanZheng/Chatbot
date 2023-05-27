import sounddevice as sd
import soundfile as sf

def save_speech_as_wav(filename):
    # Set the recording duration (in seconds)
    duration = 5
    # Set the recording sample rate (in Hz)
    sample_rate = 44100
    # Set the number of channels (1 for mono, 2 for stereo)
    channels = 1

    # Record the audio
    recording = sd.rec(int(duration * sample_rate),
                      samplerate=sample_rate,
                      channels=channels)
    print("Recording audio...")
    sd.wait()  # Wait until the recording is finished
    print("Recording finished!")

    # Save the recorded audio to a WAV file
    sf.write(filename, recording, sample_rate)

# Save the speech input to a WAV file called "speech.wav"
save_speech_as_wav("speech.wav")
