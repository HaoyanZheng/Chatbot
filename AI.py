import requests
import googletrans
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from playsound import playsound

def save_speech_as_wav_and_recognize(filename):
    # Set the recording duration (in seconds)
    duration = 5
    # Set the recording sample rate (in Hz)
    sample_rate = 44100
    # Set the number of channels (1 for mono, 2 for stereo)
    channels = 2

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
        return text
    except:
        print('Sorry, something went wrong. Please try again.')
        return ""

# Replace YOUR_API_KEY with your actual VoiceVox API key
voicevox_api_key = "i-V-38a071k167W"

# Replace YOUR_CHATBOT_API_KEY with your actual chatbot API key
chatbot_api_key = "9ffcb5785ad9617bf4e64178ac64f7b1"

# Set the base path to the user's OneDrive folder
speech_path = "D://WAIFU//speech.wav"
audio_path = "D://WAIFU//audio.wav"

# Set the VoiceVox API endpoint and headers
voicevox_endpoint = "https://api.su-shiki.com/v2/voicevox/audio/"
voicevox_headers = {
    "Authorization": f"Bearer {voicevox_api_key}"
}

# Set the chatbot API endpoint and headers
chatbot_endpoint = "https://api.ownthink.com/bot"
chatbot_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {chatbot_api_key}",
}

# Save the user's speech input as a WAV file and recognize it as text
text = save_speech_as_wav_and_recognize(speech_path)

# Set the query parameters for the chatbot API request
chatbot_params = {
    "appid": "9ffcb5785ad9617bf4e64178ac64f7b1",
    "spoken": text,
}

# Make the HTTP GET request to the chatbot API
response = requests.get(chatbot_endpoint, params=chatbot_params)

# Check the status code of the response
if response.status_code == 200:
    # Get the chatbot's response from the API response
    chatbot_response = response.json()["data"]["info"]["text"]
    print(chatbot_response)

    # Translate the chatbot's response into Japanese
    translator = googletrans.Translator()
    src_lang = translator.detect(chatbot_response).lang
    chatbot_response_ja = translator.translate(chatbot_response, dest='ja', src=src_lang).text
    print(chatbot_response_ja)

    # Check if the chatbot's response is empty
    if chatbot_response:
        # Set the query parameters for the VoiceVox API request
        voicevox_params = {
            "text": chatbot_response_ja,
            "key": voicevox_api_key,
        }

        # Make the HTTP GET request to the VoiceVox API
        response = requests.get(voicevox_endpoint, params=voicevox_params, headers=voicevox_headers)

        # Check the status code of the response
        if response.status_code == 200:
            # Choose a file name and location to save the audio file
            file_name = "audio.wav"

            # Save the audio data to the specified file
            with open(audio_path, "wb") as f:
                f.write(response.content)
            print(f"Audio file saved to {audio_path}")

            # Replace "D://WAIFU//audio.wav" with the actual path to the WAV file
            playsound(r"audio.wav")
        else:
            print(f"VoiceVox API returned status code {response.status_code}")
    else:
        print("The chatbot's response was empty.")
else:
    print(f"Chatbot API returned status code {response.status_code}")

