BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "sensors" (
	"sensor_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT NOT NULL,
	"serial_number"	TEXT NOT NULL,
	"address"	INTEGER,
	"virtualport"	INTEGER NOT NULL,
	"sensor_type"	TEXT NOT NULL,
	"description"	TEXT,
	UNIQUE("serial_number","sensor_type")
);
CREATE TABLE IF NOT EXISTS "data" (
	"dataid"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"dtstamp"	TEXT NOT NULL,
	"value"	REAL NOT NULL,
	"sensor_configid"	INTEGER NOT NULL,
	"logging_configid"	INTEGER NOT NULL,
	"qc_flag"	INTEGER,
	FOREIGN KEY("logging_configid") REFERENCES "logging_configuration"("logging_configid") ON DELETE RESTRICT,
	FOREIGN KEY("sensor_configid") REFERENCES "sensor_configuration"("sensor_configid") ON DELETE RESTRICT
);
CREATE TABLE IF NOT EXISTS "logging_configuration" (
	"logging_configid"	INTEGER,
	"measurementid"	INTEGER NOT NULL,
	"storage_interval"	INTEGER NOT NULL,
	"processid"	INTEGER NOT NULL,
	"status"	INTEGER,
	PRIMARY KEY("logging_configid"),
	FOREIGN KEY("measurementid") REFERENCES "measurements"("measurement_id") ON DELETE CASCADE,
	FOREIGN KEY("processid") REFERENCES "processes"("process_id") ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS "sensor_configuration" (
	"sensor_configid"	INTEGER,
	"sensorid"	INTEGER NOT NULL,
	"measure_interval"	REAL NOT NULL,
	"status"	INTEGER,
	PRIMARY KEY("sensor_configid"),
	FOREIGN KEY("sensorid") REFERENCES "sensors"("sensor_id") ON DELETE CASCADE,
	UNIQUE("sensorid","status")
);
CREATE TABLE IF NOT EXISTS "measurements" (
	"measurement_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"sensor_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"units"	TEXT NOT NULL,
	"description"	TEXT,
	FOREIGN KEY("sensor_id") REFERENCES "sensors"("sensor_id") on update restrict
);
CREATE TABLE IF NOT EXISTS "processes" (
	"process_id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT NOT NULL,
	"description"	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "user_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "username" TEXT,
    "password_hash" TEXT,
    "email" TEXT,
    "cellphone" TEXT,
    "permission_level" INTEGER);
CREATE TABLE IF NOT EXISTS "account_sessions" (
    "session_id" VARCHAR(255) NOT NULL PRIMARY KEY,
    "user_id" INTEGER NOT NULL,
    "login_time" DATETIME NOT NULL);
CREATE TABLE IF NOT EXISTS "variables" (
    "name" VARCHAR(255) NOT NULL PRIMARY KEY,
    "value" VARCHAR(255) NOT NULL);
INSERT INTO "sensors" ("sensor_id","name","serial_number","address","virtualport","sensor_type","description") VALUES (1,'simulator','0',NULL,'port0','dbSim','Default simulator sensor');
INSERT INTO "measurements" ("measurement_id","sensor_id","name","units","description") VALUES (1,1,'simsecond','second','The first simulator measurement.');
INSERT INTO "processes" ("process_id","name","description") VALUES (1,'Sample','Select the first measurement from storage interval for storage'),
 (2,'Average','Calculate the average value of measurements from storage interval'),
 (3,'Max','Select the maximum value from measurement in the storage interval'),
 (4,'Min','Select the minimum value from measurement in the storage interval'),
 (5,'Dump','Select all measurements from the storage interval for storage');
COMMIT;
