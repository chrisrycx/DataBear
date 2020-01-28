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

### Ideal Datalogger Features vs Data Bear 0.2
| Ideal Feature                                  | Data Bear       |
| -------------                                  | ---------       |
| Adjustable sampling rates for all measurements | &#9745;         |
| Concurrent measurement of all sensors          |                 |
| Adjustable rates of data storage               | &#9745;         |
| Store metadata associated with data values.    | &#9745;         |
