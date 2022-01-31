from __future__ import print_function
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
import time
import serial
from MixerConstants import *
#from Channel import Pin
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from infi.systray import SysTrayIcon # used for windows system tray
import sys

class Utilities:
    """
    Useful functions such as normalising ADC value to float as Windows Volume Mixer only accepts normalised floats.
    """
    def normalise(value, normal_value):
        return value / normal_value
        

class SerialDecoder:
    """
    Object to parse serialised message and separate slider values and mute statuses.
    """
    def __init__(self):
        pass
    
    def decode_serial_string(self, serial_string):
        return list(map(int, serial_string.decode("utf-8").strip().split(",")))

class Pin:
    """
    Pin object that stores information about each pin such as volume, mute status, programs allocated to pin, and also manages Windows API calls to Windows Volume Mixer.
    """
    def __init__(self,pin,processes,name = "Default"):
        self.name = name
        self.pin = pin
        self.processes = processes
        self.mute = False
        self.volume = 0
        self.setup = True

    def get_pin_name(self):
        return self.name
    
    def get_pin_index(self):
        return self.pin
        
    def get_processes(self):
        return self.processes
    
    def set_process_volume(self, session, level):
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume.SetMasterVolume(level, None)
        
    def set_process_mute(self, session, level):
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        volume.SetMute(level, None)
        
    def update(self, slider_value, mute_value, volume_interface, sessions):
        if slider_value != self.volume or self.setup:
            
            self.volume = slider_value
            volume_normalised = Utilities.normalise(slider_value, Constants.ADC_MAX_LEVEL)
            
            if (self.get_pin_index() == Constants.PIN_MASTER):
                volume_interface.SetMasterVolumeLevelScalar(volume_normalised, None)
                
            #elif (pin.get_pin_index == Constants.PIN_OTHER):
                #Need to complete later
                #pass
                
            else:
                for session in sessions:
                    if (session.Process.name() in self.get_processes()):
                        self.set_process_volume(session, volume_normalised)
                        
        
        if mute_value != int(self.mute) or self.setup:
            
            self.mute = bool(mute_value)
            
            if self.setup:
                self.setup = False
                
    
            if (self.get_pin_index() == Constants.PIN_MASTER):
                    volume_interface.SetMute(mute_value, None)
                    
                #elif (pin.get_pin_index == Constants.PIN_OTHER):
                    #Need to complete later
                    #pass
                    
            else:
                for session in sessions:
                    if (session.Process.name() in self.get_processes()):
                        self.set_process_mute(session, mute_value)

class ConfigParser:
    """
    Object to extract software-to-pin allocation from configuration file
    """
    def __init__(self, config_name):
        self.config_name = config_name
        self.extract_config()
       
    def extract_config(self):
        with open(self.config_name,'r') as f:
            self.config = f.readlines()
            self.config = [channel.strip().split(",") for channel in self.config]

    def get_pins(self):
        return self.config
        
        
class PinCreator:
    """
    Object to instantiate and manage pin objects
    """
    def __init__(self, pin_list):
        self.pin_list = pin_list
        self.pins = []
        self.create_pins()

    def create_pins(self):
        for pin_index in range(len(self.pin_list)):
            #
            if pin_index == Constants.PIN_MASTER:
                pin = Pin(pin_index, self.pin_list[pin_index], Constants.PIN_MASTER_STRING)
                
            else:
                pin = Pin(pin_index, self.pin_list[pin_index])
            self.pins.append(pin)
    
    def get_pins(self):
        return self.pins

def on_quit_callback(systray):
    #systray.shutdown()
    #sys.exit(0)
    global exit_signalled
    exit_signalled = True

def main():

    # Setup windows system tray icon
    
    def say_hello(systray): print("Hello, World!")
    #menu_options = (("Say Hello", None, say_hello),)
    
    #systray = SysTrayIcon("icon.ico", "Volume Mixer", menu_options, on_quit=on_quit_callback)
    """
    menu_options = ()
    systray = SysTrayIcon("icon.ico", "Volume Mixer", menu_options)
    systray.start()
    """
    
    # Parse configuration file and determine hardware to software pin mapping
    parser = ConfigParser(Constants.CONFIG_NAME)
    pin_creator = PinCreator(parser.get_pins())
    pins = pin_creator.get_pins()
    
    # Import utilities
    utility = Utilities()
    
    # Create serial decoding object to be ready later for connection
    serial_decoder = SerialDecoder()
    
    #Initialise master output and instantiate windows API objects
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    global exit_signalled
    
    # Loop continuously trying to connect to serial port. If successful, start reading serial values
    while not exit_signalled:
        try:
            # Connect for first time or try reconnecting if connection failed previously
            serial_interface = serial.Serial(Constants.COM, Constants.BAUDRATE)
            
            # Flush junk from buffer before intial decode
            serial_read = serial_interface.readline()
            serial_interface.reset_input_buffer()
    
            while not exit_signalled:
            
                time.sleep(0.05) # Sleep for 50ms before checking for next sensor reading
                
                # READ SERIAL PORT
                serial_read = serial_interface.readline()
                
                #serial_interface.reset_input_buffer()
                print(serial_read) #debug only
                
                #If we receive an empty string, then no data to process
                if serial_read == "":
                    print("strings are same")
                    continue
                                    
                else:
                    #Extract the desired volume levels and mute statuses
                    message = serial_decoder.decode_serial_string(serial_read) # assume data is [slider0, .., slider7, switch0, .., switch7]
                    
                    # Separate slider values from mute booleans
                    pin_values = message[0:8]
                    pin_mutes = message[8::]
                    pin_mutes = [(1 + val) % 2 for val in pin_mutes] # Invert as a switch in "up" position should correspond to a 0, not a 1.
                
                    # Update list of all current audio applications
                    sessions = [session for session in AudioUtilities.GetAllSessions() if session.Process] #Make sure session exists
                       
                    #Iterate all pins and check if they need to be updated
                    for index, pin in enumerate(pins):
                        print("mute" + str(pin_mutes[index]))
                        pin.update(pin_values[index], pin_mutes[index], volume, sessions)
                    
        except serial.serialutil.SerialException:
            print("No serial device found. Waiting 1 second...")
            time.sleep(1)
            pass


if __name__ == "__main__":
    exit_signalled = False
    menu_options = ()
    #systray = SysTrayIcon("icon.ico", "Volume Mixer", menu_options)
    systray = SysTrayIcon("VolumeIcon.ico", "Volume Mixer", menu_options, on_quit=on_quit_callback)
    systray.start()
    main()


