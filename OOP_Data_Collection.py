#written by Thomas Kidd


#imports
#--------------------------------------------------------------------------------------------------
from datetime import datetime
import time
import socket
from umodbus import conf
from umodbus.client import tcp
import sys
import pandas as pd
import feather
#--------------------------------------------------------------------------------------------------

class Monitoring():
    
    
    def __init__(self, port, ip, file, name ):

        #initiates outside variables
        
        self.port = port
        self.ip = ip
        self.file = file
        self.name = name
        

        


        #creates a socket for ipv4 connections
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket succesfully created")
        except socket.error as err:
            print ("Socket creating failed with the error %s" %(err))
        
        #connectiong to the controler
        try: 
            self.s.connect((self.ip, self.port))
            print("The socket has succesfully connected to Midnite Controller")
        except:
            print("There was an error connecting to the controler")
            sys.exit()
        
        
        # initialize and load the file into a pandas data frame to handle data quickly

        self.df = pd.read_feather(file)

        # get the last previously gathered data into a list
        
        last_row = self.df.iloc[-1]
        last_register_4116 = last_row['Average Input Voltage (Volts)']
        last_register_4118 = last_row['Average Energy To Battery (kWh)']
        last_register_4119 = last_row['Average Power to the Battery (Watts)']
        last_register_4121 = last_row['Average Terminal Input Current (Amps)']
        last_register_4122 = last_row['Last Measured open-circuit Voltage (Volts)']
        last_register_4126_4127 = last_row['Lifetime kW-Hours']
        last_register_4128_4129 = last_row[ 'Lifetime Amp Hours']

        # initialize register list values
        self.Register_4116 = [last_register_4116]
        self.Register_4118 = [last_register_4118]
        self.Register_4119 = [last_register_4119]
        self.Register_4121 = [last_register_4121]
        self.Register_4122 = [last_register_4122]
        self.Register_4126_4127 = [last_register_4126_4127]
        self.Register_4128_4129 = [last_register_4128_4129]
        




# functions to call to get data from different registers
#--------------------------------------------------------------------------------------------------

    def request_register_4116(self):
        # 4116 = Average PV terminal input Voltage (1 sec) Volts
        request_register_4116 = tcp.read_holding_registers(slave_id=1, starting_address=4115, quantity=1)
        message_register_4116 = tcp.send_message(request_register_4116, self.s)
        register_4116 = (message_register_4116[0]/10)
        return register_4116

    def request_register_4118(self):
        # 4118 = Average energy to the bettery (reset once per day) kW-H   
        request_register_4118 = tcp.read_holding_registers(slave_id=1, starting_address=4117, quantity=1)
        message_register_4118 = tcp.send_message(request_register_4118, self.s)
        register_4118 = (message_register_4118[0]/10)
        return register_4118

    def request_register_4119(self):
        # 4119 = Average Power to the Battery Watts
        request_register_4119 = tcp.read_holding_registers(slave_id=1, starting_address=4118, quantity=1)
        message_register_4119 = tcp.send_message(request_register_4119, self.s)
        register_4119 = (message_register_4119[0]/10)
        return register_4119

    def request_register_4121(self):
        # 4121 = Average Terminal Input Current
        request_register_4121 = tcp.read_holding_registers(slave_id=1, starting_address=4120, quantity=1)
        message_register_4121 = tcp.send_message(request_register_4121, self.s)
        register_4121 = (message_register_4121[0]/10)
        return register_4121
    
    def request_register_4122(self):
        # 4122 = Last Measured open-circuit Voltage at the PV terminal input
        request_register_4122 = tcp.read_holding_registers(slave_id=1, starting_address=4121, quantity=1)
        message_register_4122 = tcp.send_message(request_register_4122, self.s)
        register_4122 = (message_register_4122[0]/10)
        return register_4122

    def request_register_4126_4127(self):
        # 4128_4129 = Lifetime Amp Hours
        request_register_4126 = tcp.read_holding_registers(slave_id=1, starting_address=4125, quantity=1)
        message_register_4126 = tcp.send_message(request_register_4126, self.s)
        request_register_4127 = tcp.read_holding_registers(slave_id=1, starting_address=4126, quantity=1)
        message_register_4127 = tcp.send_message(request_register_4127, self.s)
        register_4126_4127 = (message_register_4126[0] + message_register_4127[0] * (2**16))
        return register_4126_4127

    def request_register_4128_4129(self):
        # 4126_4127 = Lifetime kW-Hours
        request_register_4128 = tcp.read_holding_registers(slave_id=1, starting_address=4127, quantity=1)
        message_register_4128 = tcp.send_message(request_register_4128, self.s)
        request_register_4129 = tcp.read_holding_registers(slave_id=1, starting_address=4128, quantity=1)
        message_register_4129 = tcp.send_message(request_register_4129, self.s)
        register_4128_4129 = (message_register_4128[0] + message_register_4129[0] * (2**16))
        return register_4128_4129

#--------------------------------------------------------------------------------------------------
#   This function is here to get and set the data to the appropriate spot.
    def set_data(self):

        

        now = datetime.now()    # getting todays date
        date_string = now.strftime("20%y-%m-%d %H:%M:%S") # putting it in a certain format
        timestamp = [date_string] # adding it to the time stamp

        # collect data continously
        while True:
            # create a list to later collect the data into and add it to the data frame
            register_list = [timestamp[0], self.Register_4116[0], self.Register_4118[0], self.Register_4119[0], 
                     self.Register_4121[0], self.Register_4122[0], self.Register_4126_4127[0], self.Register_4128_4129[0]]
            try:
                # collect the data
                self.Register_4116[0] = self.request_register_4116()
                self.Register_4118[0] = self.request_register_4118()
                self.Register_4119[0] = self.request_register_4119()
                self.Register_4121[0] = self.request_register_4121()
                self.Register_4122[0] = self.request_register_4122()
                self.Register_4126_4127[0] = self.request_register_4126_4127()
                self.Register_4128_4129[0] = self.request_register_4128_4129()

                # set the data
                self.df.loc[len(self.df)] = register_list
                self.df.to_feather(self.file)
                
                # print the data out to monitor status
                print("Data is being collected on", self.name)
                #print(self.df)
                #print("Last Index: ", self.df.last_valid_index())

                # sleep to save space 
                time.sleep(10)

            except:
                # exceptions incase of errors 
                # we use negative numbers to easily filter out of the data
                print("Error occured")
                self.Register_4116[0] = -1
                self.Register_4119[0] = -1
                self.Register_4121[0] = -1
                self.Register_4122[0] = -1
                self.Register_4126_4127[0] = -1
                self.Register_4128_4129[0] = -1
                time.sleep(60)







#object


# solar_1 = Monitoring(502, '10.10.10.10', 'renewable_data_solar_1.feather', 'Solar 1')
# solar_1.set_data()

# solar_2 = Monitoring(502, '10.10.10.11', 'renewable_data_solar_2.feather', 'Solar 2')
# solar_2.set_data()

# wind_1 = Monitoring(502, '10.10.10.12', 'renewable_data_wind_1.feather', 'Wind 1')
# wind_1.set_data()

# wind_2 = Monitoring(502, '10.10.10.13', 'renewable_data_wind_2.feather', 'Wind 2')
# wind_2.set_data()