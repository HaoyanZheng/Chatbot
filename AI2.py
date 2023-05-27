import requests #for getting the content of a html
import googletrans #google translate api
import sounddevice as sd #for recording
import soundfile as sf #write user's speech input
import speech_recognition as sr #speech recognizer
import keyboard
import numpy as np
import time
import pyautogui
from playsound import playsound
import os
import tempfile

# VoiceVox API key
voicevox_api_key = "i-V-38a071k167W"

# chatbot API key
chatbot_api_key = "9ffcb5785ad9617bf4e64178ac64f7b1"

# Set the base path to the user's OneDrive folder
speech_path = "D://WAIFU//speech.wav"

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

# initialize sound source
sound_source = 0

# initialize sound library
sound_library = {2: "四国めたん-ノーマル", 0: "四国めたん-あまあま", 6: "四国めたん-ツンツン", 4: "四国めたん-セクシー", 36: "四国めたん-ささやき", 37: "四国めたん-ささやき", 3: "ずんだもん-ノーマル", 1: "ずんだもん-あまあま", 7: "ずんだもん-ツンツン", 5: "ずんだもん-セクシー", 22: "ずんだもん-ささやき", 38: "ずんだもん-ヒソヒソ", 8: "春日部つむぎ-ノーマル", 10: "雨晴はう-ノーマル", 9: "波音リツ-ノーマル", 11: "ノーマル", 12: "白上虎太郎-ふつう", 32: "白上虎太郎-わーい", 33: "白上虎太郎-びくびく", 34: "白上虎太郎-おこ", 35: "白上虎太郎-びえーん", 13: "青山龍星-ノーマル", 14: "冥鳴ひまり-ノーマル", 16: "冥鳴ひまり-ノーマル", 15: "冥鳴ひまり-あまあま", 18: "冥鳴ひまり-ツンツン", 17: "冥鳴ひまり-セクシー", 19: "冥鳴ひまり-ささやき", 20: "もち子さん-ノーマル", 21: "剣崎雌雄-ノーマル", 23: "WhiteCUL-ノーマル", 24: "WhiteCUL-たのしい", 25: "WhiteCUL-かなしい", 26: "WhiteCUL-びえーん", 27: "後鬼-人間ver.", 28: "後鬼-ぬいぐるみver.", 29: "No.7-ノーマル", 30: "No.7-アナウンス", 31: "No.7-読み聞かせ"}

def save_speech_as_wav_and_recognize(filename):
    global sound_source

    # Set the recording sample rate (in Hz)
    sample_rate = 44100

    # Set the number of channels (1 for mono, 2 for stereo)
    channels = 2

    # Initialize the recognizer
    r = sr.Recognizer()

    # Start recording audio
    recording = []
    recording_started = False
    recording_start_time = 0

    while True:
        if keyboard.is_pressed(" "):

            if not recording_started:
                recording_start_time = time.time()
                recording.append(sd.rec(int(1 * sample_rate), samplerate=sample_rate, channels=channels))
                print("Recording audio...")
                recording_started = True

            # Add a delay of 0.1 seconds between the successive checks for the space bar press
            time.sleep(0.1)

        else:
            if recording_started:
                recording_end_time = time.time()
                recording_length = recording_end_time - recording_start_time
                print(f"Recording finished! Length of recording: {recording_length:.2f} seconds")
                for i in range(10*int(recording_length)):
                    pyautogui.keyDown("backspace")
                break

    # Check if the recording list is not empty
    if recording:

        # Concatenate the recorded audio chunks using numpy's concatenate function
        recording = np.concatenate(recording, axis=0)
    else:

        # Set recording to an empty array if the recording list is empty
        recording = np.array([])

    # Create a temporary file and save the recorded audio to it
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.wav', delete = False) as temp_file:
        sf.write(temp_file, recording, sample_rate)
        temp_file.seek(0)
        with sr.AudioFile(temp_file.name) as source:
            audio_text = r.listen(source)

    # Recognize the speech using Google Speech Recognition
    try:
        text = r.recognize_google(audio_text, language='zh-CN')
        print('Converting audio transcripts into text...')
        print(text)
        return text
    except Exception as e:
        # print(f'Sorry, something went wrong. Please try again. Error: {e}')
        return ""

def play_audio(chatbot_response):
        print("She says: " + chatbot_response)

        # Translate the chatbot's response into Japanese
        translator = googletrans.Translator()
        src_lang = translator.detect(chatbot_response).lang
        chatbot_response_ja = translator.translate(chatbot_response, dest='ja', src=src_lang).text
        print("She says: " + chatbot_response_ja + "\n")

        # Set the query parameters for the VoiceVox API request
        voicevox_params = {
            "text": chatbot_response_ja,
            "key": voicevox_api_key,
            "speaker": sound_source,
            #pitch: -1 ~ 1,
            # "pitch": 0,
            #intonationScale: -4 ~ 3, negative is rhetorical question, 0 is normal, positive is mad
            # "intonationScale": 1,
            #speed: > 0
            # "speed": 1
        }

        # Make the HTTP POST request to the VoiceVox API
        response = requests.post(voicevox_endpoint, params=voicevox_params, headers=voicevox_headers)

        # Check the status code of the response
        if response.status_code == 200:

            # Write the audio data to a temporary file
            with tempfile.NamedTemporaryFile(mode='wb', suffix='.wav', delete=False) as f:
                f.write(response.content)

            # Play the audio file using playsound
            playsound(f.name)

        else:
            print("VoiceVox坏掉惹。。。")

def audio_input():
    global sound_source
    while True:
        print("Press SPACE to start recording, release SPACE to stop recording. \nPress F1 to quit. \nPress F2 to switch sound source. \nThe current sound source is: " + sound_library[sound_source])

        key = keyboard.read_key()

        if key == "f1":
            exit()

        elif key == "f2":
            switch_soundsource()

        else:
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
                if text == "":
                    chatbot_response = "说点什么嘛~"
                    play_audio(chatbot_response)

                # Get the chatbot's response from the API response
                else:
                    chatbot_response = response.json()["data"]["info"]["text"]
                    play_audio(chatbot_response)

            else:
                print("聊天机器人坏掉惹。。。")

def exit():
            pyautogui.keyDown("backspace")

            print("She says: 拜拜~")
            print("She says: バイバイ~")

            # Set the query parameters for the VoiceVox API request
            voicevox_params = {
                "text": "バイバイ~",
                "key": voicevox_api_key,
                "speaker": sound_source,
                #pitch: -1 ~ 1,
                "pitch": 0,
                #intonationScale: -4 ~ 3, negative is rhetorical question, 0 is normal, positive is mad
                "intonationScale": 1,
                #speed: > 0
                "speed": 1
            }

            # Make the HTTP POST request to the VoiceVox API
            response = requests.post(voicevox_endpoint, params=voicevox_params, headers=voicevox_headers)

            # Check the status code of the response
            if response.status_code == 200:

                # Write the audio data to a temporary file
                with tempfile.NamedTemporaryFile(mode='wb', suffix='.wav', delete=False) as f:
                    f.write(response.content)

                # Play the audio file using playsound
                playsound(f.name)

            print("Program has exited.")

            os._exit(0)

def switch_soundsource():
    global sound_source
    sound_source = int(input("Here's a list of all the sound sources:  \n2: 四国めたん-ノーマル \n0: 四国めたん-あまあま \n6: 四国めたん-ツンツン \n4: 四国めたん-セクシー \n36: 四国めたん-ささやき \n37: 四国めたん-ささやき \n3: ずんだもん-ノーマル \n1: ずんだもん-あまあま \n7: ずんだもん-ツンツン \n5: ずんだもん-セクシー \n22: ずんだもん-ささやき \n38: ずんだもん-ヒソヒソ \n8: 春日部つむぎ-ノーマル \n10: 雨晴はう-ノーマル \n9: 波音リツ-ノーマル \n11: ノーマル \n12: 白上虎太郎-ふつう \n32: 白上虎太郎-わーい \n33: 白上虎太郎-びくびく \n34: 白上虎太郎-おこ \n35: 白上虎太郎-びえーん \n13: 青山龍星-ノーマル \n14: 冥鳴ひまり-ノーマル \n16: 冥鳴ひまり-ノーマル \n15: 冥鳴ひまり-あまあま \n18: 冥鳴ひまり-ツンツン \n17: 冥鳴ひまり-セクシー \n19: 冥鳴ひまり-ささやき \n20: もち子さん-ノーマル \n21: 剣崎雌雄-ノーマル \n23: WhiteCUL-ノーマル \n24: WhiteCUL-たのしい \n25: WhiteCUL-かなしい \n26: WhiteCUL-びえーん \n27: 後鬼-人間ver. \n28: 後鬼-ぬいぐるみver. \n29: No.7-ノーマル \n30: No.7-アナウンス \n31: No.7-読み聞かせ\nPlease enter the number for the desired sound source: "))

    print("You have selected the sound source: " + sound_library[sound_source])

def text_input():
    global sound_source
    while True:
        print("Type your message \nPress F1 to quit. \nPress F2 to switch sound source. \nThe current sound source is: " + sound_library[sound_source])

        key = keyboard.read_key()

        if key == "f1":
            exit()

        elif key == "f2":
            switch_soundsource()
            continue

        else:
            # Save the user's speech input as a WAV file and recognize it as text
            text = input()

            # Set the query parameters for the chatbot API request
            chatbot_params = {
                "appid": "9ffcb5785ad9617bf4e64178ac64f7b1",
                "spoken": text,
            }

            # Make the HTTP GET request to the chatbot API
            response = requests.get(chatbot_endpoint, params=chatbot_params)

            # Check the status code of the response
            if response.status_code == 200:
                if text == "":
                    chatbot_response = "说点什么嘛~"
                    play_audio(chatbot_response)

                # Get the chatbot's response from the API response
                else:
                    chatbot_response = response.json()["data"]["info"]["text"]
                    play_audio(chatbot_response)

            else:
                print("聊天机器人坏掉惹。。。")

print("Press 1 for text input; Press 2 for audio input")

while True:
    if keyboard.is_pressed("1"):
        pyautogui.keyDown("backspace")
        text_input()
    if keyboard.is_pressed("2"):
        pyautogui.keyDown("backspace")
        audio_input()