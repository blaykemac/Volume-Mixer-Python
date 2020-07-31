from __future__ import print_function
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume, IAudioEndpointVolume
import time
import serial
from MixerConstants import *
#from Channel import Pin
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL

class Utilities:
    def __init__(self):
        pass
    
    def normalise(self, value, normal_value):
        return value / normal_value
        

class SerialDecoder:
    def __init__(self):
        pass
    
    def decode_serial_string(self, serial_string):
        return list(map(int, serial_string.decode("utf-8").strip().split(",")))

class Pin:
    def __init__(self,pin,processes,name = "Default"):
        self.name = name
        self.pin = pin
        self.processes = processes
    
    def get_pin_index(self):
        return self.pin
        
    def get_processes(self):
        return self.processes
    
    def set_process_volume(self, session):
        pass
        
class ConfigParser:
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

    def __init__(self, pin_list):
        self.pin_list = pin_list
        self.pins = []
        self.create_pins()

    def create_pins(self):
        for pin_index in range(len(self.pin_list)):
            #if (self.pin_list[pin_index] # 
            pin = Pin(pin_index, self.pin_list[pin_index])
            self.pins.append(pin)
    
    def get_pins(self):
        return self.pins

def main():

    # Parse configuration file and determine hardware to software pin mapping
    parser = ConfigParser(Constants.CONFIG_NAME)
    pin_creator = PinCreator(parser.get_pins())
    pins = pin_creator.get_pins()
    
    # Import utilities
    utility = Utilities()
    
    # Setup serial connection
    serial_decoder = SerialDecoder()
    
    # Check if connection successful
    #try error?
    serial_interface = serial.Serial(Constants.COM, Constants.BAUDRATE)
    
    
    # Enter infinite loop where we constantly check the serial port and change volume if needed
    
    # Initialise zeroes list 
    old_values = [0 for pin in range(Constants.PINS_USED)]
    
    # Flush junk from buffer before intial decode
    serial_read = serial_interface.readline()
    serial_interface.reset_input_buffer()
    print(serial_read) #debug only
    
    while True:
    
        time.sleep(0.25) # Sleep for 10ms until next sensor reading
        
        # READ SERIAL PORT
        serial_read = serial_interface.readline()
        #serial_interface.reset_input_buffer()
        if serial_read == "":
            print("strings are same")
            continue
        print(serial_read) #debug only
        new_values = serial_decoder.decode_serial_string(serial_read)
        normalised_values_float = [utility.normalise(ADC_level,Constants.ADC_MAX_LEVEL) for ADC_level in new_values]
        
        if (new_values == old_values):
            # Then don't adjust volume
            continue
            
        else:
        
            # Update all current audio applications
            
            # Change the master volume
            for pin in pins:
                pass
                
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(normalised_values_float[0], None) #Hard coded master but might remove 


            # Change the processes not affected by other
            
            
            # Check for individual processes and adjust according to the pin the process belongs to
            
            sessions = AudioUtilities.GetAllSessions()
            session_names = [[session, session.Process.name()] for session in sessions if session.Process]
            
            for session_pair in session_names:
                for pin in pins:
                    if (session_pair[1] in pin.get_processes()):
                        volume = session_pair[0]._ctl.QueryInterface(ISimpleAudioVolume)
                        #print(session_pair[1])
                        #print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
                        volume.SetMasterVolume(normalised_values_float[pin.get_pin_index()], None)
                    
            old_values = new_values
            
        


if __name__ == "__main__":
    main()

