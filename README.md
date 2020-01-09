# Data Bear
General purpose data aquistion, processing, and logging platform written in Python.

### Goals:
* Easy to use - intuitive setup and configuration.
* Versatile - use on any hardware device that runs Python.
* Extendible - add new methods for measurement as needed.

### Example uses (methods still under development):
* Read a temperature sensor using Modbus communications every minute and record the data to CSV.
* Measure soil moisture using SDI-12 communications every 5 minutes, average to hourly, and save as CSV.

### Ideal Datalogger Features vs Current Data Bear
More ideal features to be added...
|            Ideal Feature                       |      Data Bear       |
|           -------------                        |      ---------       |
| Adjustable sampling rates for all measurements |       &#9745;        |
| Concurrent measurement of all sensors          |                      |
| Adjustable rates of data storage               |       &#9745;        |
| Store metadata associated with data values.    |       &#9745;        |