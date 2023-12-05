import main
import sys
import subprocess

import modules.inputs.windowCanvas as windowCanvas

def turnPowerOFF():
    subprocess.run(['shutdown','-h','now'])

def restartDevice():
    subprocess.run(['reboot'])

def poweroffDelay(minutes):
    restart_time = f"+{minutes} minutes"

    restart_command = 'reboot'

    subprocess.run(['at', restart_time], input=restart_command.encode())

def showPowerConfig():
    powerOptions = ["Turn Off Device", "Restart Device", "Set Poweroff time -- minutes"]

    selection = windowCanvas.windowCanvas('list', powerOptions,'Power Settings')

    if selection == "Turn Off Device":
        main.speak("Would you like to turn off the Device ?")
        confirm = main.confirmProcess()

        if confirm == 'Yes':
            main.speak('Goodbye!!')
            turnPowerOFF()
    
    elif selection == "Restart Device":
        main.speak("Would you like to restart the device")
        confirm = main.confirmProcess()

        if confirm == 'Yes':
            main.speak('see you soon!!')
            restartDevice()
        
    elif selection == "Set Poweroff time -- minutes":
        
        main.speak("Would you like to schedule a power off?")
        command = main.listen().lower()

        if 'yes' in command or 'sure' in command:
            timeFrame = ["1 min.","5 min.","15 min.","30 min.","1 Hours","2 Hours"]
            main.listen("Please select the how long")
            selection = windowCanvas.windowCanvas("list",timeFrame,"Select Power Off time")

            if selection == "1 min.":
                poweroffDelay(1)
                main.listen("Restarting in one minutes")
            elif selection == "5 min.":
                poweroffDelay(5)
                main.listen("Restarting in five minutes")
            elif selection == "15 min.":
                poweroffDelay(15)
                main.listen("Restarting in fifteen minutes")
            elif selection == "30 min.":
                poweroffDelay(30)
                main.listen("Restarting in thirty minutes")
            elif selection == "1 Hours":
                poweroffDelay(60)
                main.listen("Restarting in one hour")
            elif selection == "2 Hours":
                poweroffDelay(120)
                main.listen("Restarting in two hour")
            
