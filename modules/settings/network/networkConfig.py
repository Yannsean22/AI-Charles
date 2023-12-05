import platform
import subprocess
import requests
import time

import main
import modules.inputs.windowCanvas as windowCanvas


def is_network_enable():

    try:
        result = subprocess.check_output(["nmcli", "-t", "-f", "wifi", "general"]).decode("utf-8")
        network_status = result.strip()
        return network_status == "enabled"
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False


def enable_network():
    
    try:
        subprocess.check_output(["nmcli", "radio", "wifi", "on"])
        return "Network turned on"
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return "Sorry, I ran into a problem"

def disable_network():
    
    try:
        subprocess.check_output(["nmcli", "radio", "wifi", "off"])
        return "Network turned off"
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return "Sorry, I ran into a problem"

def get_network_ssid():
    system = platform.system()
        
    try:
        result = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"]).decode("utf-8")
        lines = result.strip().split('\n')
        for line in lines:
            active, ssid = line.split(':')
            if active == 'yes':
                return ssid

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def get_Status():
    try:
        response = requests.get("https://www.example.com", timeout=120)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Error: {e}")
        return False

def get_avalible_network():

    try: 
        results = subprocess.check_output(["nmcli", "-t", "-f", "ssid", "dev", "wifi"]).decode("utf-8")
        networks = results.strip().split('\n')
        return networks
    
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return ["No avalible network"]
    

def connect_to_new_network(ssid, password):

    try: 
        subprocess.check_output(["nmcli", "dev", "wifi", "connect", ssid, "password", password], timeout=120)
        result = get_Status()
        if result == True:
            return f"Connected to {ssid}"
    except subprocess.CalledProcessError as e:
        print(f"Erro: {e}")
        return f"Sorry, Could not connect to {ssid}"


    

#showing

def showSettings():
    settings = []
    selection = windowCanvas.windowCanvas('list',settings)


def showNetworkSettings():
    settingsOptions = ["Turn Network On or Off", "New Connection"]
    selections = windowCanvas.windowCanvas("list",settingsOptions, "Network Settings")

    if selections == "Turn Network On or Off":
        check = is_network_enable()
        if check == True:
            main.speak("Would you like me to turn off network")
            command = main.confirmProcess()

            if command == "Yes":
                trial = disable_network()
                main.speak(trial)
        else:
            main.speak("Would you like me to turn on network")
            command = main.confirmProcess()

            if command == "Yes":
                trial = enable_network()
                main.speak(trial)

    elif selections == "Network Status":
        pass

    elif selections == "New Connection":
        main.speak("Would like to set up a new connection")
        command = main.confirmProcess()

        if command == "Yes":
            main.speak("Please choose a network then enter the password")
            avalibleNetwork = get_avalible_network()
            network = windowCanvas.windowCanvas("list",avalibleNetwork)
            main.speak("Please enter the password, leave empty if there is not one")
            password = windowCanvas.windowCanvas("key")

            trial = connect_to_new_network(network, password)

            main.speak(trial)
 




