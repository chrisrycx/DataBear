BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"user_id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL,
	"password_hash"	TEXT,
	"permission_level"	INTEGER,
	PRIMARY KEY("user_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "sensors" (
	"sensor_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"serial_number"	TEXT,
	"sensor_type"	TEXT NOT NULL,
	"description"	TEXT,
	PRIMARY KEY("sensor_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "operations" (
	"operation_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"description"	TEXT,
	PRIMARY KEY("operation_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "processes" (
	"process_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("process_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "configuration" (
	"config_id"	INTEGER NOT NULL,
	"operation_id"	INTEGER NOT NULL,
	"interval_sec"	REAL NOT NULL,
	"process_id"	INTEGER NOT NULL,
	"measure_id"	INTEGER NOT NULL,
	FOREIGN KEY("process_id") REFERENCES "processes"("process_id") on update restrict,
	FOREIGN KEY("measure_id") REFERENCES "measurements"("measurement_id") on update restrict,
	FOREIGN KEY("operation_id") REFERENCES "operations"("operation_id") on update restrict,
	PRIMARY KEY("config_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "data" (
	"dataid"	INTEGER NOT NULL,
	"dtstamp"	TEXT NOT NULL,
	"value"	REAL NOT NULL,
	"measure_id"	INTEGER NOT NULL,
	"process_id"	INTEGER NOT NULL,
	"qc_flag"	INTEGER,
	FOREIGN KEY("measure_id") REFERENCES "measurements"("measurement_id") on update restrict,
	FOREIGN KEY("process_id") REFERENCES "processes"("process_id") on update restrict,
	PRIMARY KEY("dataid" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "measurements" (
	"measurement_id"	INTEGER NOT NULL,
	"sensor_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"units"	TEXT NOT NULL,
	"description"	TEXT,
	FOREIGN KEY("sensor_id") REFERENCES "sensors"("sensor_id") on update restrict,
	PRIMARY KEY("measurement_id" AUTOINCREMENT)
);
INSERT INTO "operations" VALUES (1,'Measure','Perform a measurement using a sensor');
INSERT INTO "operations" VALUES (2,'Store','Store data to the database for a sensor');
INSERT INTO "processes" VALUES (1,'Sample','Select the first measurement from storage interval for storage');
INSERT INTO "processes" VALUES (2,'Average','Calculate the average value of measurements from storage interval');
INSERT INTO "processes" VALUES (3,'Max','Select the maximum value from measurement in the storage interval');
INSERT INTO "processes" VALUES (4,'Min','Select the minimum value from measurement in the storage interval');
INSERT INTO "processes" VALUES (5,'Dump','Select all measurements from the storage interval for storage');
COMMIT;
