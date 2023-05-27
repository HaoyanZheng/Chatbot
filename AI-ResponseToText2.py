import requests
import googletrans
from playsound import playsound

# Replace YOUR_API_KEY with your actual VoiceVox API key
voicevox_api_key = "i-V-38a071k167W"

# Replace YOUR_CHATBOT_API_KEY with your actual chatbot API key
chatbot_api_key = "9ffcb5785ad9617bf4e64178ac64f7b1"

# Set the base path to the user's OneDrive folder
path = "D://WAIFU//audio.wav"

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

# Prompt the user for input
text = input("Please enter the text to be read out loud: ")

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
        response = requests.get(voicevox_endpoint, headers=voicevox_headers, params=voicevox_params)

        # Check the status code of the response
        if response.status_code == 200:
            # Choose a file name and location to save the audio file
            file_name = "audio.wav"
            file_path = path

            # Save the audio data to the specified file
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Audio file saved to {file_path}")

            # Replace "D://WAIFU//audio.wav" with the actual path to the WAV file
            playsound(r"audio.wav")
        else:
            print(f"Error: VoiceVox API request failed with status code {response.status_code}")
    else:
        print("Error: Chatbot returned an empty response.")
else:
    print(f"Error: Chatbot API request failed with status code {response.status_code}")
