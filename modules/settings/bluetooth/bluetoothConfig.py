#sets Bluetooth prefrences and connection
import main
import sys
import subprocess


import modules.inputs.windowCanvas as windowCanvas

def BT_On():
    try:
        subprocess.run(['rfkill', 'unblock', 'bluetooth'], check=True)
        return 'Bluetooth turned on'
    except subprocess.CalledProcessError as e:
        print(f"Bluetooth Error: {e}")

def BT_OFF():
    try:
        subprocess.run(['rfkill', 'block', 'bluetooth'],check=True)
        return 'Bluetooth turned off'
    except subprocess.CalledProcessError as e:
        print(f"Bluetooth Error: {e}")

def BT_current_connections():
    try:
        result = subprocess.run(['bluetoothctl', 'devices'], capture_output=True, text=True, check=True)

        return result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def BT_pair_new_device():
    pass

def BT_search_device():

    try:
        result = subprocess.run(['hcitool', 'scan'], capture_output=True, text=True, check=True)

        lines = result.stdout.strip().split('\n')[1:]
        devices = []
        for line in lines:
            devices.append(line)

        return devices

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")   

def get_New_Device_Address(string):

    new_string = []
    count = 0
    
    while True:
        if count != 19:
            new_string.append(string[count])
            count +=1
        else:
            break

    return ''.join(new_string)

def connect_to_device(address):
    try:
        bluetoothctl = subprocess.Popen(['bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

        commands = [
            f"trust {address}",
            f"pair {address}",
            f"connect {address}",
            "exit"
        ]

        for cmd in commands:
            bluetoothctl.stdin.write(cmd + '\n')
            bluetoothctl.stdin.flush()

        bluetoothctl.wait()

        return "Device Paired"
    
    except subprocess.CalledProcessError as e:
        print(f"bluetooth Error: {e}")


def showBluetoothSettings():
    bluetoothOption = ["Turn On","Turn Off", "Show current connections", "Pair new device"]

    selection = windowCanvas.windowCanvas("list",bluetoothOption,"Blutooth Settings")

    if selection == bluetoothOption[0]:
        main.speak("Would you like to turn on bluetooth")
        confirm = main.confirmProcess()
        if confirm == "Yes":
            process = BT_On()
            main.speak(process)
    elif selection == bluetoothOption[1]:
        main.speak("Would you like to turn off bluetooth")
        confirm = main.confirmProcess()
        if confirm == "Yes":
            process = BT_OFF()
            main.speak(process)
    elif selection == bluetoothOption[2]:
        connections = BT_current_connections()
        windowCanvas.windowCanvas('list',connections, 'Current Bluetooth Connections')
    elif selection == bluetoothOption[3]:
        main.speak("Searching for devices")
        devices = BT_search_device()
        selected = windowCanvas.windowCanvas('list',devices,'Found devices')
        address = get_New_Device_Address(selected)
        connected = connect_to_device(address)

        main.speak(connected)