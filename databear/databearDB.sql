BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "sensors_available" (
	"sensorclass_id"	INTEGER,
	"class_name"	TEXT NOT NULL,
	UNIQUE("class_name"),
	PRIMARY KEY("sensorclass_id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "data" (
	"data_id"	INTEGER NOT NULL,
	"dtstamp"	TEXT NOT NULL,
	"value"	REAL NOT NULL,
	"sensor_configid"	INTEGER NOT NULL,
	"logging_configid"	INTEGER NOT NULL,
	"qc_flag"	INTEGER,
	FOREIGN KEY("logging_configid") REFERENCES "logging_configuration"("logging_configid") ON DELETE RESTRICT,
	FOREIGN KEY("sensor_configid") REFERENCES "sensor_configuration"("sensor_configid") ON DELETE RESTRICT,
	PRIMARY KEY("data_id" AUTOINCREMENT)
);
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
	"status"	INTEGER,
	FOREIGN KEY("sensor_id") REFERENCES "sensors"("sensor_id") ON DELETE CASCADE,
	UNIQUE("sensor_id","status"),
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
	"class_name"	TEXT NOT NULL,
	"description"	TEXT,
	FOREIGN KEY("class_name") REFERENCES "sensors_available"("class_name"),
	UNIQUE("serial_number","class_name"),
	PRIMARY KEY("sensor_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "measurements" (
	"measurement_id"	INTEGER,
	"name"	TEXT NOT NULL,
	"units"	TEXT NOT NULL,
	"description"	TEXT,
	"class_name"	TEXT,
	FOREIGN KEY("class_name") REFERENCES "sensors_available"("class_name") ON DELETE CASCADE,
	PRIMARY KEY("measurement_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "databear_configuration" (
    "name" TEXT NOT NULL PRIMARY KEY,
    "value" INTEGER NOT NULL
);
INSERT INTO "processes" VALUES (1,'Sample','Select the first measurement from storage interval for storage');
INSERT INTO "processes" VALUES (2,'Average','Calculate the average value of measurements from storage interval');
INSERT INTO "processes" VALUES (3,'Max','Select the maximum value from measurement in the storage interval');
INSERT INTO "processes" VALUES (4,'Min','Select the minimum value from measurement in the storage interval');
INSERT INTO "processes" VALUES (5,'Dump','Select all measurements from the storage interval for storage');
INSERT INTO "databear_configuration" VALUES("schemaversion", 1);
COMMIT;
