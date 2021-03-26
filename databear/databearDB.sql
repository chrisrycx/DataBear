BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "sensors_available" (
	"sensormodule_id"	INTEGER,
	"sensor_module"	TEXT NOT NULL,
	UNIQUE("sensor_module"),
	PRIMARY KEY("sensormodule_id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "data" (
	"data_id"	INTEGER NOT NULL,
	"dtstamp"	TEXT NOT NULL,
	"value"	REAL NOT NULL,
	"sensor_configid"	INTEGER NOT NULL,
	"logging_configid"	INTEGER NOT NULL,
	"qc_flag"	INTEGER,
	FOREIGN KEY("logging_configid") REFERENCES "logging_configuration"("logging_configid"),
	FOREIGN KEY("sensor_configid") REFERENCES "sensor_configuration"("sensor_configid"),
	PRIMARY KEY("data_id" AUTOINCREMENT)
);

CREATE INDEX IF NOT EXISTS data_index ON data ("dtstamp");

CREATE TABLE IF NOT EXISTS "processes" (
	"process_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("process_id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "sensor_configuration" (
	"sensor_config_id"	INTEGER NOT NULL,
	"sensor_id"	INTEGER NOT NULL,
	"measure_interval"	REAL NOT NULL,
	"status"    INTEGER,
	FOREIGN KEY("sensor_id") REFERENCES "sensors"("sensor_id") ON DELETE CASCADE,
	PRIMARY KEY("sensor_config_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "logging_configuration" (
	"logging_config_id"	INTEGER NOT NULL,
	"measurement_id"	INTEGER NOT NULL,
	"sensor_id"	INTEGER NOT NULL,
	"storage_interval"	INTEGER NOT NULL,
	"process_id"	INTEGER NOT NULL,
	"status"	INTEGER,
	FOREIGN KEY("measurement_id") REFERENCES "measurements"("measurement_id") ON DELETE CASCADE,
	FOREIGN KEY("process_id") REFERENCES "processes"("process_id") ON UPDATE CASCADE,
	FOREIGN KEY("sensor_id") REFERENCES "sensors"("sensor_id") ON DELETE CASCADE,
	PRIMARY KEY("logging_config_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "sensors" (
	"sensor_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"serial_number"	TEXT NOT NULL,
	"address"	INTEGER NOT NULL DEFAULT 0,
	"virtualport"	INTEGER NOT NULL,
	"module_name"	TEXT NOT NULL,
	"description"	TEXT,
	FOREIGN KEY("module_name") REFERENCES "sensors_available"("sensor_module"),
	UNIQUE("serial_number","module_name"),
	PRIMARY KEY("sensor_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "measurements" (
	"measurement_id"	INTEGER,
	"name"	TEXT NOT NULL,
	"units"	TEXT NOT NULL,
	"description"	TEXT,
	"sensor_module"	TEXT,
	FOREIGN KEY("sensor_module") REFERENCES "sensors_available"("sensor_module") ON DELETE CASCADE,
	PRIMARY KEY("measurement_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "databear_configuration" (
    "name" TEXT NOT NULL PRIMARY KEY,
    "value" INTEGER NOT NULL
);

CREATE VIEW dataview AS
SELECT d.dtstamp, d.value, s.name AS sensor_name, m.name AS measurement, 
       p.name AS process, sc.measure_interval AS measure_interval 
FROM DATA d
	INNER JOIN sensor_configuration sc ON d.sensor_configid=sc.sensor_config_id
	INNER JOIN logging_configuration lc ON d.logging_configid=lc.logging_config_id
	JOIN sensors s ON sc.sensor_id=s.sensor_id
	JOIN measurements m ON lc.measurement_id=m.measurement_id
    JOIN processes p ON lc.process_id=p.process_id;
    
INSERT INTO "processes" VALUES (1,'Sample','Select the first measurement from storage interval for storage');
INSERT INTO "processes" VALUES (2,'Average','Calculate the average value of measurements from storage interval');
INSERT INTO "processes" VALUES (3,'Max','Select the maximum value from measurement in the storage interval');
INSERT INTO "processes" VALUES (4,'Min','Select the minimum value from measurement in the storage interval');
INSERT INTO "processes" VALUES (5,'Dump','Select all measurements from the storage interval for storage');
INSERT INTO "databear_configuration" VALUES("schemaversion", 2);
COMMIT;
