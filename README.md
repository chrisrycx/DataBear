# DataBear
General purpose data aquistion, processing, and logging platform written 
in Python. DataBear is hardware independent, but is meant to be easily integrated via a custom hardware interface provided by the user.

### Goals:
* Easy to use - intuitive setup and configuration.
* Versatile
    * Use on any hardware device that runs Python.
    * Compatible with most sensor output.
* Extendible
    * User can integrate platform with new sensor and methods.

### Some potential usage scenarios:
Here are some random ideas to give a sense for DataBear capabilities (some capabilities under development).
* Run DataBear on a Raspberry Pi (https://www.raspberrypi.org/) to read a Modbus temperature sensor.  The sensor could be connected to a USB port on the Pi via an RS485 to USB converter and data could be read every second, averaged, and stored to CSV.
* Integrate DataBear into an existing Linux based measurement platform, such as the Dyacon MDL-700 (https://dyacon.com).

### Ideal Datalogger Features vs Data Bear 1.2
| Ideal Feature                                  | Data Bear       |
| -------------                                  | ---------       |
| Adjustable sampling rates for all measurements | &#9745;         |
| Concurrent measurement of all sensors          | &#9745;         |
| Adjustable rates of data storage               | &#9745;         |
| Store metadata associated with data values     | &#9745;         |
| Supports polled or continuously streaming sensors    | &#9745;         |

### Installation
* pip install databear

### Hardware
A "DataBear Driver" is needed to use DataBear on different devices.
Create a driver following the "Driver Interface" below.

### General Usage
1. Check to see if a class has been created for your sensor(s) 
 in DataBear/sensors. Since this project is new, it is likely you 
 will need to create a sensor class or modify an existing one (See "Sensor Class Interface").
2. Create a class for your sensor(s) following the interface defined below.
Use existing classes as examples or templates. Share your sensor class
with the DataBear project so others can use it.
3. Create a new configuration file following the approach used in the examples folder.
4. Create a short script to initialize and run DataBear. This script will 
register your sensor(s) class with DataBear and load the configuration file.
See example.py for details. 

### DataBear API
DataBear now features a rudimentary API for use with interprocess communication. Commands and responses are exchanged in JSON via UDP.
* UDP Port: 62000
* Command Format: {'command': \<command\>, 'arg': \<Optional Argument\>}
* Commands
    * status - Return a response if logger is active.
    * getdata \<sensor name\> - Return most recent measurement data for sensor.
    * stop \<sensor name\> - Stop measurement and data storage for sensor.
    * shutdown - Stop logger.


### Sensor Interface (V1.0)
Class Name: (Format optional but recommended)
* \<manufacturer>\<Model>	
* Use databear.sensors.Sensor as a base class
* Example - class dyaconWSD(sensors.Sensor):

Methods
* __init__(self,name,sn,address,interval)
    * Inputs
        * name - name of sensor
        * sn - serial number of sensor
        * address - sensor address, set to 0 if none
        * interval - measurement interval (may be removed in future release)
    * Define a data dictionary for the sensor after calling the base class
      __init__.
        * data = {"measure1":[],"measure2":[],...}
* connect(self,port)
    * Use to initialize a connection to actual hardware port.
* measure(self)
    * Performs sensor measurement. No inputs.
    * Data for each measurement is added to the ‘data’ attribute.
    * Data should consist of a tuple of the form (\<timestamp>,\<datavalue>)
        * data[\<measurement name>] = (\<timestamp>,\<datavalue>)

### Driver Interface (V0)
Class definition:
* dbdriver
    * No base class to inherit from
Methods
* __init__
    * Use to map virtual ports to real hardware ports
* connect(self,virtualport,hardware_settings)
    * Use to configure hardware and return hardware port name from mapping


