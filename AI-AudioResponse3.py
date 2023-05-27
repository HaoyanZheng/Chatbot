import requests
import googletrans
from playsound import playsound
import os
import openai
import tempfile
import requests #for getting the content of a html
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

# Replace YOUR_CHATBOT_API_KEY with your actual OpenAI API key
openai.api_key = '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'

# Replace YOUR_VOICEVOX_API_KEY with your actual VoiceVox API key
voicevox_api_key = 'i-V-38a071k167W'

# Set the VoiceVox API endpoint and headers
voicevox_endpoint = "https://api.su-shiki.com/v2/voicevox/audio/"
voicevox_headers = {
    "Authorization": f"Bearer {voicevox_api_key}"
}

# initialize sound source
sound_source = 0

# initialize sound library
sound_library = {2: "四国めたん-ノーマル", 0: "四国めたん-あまあま", 6: "四国めたん-ツンツン", 4: "四国めたん-セクシー", 36: "四国めたん-ささやき", 37: "四国めたん-ささやき", 3: "ずんだもん-ノーマル", 1: "ずんだもん-あまあま", 7: "ずんだもん-ツンツン", 5: "ずんだもん-セクシー", 22: "ずんだもん-ささやき", 38: "ずんだもん-ヒソヒソ", 8: "春日部つむぎ-ノーマル", 10: "雨晴はう-ノーマル", 9: "波音リツ-ノーマル", 11: "ノーマル", 12: "白上虎太郎-ふつう", 32: "白上虎太郎-わーい", 33: "白上虎太郎-びくびく", 34: "白上虎太郎-おこ", 35: "白上虎太郎-びえーん", 13: "青山龍星-ノーマル", 14: "冥鳴ひまり-ノーマル", 16: "冥鳴ひまり-ノーマル", 15: "冥鳴ひまり-あまあま", 18: "冥鳴ひまり-ツンツン", 17: "冥鳴ひまり-セクシー", 19: "冥鳴ひまり-ささやき", 20: "もち子さん-ノーマル", 21: "剣崎雌雄-ノーマル", 23: "WhiteCUL-ノーマル", 24: "WhiteCUL-たのしい", 25: "WhiteCUL-かなしい", 26: "WhiteCUL-びえーん", 27: "後鬼-人間ver.", 28: "後鬼-ぬいぐるみver.", 29: "No.7-ノーマル", 30: "No.7-アナウンス", 31: "No.7-読み聞かせ"}

def friend_chat(all_text,prompt0 = "",call_name = '南ことり'):
  start_sequence = '\n'+str(call_name)+':'
  restart_sequence = "\nYou: "
  all_text = all_text + restart_sequence
  if prompt0 == '':
     prompt0 = input(restart_sequence) #当期prompt
  if prompt0 == 'quit':
     return prompt0
  prompt = all_text + prompt0 + start_sequence


  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0.5,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.0,
    stop=["\nYou:"]
  )
  audio_text = response['choices'][0]['text'].strip()
  print(start_sequence + response['choices'][0]['text'].strip())
  all_text = prompt + response['choices'][0]['text'].strip()
  return prompt0,all_text,audio_text

def play_audio(chatbot_response):
        print("She says: " + chatbot_response)

        # Translate the chatbot's response into Japanese
        translator = googletrans.Translator()
        src_lang = translator.detect(chatbot_response).lang
        chatbot_response_ja = translator.translate(chatbot_response, dest='ja', src=src_lang).text
        print("She says: " + chatbot_response_ja)

        # Set the query parameters for the VoiceVox API request
        voicevox_params = {
            "text": chatbot_response,
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


if __name__ == '__main__':
  all_text = input('输入初始设定文本:')
  while True:
    resualt,all_text,audio_text = friend_chat(all_text)
    play_audio(audio_text)
    if resualt == 'quit':
      break