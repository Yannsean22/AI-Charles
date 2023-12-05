#provides settings holders

import main
import sys
import subprocess

import modules.inputs.windowCanvas as windowCanvas

#settings options
import modules.settings.network.networkConfig as networkConfig
import modules.settings.bluetooth.bluetoothConfig as bluetoothConfig
import modules.settings.power.powerConfig as powerConfig
import modules.settings.about.aboutConfig as aboutConfig
import modules.changeCityConfig as changeCityConfig
def showSettingsOptions():
    main.invokeCharles()
    settingsOptions = ["About", "Network", "Bluetooth", "Power","Change Location", "More updates coming soon!!"]
    selectedSettings = windowCanvas.windowCanvas("list", settingsOptions)
    
    if selectedSettings == 'About':
        aboutConfig.showAboutConfig()
    elif selectedSettings == 'Network':
        networkConfig.showNetworkSettings()
    elif selectedSettings == 'Bluetooth':
        bluetoothConfig.showBluetoothSettings()
    elif selectedSettings == 'Change Location':
        changeCityConfig.showCityOptions()
    elif selectedSettings == 'Power':
        powerConfig.showPowerConfig()
    
