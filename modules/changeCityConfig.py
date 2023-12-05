import os

import modules.inputs.windowCanvas as windowCanvas
import modules.settings.power.powerConfig as powerConfig
import main

def modifyContent(city, code):
    try:
        full_path = os.path.join(os.path.expanduser("~/Desktop"), "MagicMirror/config/config.js")

        with open(full_path, 'r') as file:
            lines = file.readlines()

        lines[0] = f"let data = ['{city}', '{code}'] \n"

        with open(full_path, 'w') as file:
            file.writelines(lines)
    except FileNotFoundError:
        print("Not Found")
        print(full_path)
    except Exception as e:
        print(f"Error: {e}")

def showCityOptions():
    options = ["Bozeman", "Londonderry", "Manchester","Waukesha"]
    select = windowCanvas.windowCanvas('list', options, 'Please choose a city')

    if select == options[0]:
        modifyContent(select, '5641727')
    elif select == options[1]:
        modifyContent(select, '5088905')
    elif select == options[2]:
        modifyContent(select, '5089178')
    elif select == options[3]:
        modifyContent(select, '5278052')