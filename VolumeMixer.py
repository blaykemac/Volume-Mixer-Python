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
        
    
    def set_process_volume(self):
        
    
    def parse_config(self):
    
def createMixer():
    global content
    with open(Constants.CONFIG_NAME,'r') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
		
        
    

def main():
    createMixer()
    pin_number = 0
    for item in content:
        if "-" not in item and ".exe" not in item:
            continue    
            
        elif ".exe" not in item:
            #then the item is a pin
            
            pin_number += 1
            
    for pin_number in range(Constants.PINS_USED):
        pin = Pin()
    print(content)
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



# import ctypes #process find
# import time   #sleep
# from pycaw.pycaw import AudioUtilities #mute


# while True:
    # EnumWindows = ctypes.windll.user32.EnumWindows    
    # EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    # GetWindowText = ctypes.windll.user32.GetWindowTextW
    # GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    # IsWindowVisible = ctypes.windll.user32.IsWindowVisible
    # ####### Modules to gather data
    # time.sleep(5)      #Sleep between checks (in seconds)
    # titles = [] #Empty list for titles (As String Objects)
    # def foreach_window(hwnd, lParam):
        # if IsWindowVisible(hwnd):
            # length = GetWindowTextLength(hwnd)
            # buff = ctypes.create_unicode_buffer(length + 1)
            # GetWindowText(hwnd, buff, length + 1)
            # titles.append(buff.value)
        # return True
    # EnumWindows(EnumWindowsProc(foreach_window), 0)
    
    # #print(titles)
    # #print(len(titles))
    # for title in titles:
        # if "Spotify" in title:
            # print("Spotify found" + str(title))
            # print(titles)
    
    
    # if "Advertisement" in titles:  #Spotify app is named as Advertisement
        # sessions = AudioUtilities.GetAllSessions()
        # for session in sessions:
            # volume = session.SimpleAudioVolume
            # volume.SetMute(1, None)
    # elif "Spotify" in titles:      #App named as Spotify(Only when ad plays, else it's Spotify Free)
        # sessions = AudioUtilities.GetAllSessions()
        # for session in sessions:
            # volume = session.SimpleAudioVolume
            # volume.SetMute(1, None)
    # else:
        # sessions = AudioUtilities.GetAllSessions()
        # for session in sessions:
            # volume = session.SimpleAudioVolume
            # volume.SetMute(0, None)