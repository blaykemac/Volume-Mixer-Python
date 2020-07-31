from __future__ import print_function
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import time
import serial
from MixerConstants import *
#from Channel import Pin

class Pin:
	def __init__(self,name = "Default",pin,processes):
		self.name = name
		self.pin = pin
        self.processes = processes
            
    def set_process_volume(self, session):
        
class ConfigParser:
    def __init__(self, config_name):
        self.config_name = config_name
        self.extract_config()
       
    
    def extract_config(self):
        with open(self.config_name,'r') as f:
            self.config = f.readlines()
            self.config = [channel.strip().split(",") for channel in self.config]"
	
    def get_pins(self):
        return self.config
        
class PinCreator:

    self.pins = []
    def __init__(self, pin_list):
        self.pin_list = pin_list
        self.create_pins()

    def create_pins(self):
        for pin_index in range(len(self.pin_list)):
            #if (self.pin_list[pin_index] # 
            pin = Pin(pin = pin_index, processes = self.pin_list[pin_index])
    
    def get_pins(self):
        return self.pins

 
 
 pin_number = 0
        temp_group = []
        
        for item in self.config:
            if "-" not in item and ".exe" not in item:
                continue    
                
            elif ".exe" not in item:
                #then the item is a pin
                
                pin_number += 1
     

def main():
    parser = ConfigParser(Constants.CONFIG_NAME)
    pin_creator = PinCreator(parser.get_pins())
    pins = pin_creator.get_pins()
    
    # Setup serial connection
    ser = serial.Serial(Constants.COM, Constants.BAUDRATE)
    
    
    # Enter infinite loop where we constantly check the serial port and change volume if needed
    
    old_value = [0 for pin in range(Constants.PINS_USED)]
    while True:
        # READ SERIAL PORT
        
        
        
        # ....
        new_value = ......
        
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            
            if session.Process and session.Process.name() == "Spotify.exe":
                print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
                volume.SetMasterVolume(0.1, None)
                
        
        old_values = new_values
        time.sleep(1)


if __name__ == "__main__":
    main()

