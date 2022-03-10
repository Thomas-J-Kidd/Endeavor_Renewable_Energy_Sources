import OOP_Data_Collection
import multiprocessing


def set_solar_1():
    solar_1 = OOP_Data_Collection.Monitoring(502, '10.10.10.10', 'renewable_data_solar_1.feather', 'Solar 1')
    solar_1.set_data()
def set_solar_2():
    solar_2 = OOP_Data_Collection.Monitoring(502, '10.10.10.11', 'renewable_data_solar_2.feather', 'Solar 2')
    solar_2.set_data()
def set_wind_1():
    solar_1 = OOP_Data_Collection.Monitoring(502, '10.10.10.12', 'renewable_data_solar_1.feather', 'Wind 1')
    solar_1.set_data()
def set_wind_2():
    solar_2 = OOP_Data_Collection.Monitoring(502, '10.10.10.13', 'renewable_data_solar_2.feather', 'Wind 2')
    solar_2.set_data()

process_1 = multiprocessing.Process(target=set_solar_1)
process_2 = multiprocessing.Process(target=set_solar_2)
process_3 = multiprocessing.Process(target=set_wind_1)
process_4 = multiprocessing.Process(target=set_wind_2)


process_1.start()
process_2.start()
process_3.start()
process_4.start()
