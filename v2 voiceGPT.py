from dotenv import load_dotenv, dotenv_values, set_key
from openai import OpenAI
from pathlib import Path
import os
import wave
import time
import threading
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import pyaudio
import pygame

load_dotenv('.env')


def click_handler():
    if currently_recording.get():
        currently_recording.set(False)
        record_button.configure(fg_color=green_color.get(), text='Record')
        print('Recording stopped')
    else:
        currently_recording.set(True)
        record_button.configure(fg_color=red_color.get(), text='Stop \n Recording')
        
        print('Recording started')

        # threading runs the recording process PARALLEL to the GUI process.
        threading.Thread(target=record).start()

def record():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, 
                        input=True, frames_per_buffer=1024)

    frames = []

    start = time.time()

    while currently_recording.get():
        data = stream.read(1024)
        frames.append(data)

        passed = time.time() - start
        secs = passed % 60
        mins = passed // 60

        # :02d adds zeros if there's no value, i.E. 8 will be 08.
        status_message.set(f'{int(mins):02d}:{int(secs):02d}')

    stream.stop_stream()
    stream.close()
    audio.terminate()

    sound_file = wave.open(f'audio_prompt.wav', 'wb') #wb = write bytes
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

    print('Recording file saved.')
    status_message.set('Prompt is being sent.')

    client = OpenAI() # gets key using os.environ.get('OPENAI_API_KEY')

    ## Send audio_prompt to OpenAI for transcription.
    audio_file = open('audio_prompt.wav', 'rb')
    transcription = client.audio.transcriptions.create(
    model='whisper-1',
    file=audio_file
    )

    text_prompt = transcription.text
    print(f'Your prompt: {text_prompt}')
    os.remove('audio_prompt.wav')

    ## Send text_prompt to OpenAI for a GPT_answer.  
    completion = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[
        # {'role': 'system', 'content': 'You're a human, not a computer. Answer like in a human conversiation, not like an assistant.'},
        {'role': 'user', 'content': text_prompt}
    ]
    )

    gpt_answer = str(completion.choices[0].message.content)
    print(f'GPT Answer: {gpt_answer}')
    status_message.set('Answer is being processed.')

    ## Send the gpt_answer to OpenAI for a speech_output
    speech_file_path = Path(__file__).parent / 'speech_output.mp3'
    response = client.audio.speech.create(
    model='tts-1',
    voice='shimmer',
    input=gpt_answer
    )

    response.write_to_file(speech_file_path)

    ## Read out the answer and delete the audio files.
    pygame.mixer.init()
    pygame.mixer.music.load('speech_output.mp3')
    pygame.mixer.music.play()

    # Initially call check_playback to monitor the audio playback
    check_playback()
    
    os.remove('speech_output.mp3')


def check_playback(): # Separate function needed to correctly detect playback.
    if pygame.mixer.music.get_busy():
        # If still playing, update the status and check again after a short delay
        status_message.set('ChatGPT is talking.')
        window.after(100, check_playback)  # Check again after 100 milliseconds
    else:
        # Once playback is finished, update the status message
        status_message.set('Start next conversation \n by recording your prompt.')


def open_settings_window():
    settings_window = ctk.CTkToplevel(window)  # `window` refers to main application window
    settings_window.title('voiceGPT – Settings')
    
    # Define window size
    window_width = 500
    window_height = 300

    # Place window in center of screen
    screen_width = settings_window.winfo_screenwidth()
    screen_height = settings_window.winfo_screenheight()
    x = (screen_width/2) - (window_width/2)
    y = (screen_height/2) - (window_height/2)
    settings_window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

    # Load .env file for API Key
    env_values = dotenv_values('.env') # Load the values from the .env file into a dictionary
    api_key = env_values.get('OPENAI_API_KEY', '') # Get the value corresponding to the specified key or default to empty string
    
    # API Key Entry Field
    explanation_label = ctk.CTkLabel(settings_window, font=('Roboto light', 16), text="Please paste the OpenAI API key you want to use.", text_color=black_color.get())
    explanation_label.pack(pady=(20, 0))

    api_key_entry = ctk.CTkEntry(settings_window, width=350, show="•", placeholder_text="Paste your API key here.")
    api_key_entry.insert(0, api_key)
    api_key_entry.pack(pady=(0, 20))

    # Save Button
    save_button = ctk.CTkButton(settings_window, text="Save", command=lambda: save_settings(api_key_entry.get(), settings_window))
    save_button.pack(pady=(20, 0))

def save_settings(api_key, settings_window):
    set_key('.env', 'OPENAI_API_KEY', api_key)
    print("Settings saved:")
    messagebox.showinfo("Settings saved!", "Your settings have been saved.")
    settings_window.destroy()



# window
window = ctk.CTk(fg_color='#D6D6D6')
window.resizable(True, True)
window.title('voiceGPT')

# Define window size
window_width = 600
window_height = 400

# Get screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate x and y coordinates for the Tk root window and to be in center of screen
x = (screen_width/2) - (window_width/2)
y = (screen_height/2) - (window_height/2)
window.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

# GUI Color Scheme Variables
black_color = tk.StringVar()
black_color.set('#4D4D4D')
white_color = tk.StringVar()
white_color.set('#F5F5F5')
accent_color = tk.StringVar()
accent_color.set('#6B00C7')
green_color = tk.StringVar()
green_color.set('#02864A')
red_color = tk.StringVar()
red_color.set('#880218')

# Tkinter variables
currently_recording = tk.BooleanVar(value=False)
status_message = tk.StringVar()
status_message.set('Start the conversation \n by recording your prompt.')

# title
title_label = ctk.CTkLabel(window, text='voiceGPT', font=('Roboto bold', 24), text_color=black_color.get())
title_label.pack(pady=25)

# record button
record_button = ctk.CTkButton(window, text='Record', font=('Roboto bold', 20), fg_color=green_color.get(), corner_radius=15, height=100, command=click_handler)
record_button.pack(pady=[20, 5])

# Status Message
status_label = ctk.CTkLabel(master=window, font=('Roboto light', 16), textvariable=status_message, text_color=black_color.get())
status_label.pack(pady=5)

# settings button
settings_button = ctk.CTkButton(window, text="Settings", fg_color=black_color.get(), command=open_settings_window)
settings_button.pack(pady=20, side='bottom')

# run
window.mainloop()