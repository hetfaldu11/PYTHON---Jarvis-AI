import webbrowser
import speech_recognition as sr
import time
import keyboard
import win32com.client
import psutil
import pyautogui
import spotipy
import threading
import os
from google import genai
from google.genai import types
from spotipy.oauth2 import SpotifyClientCredentials
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from API_KEY import GEMINI_API_KEY
speaker = win32com.client.Dispatch("SAPI.SpVoice")
# speaker.Rate = -3
def speak(text):
    speaker.Speak(text, 1)  # '1' makes it async (non-blocking)
    return text

def speak_thread(text):
    threading.Thread(target=speak, args=(text,)).start()

def stopspeak():
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

    # Open using OS-level call (or you can use webbrowser.open too)
    os.system(f'start {song_url}')  # For Windows

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

    # if "open youtube" in text.lower():
    #     os.startfile("C:/Users/LENOVO/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Chrome Apps/youtube.lnk")
    # elif "open github" in text.lower():
    #     os.startfile("C:/Users/LENOVO/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Chrome Apps/github.lnk")
    #
    # elif "open classroom" in text.lower():
    #     os.startfile(
    #         "C:/Users/LENOVO/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Chrome Apps/Google Classroom.lnk")
    # elif "open keep" in text.lower():
    #     os.startfile(
    #         "C:/Users/LENOVO/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Chrome Apps/Google Keep.lnk")
    # elif "open drive" in text.lower():
    #     os.startfile(
    #         "C:/Users/LENOVO/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Chrome Apps/Google Drive.lnk")
    if "open side panel" in text.lower():
        keyboard.send("win+a")

    elif "open file explorer" in text.lower():
        keyboard.send("win+e")

    elif "hello" in text.lower():
        speak_thread("Hello Sir! How can I help you?")

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

    if "page up" or "scroll up"  in text.lower():
        pyautogui.press("pageup")

    if "page down" or "scroll down" in text.lower():
        pyautogui.press("pagedown")

    if "scroll right" in text.lower():
        pyautogui.press("right")

    if "scroll left" in text.lower():
        pyautogui.press("left")

    if "close current tab" in text.lower():
        pyautogui.hotkey("ctrl", "w")

    if "close all tab" in text.lower():
        pyautogui.hotkey("ctrl", "shift", "w")

    if "new tab" in text.lower():
        pyautogui.hotkey("ctrl", "t")

    if "close current window" in text.lower():
        pyautogui.hotkey("alt", "f4")

    if "click" in text.lower():
        keyboard.send("enter")

    if "press" in text.lower():
        keyboard.send(text.split(" ")[1])

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
        answer=generate("gemini "+text[4:])
        speak_thread(answer)

    if "stop" == text.lower():
        stopspeak()

