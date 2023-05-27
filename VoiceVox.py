import tempfile
import requests
from playsound import playsound

# Replace YOUR_API_KEY with your actual VoiceVox API key
api_key = "i-V-38a071k167W"

# Set the API endpoint and headers
endpoint = "https://api.su-shiki.com/v2/voicevox/audio/"
headers = {
    "Authorization": f"Bearer {api_key}"
}

while True:
    # Prompt the user for input
    text = input("Please enter the text to be read out loud: ")

    # Set the query parameters for the request
    params = {
        "text": text,
        "key": api_key
    }

    # Make the HTTP GET request to the VoiceVox API
    response = requests.get(endpoint, headers=headers, params=params)

    # Check the status code of the response
    if response.status_code == 200:
        # Write the audio data to a temporary file
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.wav', delete=False) as f:
            f.write(response.content)

        # Play the audio file using playsound
        playsound(f.name)
    else:
        print(f"Error: API request failed with status code {response.status_code}")