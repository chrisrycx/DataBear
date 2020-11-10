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

### V2.0 Changes
Databear now uses a SQLite database for both configuration and data storage.
However, direct interaction with the database is optional and configuration
can still be completed using YAML. 

DataBear now runs in the background and can be managed via the commandline or
through socket communication.

### Some potential usage scenarios:
Here are some random ideas to give a sense for DataBear capabilities (some capabilities under development).
* Run DataBear on a Raspberry Pi (https://www.raspberrypi.org/) to read a Modbus temperature sensor.  The sensor could be connected to a USB port on the Pi via an RS485 to USB converter and data could be read every second, averaged, and stored to CSV.
* Integrate DataBear into an existing Linux based measurement platform, such as the Dyacon MDL-700 (https://dyacon.com).

### Ideal Datalogger Features vs Data Bear 2.0
| Ideal Feature                                  | Data Bear       |
| -------------                                  | ---------       |
| Adjustable sampling rates for all measurements | &#9745;         |
| Concurrent measurement of all sensors          | &#9745;         |
| Adjustable rates of data storage               | &#9745;         |
| Complete storage of metadata                   | &#9745;         |
| Supports polled or continuously streaming sensors    | &#9745;         |
| Ability to change settings on the fly          | Coming soon     |
| Support for sensors on a bus                   | Coming soon     |

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
3. Create a driver for your platform (See Driver Interface)
4. Create a new configuration file (YAML) following the approach used in the example folder. This file should be stored in your project directory.
5. Set two environmental variables:

    ```bash
    : export DBDRIVER=<my driver>
    : export DBSENSORS=<folder name with sensors>
    ```
6. Run/Stop DataBear
    ```
    : databear run <myconfig>.yaml
    : databear shutdown 

### DataBear API
DataBear now features a rudimentary API for use with interprocess communication. Commands and responses are exchanged in JSON via UDP.
* UDP Port: 62000
* Command Format: {'command': \<command\>, 'arg': \<Optional Argument\>}
* Commands
    * status - Return a response if logger is active.
    * getdata \<sensor name\> - Return most recent measurement data for sensor.
    * stop \<sensor name\> - Stop measurement and data storage for sensor.
    * shutdown - Stop logger.


### Sensor Interface (V1.1)
- Recommended class naming convention 'manufacturerModel'
- Inherit sensor base class

```python
class dyaconWSD(sensors.Sensor):
    '''
    Overwrite base class attributes to make
    sensor specific. Overwriting measurements
    is mandatory, others are optional.
    '''
    measurements = ['measure1','measure2']
    def __init__(self,name,sn,address):
        '''
        Create a new simulator
        - Call base class init
        - Override base data structure
        '''
        super().__init__(name,sn,address)

        #Initialize a counter
        self.counter = 0 

    def connect(self,port):
        '''
        Set up connection to hardware
        port - port returned by driver
        '''
    
    def measure(self):
        '''
        Override base method and define
        how sensor makes a measurement.
        Store measurement in 
            self.data[<measurement name>].append(datetime,value)
        '''
        pass
```
### Driver Interface (V0)
- A class that maps Databear virtual ports to hardware ports

```python
class dbdriver:
    def __init__(self):
        '''
        Map virtual ports to hardware ports
        '''
        #A windows example
        self.ports = {
            'port1':'COM6',
            'port2':'COM21'
        }

    def connect(self,databearport,hardware_settings):
        '''
        Perform any hardware configuration and return
        hardware port for use by sensor.connect method
        '''
        #A windows example
        return self.ports[databearport]
```




