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
        self.mute = False
        self.volume = 0

    def get_pin_name(self):
        return self.name
    
    def get_pin_index(self):
        return self.pin
        
    def get_processes(self):
        return self.processes
    
    def set_process_volume(self, session, level):
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        #print(session)
        #print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
        volume.SetMasterVolume(level, None)
        
    def process_mute(self):
        if self.mute:
            pass
        else:
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
            #
            if pin_index == Constants.PIN_MASTER:
                pin = Pin(pin_index, self.pin_list[pin_index], Constants.PIN_MASTER_STRING)
                
            else:
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
    old_values = [0 for pin in range(2*Constants.PINS_USED)]
    
    # Flush junk from buffer before intial decode
    serial_read = serial_interface.readline()
    serial_interface.reset_input_buffer()
    print(serial_read) #debug only
    
    #Initialise master output
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    while True:
    
        time.sleep(0.1) # Sleep for 10ms until next sensor reading
        
        # READ SERIAL PORT
        serial_read = serial_interface.readline()
        #serial_interface.reset_input_buffer()
        print(serial_read) #debug only
        
        #If we receive an empty string
        if serial_read == "":
            print("strings are same")
            continue
            
        
        else:
            #Extract the desired volume level
            new_values = serial_decoder.decode_serial_string(serial_read)
            pin_values_normal = [utility.normalise(ADC_level,Constants.ADC_MAX_LEVEL) for ADC_level in new_values]
        
            # Update list of all current audio applications
            sessions = [session for session in AudioUtilities.GetAllSessions() if session.Process] #Make sure session exists
               
            #Iterate all pins and check if they need to be updated
            for pin in pins:
                if (new_values[pin.get_pin_index()] != old_values[pin.get_pin_index()]):
                #If this the master channel that needs updating
                    if (pin.get_pin_index() == Constants.PIN_MASTER):
                        volume.SetMasterVolumeLevelScalar(pin_values_normal[0], None)
                    
                    elif (pin.get_pin_index == Constants.PIN_OTHER):
                        #Need to complete later
                        pass
                        
                    else:
                        for session in sessions:
                            if (session.Process.name() in pin.get_processes()):
                                pin.set_process_volume(session, pin_values_normal[pin.get_pin_index()])
                        

            old_values = new_values
            
        


if __name__ == "__main__":
    main()

