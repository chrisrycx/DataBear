'''
Test imports of modules from different places

Built in sensor in databear.sensors
Custom sensor in path added to PYTHONPATH

** Assume custom sensor module is in the current directory
'''
import importlib
import sys

custom_sensor_path = ''

enabledsensors = [
    {
        'class_name':'databearSim',
        'customsensor':0
    },
    {
        'class_name':'dyaconTPH1B',
        'customsensor':1
    }]

for enabled_sensor in enabledsensors:
    #Import string
    impstr = enabled_sensor['class_name']

    #Import class
    if enabled_sensor['customsensor']==0:
        #Built in sensor (sensors folder)
        impstr = 'databear.sensors.'+impstr 

    sensor_module = importlib.import_module(impstr)
    sensor_class = getattr(sensor_module,enabled_sensor['class_name'])

    print(sensor_class.hardware_settings)



