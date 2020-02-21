# DataBear
General purpose data aquistion, processing, and logging platform written in Python.
DataBear is hardware independent, but is meant to be easily integrated via a custom
hardware interface provided by the user.

### Goals:
* Easy to use - intuitive setup and configuration.
* Versatile - use on any hardware device that runs Python.
* Extendible - add new methods for measurement as needed.

### Some potential usage scenarios:
Here are some random ideas to give a sense for DataBear capabilities (some capabilities under development).
* Run DataBear on a Raspberry Pi (https://www.raspberrypi.org/) to read a Modbus temperature sensor.  The sensor could be connected to a USB port on the Pi via an RS485 to USB converter and data could be read every second, averaged, and stored to CSV.
* Integrate DataBear into an existing Linux based measurement platform, such as the Dyacon MDL-700 (https://dyacon.com). In this case, DataBear is utilized by pyMDL (https://github.com/dyacon/pyMDL) to schedule measurement and storage, while pyMDL specifies hardware configuration.

### Ideal Datalogger Features vs Data Bear 1.0
| Ideal Feature                                  | Data Bear       |
| -------------                                  | ---------       |
| Adjustable sampling rates for all measurements | &#9745;         |
| Concurrent measurement of all sensors          |                 |
| Adjustable rates of data storage               | &#9745;         |
| Store metadata associated with data values.    | &#9745;         |

### Installation
* pip install databear

### Usage
1. Check to see if a class has been created for your sensor(s) 
 in DataBear/sensors. Since this project is new, it is likely you 
 will need to create a sensor class or modify an existing one.
2. Create a class for your sensor(s) following the interface defined below.
Use existing classes as examples or templates. Share your sensor class
with the DataBear project so others can use it.
3. Create a new configuration file following the example shown in config.yaml.
4. Create a short script to initialize and run DataBear. This script will 
register your sensor(s) class with DataBear and load the configuration file.
See example.py for details. 

### Sensor Class Interface (V0)
Class Name: (Optional but recommended)
* \<manufacturer>\<Model>	Example - class dyaconWSD2:

Instantiation Inputs: (Mandatory)
* ‘name’ - [string] User configurable sensor name
* ‘settings’ - [dictionary] A dictionary of settings that are necessary for mandatory methods and attributes. 

Attributes: (Mandatory)
* All sensors
    * sn - [string] Sensor serial number specified in ‘settings’.
    * frequency - [float] Sensor measurement frequency in seconds specified     in ‘settings’.
    * maxfrequency - [float] Maximum frequency in seconds that the sensor can   measure. 
    * data - [dictionary] Stores data for each measurement.
        * Initialize to {\<key>: [ ] , ...} where \<key> is the name of each measurement.  

* Serial sensors - Attributes describing serial hardware settings. These may not be used but should be available for certain hardware devices.
    * rs - [string] serial protocol: ‘RS485’, ‘RS232’
    * duplex - [string] ‘half’, ‘full’
    * resistors - [boolean] Indicates if termination resistors are present.
    * bias - [boolean] Indicates if bias resistors are active. 

Methods: (Mandatory)
* ‘measure( )’ - Implements coding required to obtain data for each measurement.
    * No inputs
    * Data for each measurement is added to the ‘data’ attribute.
    * Data should consist of a tuple of the form (\<timestamp>,\<datavalue>)
        * data[\<measurement name>] = (\<timestamp>,\<datavalue>)

* ‘cleardata(name)’ - Clears data associated with a given measurement.
    * Input ‘name’ - the name of the measurement.
    * data[name] = [ ]