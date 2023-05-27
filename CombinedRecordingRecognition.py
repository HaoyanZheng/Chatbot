import sounddevice as sd
import soundfile as sf
import speech_recognition as sr

def save_speech_as_wav_and_recognize(filename):
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

    # Initialize the recognizer
    r = sr.Recognizer()

    # Read the audio file
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)

    # Recognize the speech using Google Speech Recognition
    try:
        text = r.recognize_google(audio_text, language='zh-CN')
        print('Converting audio transcripts into text...')
        print(text)
    except:
        print('Sorry, something went wrong. Please try again.')

# Save the speech input to a WAV file called "speech.wav"
# and recognize it using Google Speech Recognition
save_speech_as_wav_and_recognize("speech.wav")