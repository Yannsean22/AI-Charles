#Cubex - Charles 0.0.1 built by Yann Kabambi - Crystal Ice for Meredith Teuber
import speech_recognition as sr
import pyttsx3
import pygame
import random
import time

import modules.settings.settingsConfig as settingsConfig
import modules.settings.network.networkConfig as networkConfig
import modules.settings.bluetooth.bluetoothConfig as bluetoothConfig
import modules.inputs.windowCanvas as windowCanvas

# Media assets
CharlesListeningSound = './assets/Charles-listeningSound.mp3'
CharlesThinkingSound = './assets/Charles-thinkingSound.mp3'

charlesInvoke = ["Yes", "How can I help you?", "", "Hello, how can I help?"]
general_greetings = ["hello", "hi", "hey", "greetings", "howdy", "hi there", "hello there", "hey there", "hello good to have you", "hey what's up", "hi it's good to see you","hello friend", "hi stranger"]

# Define Listening / Thinking Sound
def play_sound(file_path, volume=0.95):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(volume)
    sound.play() 

def listeningSound():
    play_sound(CharlesListeningSound)

def thinkingSound():
    play_sound(CharlesThinkingSound)

def confirmProcess():
    options = ['Yes', 'No']
    result = windowCanvas.windowCanvas('list',options,"Please Choose: ")

    return result
# Define Charles
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return "Could not understand"

    except sr.RequestError as e:
        return f"Error: {e}"

#General Handles
def handlePassThru():
    speak(f"What would you like to configure? {time.sleep(1)} Please say options to hear what the are.")
    command = listen().lower()
    return command


#Network



#Settings

def continueCommand():
    listeningSound()
    command = listen().lower()
    return command


def processCommand(command):
    if command in general_greetings:
        greet = random.choice(general_greetings)
        speak(f"g{greet}, how can I help")
        command = continueCommand()
        processCommand(command)

    elif ("network" in command and "settings" in command ) or ("network" in command and "setting" in command):
        speak("Here are the network settings")
        networkConfig.showNetworkSettings()
    
    elif ("bluetooth" in command and "settings" in command ) or ("blutooth" in command and "setting" in command):
        speak("Here are the bluetooth settings")
        bluetoothConfig.showBluetoothSettings()

    elif "settings" in command or "configuration" in command:    
        settingsConfig.showSettingsOptions()
       

def invokeCharles():
    charles_greet = random.choice(charlesInvoke)
    speak(charles_greet)
    thinkingSound()


if __name__ == "__main__":
    windowCanvas.showFace()
            
