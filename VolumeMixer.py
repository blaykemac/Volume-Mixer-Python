from __future__ import print_function
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import time
from MixerConstants import *
#from Channel import Pin

class Pin:
	def __init__(self,name,pin,processes):
		self.name = name
		self.pin = pin
        self.processes = processes
        
    
    def set_process_volume(self, session):
        
class ConfigParser:
    def __init__(self, config_name):
        self.config_name = config_name
        self.extract_config()
       
    
    def extract_config():
        with open(self.config_name,'r') as f:
            self.config = f.readlines()
            self.config = [channel.strip().split(",") for channel in self.config]"
		
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
            
    for pin_number in range(Constants.PINS_USED):
        pin = Pin()
    print(self.config)
    while True:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process:
                print(session.Process.name()) #debugging only
            if session.Process and session.Process.name() == "Spotify.exe":
                print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
                volume.SetMasterVolume(0.1, None)
                
        time.sleep(5)


if __name__ == "__main__":
    main()

