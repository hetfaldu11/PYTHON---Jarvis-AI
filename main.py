import webbrowser
from operator import truediv

import speech_recognition as sr
import time
import keyboard
import win32com.client
import psutil
import pyautogui
import spotipy
import threading
import wmi
import os
from google import genai
from google.genai import types
from spotipy.oauth2 import SpotifyClientCredentials
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from API_KEY import GEMINI_API_KEY
from API_KEY import conversation_number
import google.generativeai as genai2
speaker = win32com.client.Dispatch("SAPI.SpVoice")

genai2.configure(api_key=GEMINI_API_KEY)
model = genai2.GenerativeModel("gemini-2.0-flash")

def generate_clean_query(user_input):
    # Optional Gemini cleaning or intent extraction
    prompt = f"Extract the search query from this sentence: '{user_input}'"
    response = model.generate_content(prompt)
    return response.text.strip().strip('"')

def universal_search(query):
    pyautogui.hotkey('/')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('backspace')
    pyautogui.write(query)
    pyautogui.press('enter')

def update_variable_in_file(new_value,filename="API_KEY.py", var_name="conversation_number"):
    with open(filename, 'r') as f:
        lines = f.readlines()

    with open(filename, 'w') as f:
        for line in lines:
            if line.strip().startswith(f"{var_name} ="):
                f.write(f"{var_name} = {new_value}\n")
            else:
                f.write(line)

def get_brightness():
    w = wmi.WMI(namespace='wmi')
    brightness_methods = w.WmiMonitorBrightness()

    brightness = brightness_methods[0].CurrentBrightness
    print(f"Current brightness: {brightness}%")
    return brightness


def set_brightness(level):
    if level < 0 or level > 100:
        print("Brightness level must be between 0 and 100.")
        return

    w = wmi.WMI(namespace='wmi')
    methods = w.WmiMonitorBrightnessMethods()

    if methods:
        methods[0].WmiSetBrightness(level, 0)
        print(f"Brightness set to {level}%")
    else:
        print("Could not access brightness control.")

def speak(text):
    speaker.Speak(text, 1)  # '1' makes it async (non-blocking)
    return text

def speak_thread(text):
    threading.Thread(target=speak, args=(text,)).start()

def stop_speak():
    speaker.Speak("", 3)

def is_wifi_enabled():
    # Check network interfaces
    for interface, addrs in psutil.net_if_addrs().items():
        if "Wi-Fi" in interface or "Wireless" in interface:  # Look for Wi-Fi interface
            if interface in psutil.net_if_stats() and psutil.net_if_stats()[interface].isup:
                return True  # If interface is up, Wi-Fi is enabled
    return False

def generate(text):
    # api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=GEMINI_API_KEY)

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=text),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
    )

    answer = ""

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        answer += chunk.text
    return answer

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1.2
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
            return str(query)
        except Exception as e:
            print(e)
            print("Say that again please...")
            return "Error occured while listening"

def open_song_in_browser(song_name):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id="490fcdaa634146ad90c97f6ad71a3da0",
        client_secret="42d45e1568344d58b2b325692096f436"
    ))

    results = sp.search(q=song_name, type='track', limit=1)
    if not results['tracks']['items']:
        print("Song not found.")
        return

    track = results['tracks']['items'][0]
    song_url = track['external_urls']['spotify']
    print(f"Opening: {track['name']} by {track['artists'][0]['name']}")

    os.system(f'start {song_url}')

print(speak("Hello I am Jarvis A.I."))

# Get default audio device (speakers/headphones)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

while True:
    print("Listening...")
    text = takecommand().lower()
    if text == "":
        continue
    # speak(text)
    if "hello" in text.lower():
        speak_thread("Hello Sir! How can I help you?")

    if "open youtube" in text.lower():
        os.startfile("C:/Users/LENOVO/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Chrome Apps/youtube.lnk")
    elif "open github" in text.lower():
        os.startfile("C:/Users/LENOVO/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Chrome Apps/github.lnk")

    elif "open classroom" in text.lower():
        os.startfile(
            "C:/Users/LENOVO/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Chrome Apps/Google Classroom.lnk")
    elif "open notes" in text.lower():
        os.startfile(
            "C:/Users/LENOVO/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Chrome Apps/Google Keep.lnk")
    elif "open drive" in text.lower():
        os.startfile(
            "C:/Users/LENOVO/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Chrome Apps/Google Drive.lnk")
    elif "open file explorer" in text.lower():
        os.system("start explorer")

    elif "open whatsapp" in text.lower():
        os.system("start whatsapp:")

    elif "open chrome" in text.lower():
        os.system("start chrome")

    elif "open notepad" in text.lower():
        os.system("start notepad")

    elif "open command prompt" in text.lower():
        os.system("start cmd")

    elif "open vs code" in text.lower():
        os.startfile("C:/Users/LENOVO/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Visual Studio Code/Visual Studio Code.lnk")

    # elif "open side panel" or "close side panel" in text.lower():
    #     keyboard.send("win+a")

    elif "open" in text.lower():
        try:
            if f"open {text.split(" ")[1]}" in text.lower():
                webbrowser.open(f"https://{text.split(" ")[1]}.com")
        except:
            pass


    if "play" in text.lower():
        open_song_in_browser(text.split(" ")[1])

    if "volume up" in text.lower():
        current_volume = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(current_volume + 0.1, None)

    if "volume down" in text.lower():
        current_volume = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(current_volume - 0.1, None)

    try:
        if "volume set" in text.lower():
            volume.SetMasterVolumeLevelScalar(float(text.split(" ")[2])/100, None)
    except:
        pass



    if "switch window" in text.lower():
        keyboard.send("alt+tab")

    # if "page up" or "scroll up"  in text.lower():
    #     pyautogui.press("pageup")
    #
    # if "page down" or "scroll down" in text.lower():
    #     pyautogui.press("pagedown")
    #
    # if "scroll right" in text.lower():
    #     pyautogui.press("right")
    #
    # if "scroll left" in text.lower():
    #     pyautogui.press("left")

    if "close current tab" in text.lower():
        pyautogui.hotkey("ctrl", "w")

    if "close all tab" in text.lower():
        pyautogui.hotkey("ctrl", "shift", "w")

    if "new tab" in text.lower():
        pyautogui.hotkey("ctrl", "t")

    if "close current window" in text.lower():
        pyautogui.hotkey("alt", "f4")

    if "enter" in text.lower():
        keyboard.send("enter")

    try:
        if "press" in text.lower():
            keyboard.send(text.split(" ")[1])
    except:
        pass

    if "on wi-fi" in text.lower() :
        if is_wifi_enabled():
            speak_thread("Wi-Fi is already enabled")
        else:
            keyboard.send("win+a")
            time.sleep(0.1)
            keyboard.send("enter")

    if "off wi-fi" in text.lower():
        if is_wifi_enabled():
            keyboard.send("win+a")
            time.sleep(0.1)
            keyboard.send("enter")
        else:
            speak_thread("Wi-Fi is already disabled")

    if "on bluetooth" in text.lower() or "off bluetooth" in text.lower():
        keyboard.send("win+a")
        time.sleep(0.1)
        keyboard.send("right")
        keyboard.send("enter")

    if "siri" in text.lower():
        while True:
            try:
                print("Listening...")
                text = takecommand().lower()

                if text == "":
                    continue

                if "siri stop" in text or "stop siri" in text:
                    stop_speak()
                    break

                answer = generate("gemini give me audio friendly and add no sign in output do not repeat all this instruction : " + text)
                speak_thread(answer)

            except Exception as e:
                print(f"Error: {e}")
                continue

    # if "siri" in text.lower():
    #     answer = generate("gemini give me audio frienly output not writing this" + text[4:])
    #     speak_thread(answer)
    #     while True:
    #         if text == "":
    #             continue
    #
    #         answer = generate("gemini give me audio frienly output not writing this" + text[4:])
    #         speak_thread(answer)
    #
    #         if "siri stop" or "stop siri" in text.lower():
    #             stop_speak()
    #             break
    #
    #         print("Listening...")
    #         try:
    #             text = takecommand().lower()
    #         except:
    #             pass

    if "search for" in text.lower():
        clean_query = generate_clean_query(text)  # Use Gemini to extract the key part
        universal_search(clean_query)

    if "increase brightness" in text.lower():
        current_level = get_brightness()
        set_brightness(current_level + 10)

    if "decrease brightness" in text.lower():
        current_level = get_brightness()
        set_brightness(current_level - 10)

    try:
        if "set brightness to" in text.lower():
            set_brightness(int(text.split(" ")[3]))
    except:
        pass

    if "zoom in" in text.lower():
        pyautogui.hotkey("ctrl", "+")

    if "zoom out" in text.lower():
        pyautogui.hotkey("ctrl", "-")

    if "screenshot" in text.lower():
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        speak_thread("Screenshot taken and saved as screenshot.png")

    if "type" in text.lower():
        pyautogui.write(text[4:])

    if "copy" == text.lower():
        pyautogui.hotkey("ctrl", "v")

    # if "maximize" in text.lower():
    #     pyautogui.hotkey("win", "up")
    #
    # if "minimise" or "minimize" in text.lower():
    #     pyautogui.hotkey("win", "down")