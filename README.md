# voiceGPT: A Voice-Interactive ChatGPT Experience

This app let's you voice interact with ChatGPT instead of typing and reading.

It's amazing how ChatGPT responds almost like a real human, right?
But don't you feel like typing your question and then reading it's answer greatly worsens this feeling of having a real human assistant?

Yep, me too!

Introducing: voiceGPT! 
Now you can just speak to ChatGPT and listen to the answer. Like real humans do when they communicate.

## 📱 What it does
– Listens to your prompt (audio recording)  
– Converts your voice-prompt into text (using OpenAI's Speech-To-Text)  
– Sends your (now written) prompt to ChatGPT (using OpenAI's API)  
– Gets an answer from ChatGPT (using OpenAI's API)  
– Turns the (written) answer into speech (using OpenAI's Text-To-Speech)  
– Plays the audio file

## 🌍 Language Support
You can expect good results when transcribing the following languages:  
Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Chinese, Croatian, Czech, Danish, Dutch, English, Estonian, Finnish, French, Galician, German, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Italian, Japanese, Kannada, Kazakh, Korean, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Portuguese, Romanian, Russian, Serbian, Slovak, Slovenian, Spanish, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, and Welsh.  

Other languages might work, but the results may be of low quality.  

You can read more in the OpenAI documentation [here](https://platform.openai.com/docs/guides/speech-to-text/quickstart).  

## Requirements  

1. **OpenAI Plus Account:** To use this script, you need an OpenAI Plus account, which costs $20 per month.
2. **Available Balance:** Ensure you have a sufficient balance in your OpenAI Plus account. You can check your balance [here](https://platform.openai.com/account/billing/overview).
   - Your OpenAI Plus account operates similarly to a phone plan with both a monthly subscription and a prepaid balance. Make sure you have funds in your prepaid balance.
  
## Setup

1. **API Key:** Generate a personal API key for yourself [here](https://platform.openai.com/api-keys). Do not share this key with anyone.
2. **Download the Script:** Download the script "v2 voiceGPT.py" to your local machine.
3. **Install Dependencies:** Make sure you have the following dependencies installed:

```bash
pip install python-dotenv
pip install --upgrade openai
pip install customtkinter
pip install pyaudio
pip install pygame
```

4. **Run the Script:** On first execution navigate to "Settings" and enter the API Key you want to use. Your key will then be stored in an .env file locally in the same folder as the script. Your key will not be shared. Do not share your key.
5. **Test it out:** Click "Record" and start speaking. Have fun!  

You can monitor the usage of your balance [here](https://platform.openai.com/usage). This way you always keep an overview of the cost of your usage.

## ⚠️ Disclaimers
- **AI-Generated Responses**: Remember, the voice you hear is AI-generated. ChatGPT doesn't embody a real person. Always cross-verify crucial information.
- **Beginner's Creation**:  I'm a beginner. I made this project because I wanted to learn how to work with an API in python and how to create a GUI. This code was made for my own learning purposes and might be buggy. Use it at your own risk.

![logo-color-wide](https://github.com/jonasclick/TalkGPT/assets/93444574/4e3cf9ee-40c7-4e5c-9314-ae01b0d21977)

---

Embrace this unique way to engage with AI. **voiceGPT** awaits to amaze you with every conversation. Let's break the barriers between human and machine - one voice prompt at a time.
