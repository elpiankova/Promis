BEGIN; 

-- satellites
DROP TABLE IF EXISTS "satellites";
CREATE TABLE "satellites" (
    "title" varchar(255) NOT NULL,
    "description" text NOT NULL,
    CONSTRAINT "satellites_pkey" PRIMARY KEY ("title")
)
;

-- devices
DROP TABLE IF EXISTS "devices";
CREATE TABLE "devices" (
    "id" serial NOT NULL,
    "title" varchar(255) NOT NULL,
    "description" text NOT NULL,
    "satellite_title" varchar(255) NOT NULL,
    CONSTRAINT "devices_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "devices_title_satellite_title_key" UNIQUE ("title", "satellite_title")
)
;

--channels
DROP TABLE IF EXISTS "channels";
CREATE TABLE "channels" (
    "id" serial NOT NULL,
    "title" varchar(255) NOT NULL,
    "description" text NOT NULL,
--    "sampling_frequency" double precision,
    "device_id" integer NOT NULL ,
    CONSTRAINT "channels_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "channels_title_device_id_key" UNIQUE ("title", "device_id")
)
;

--channels_options
DROP TABLE IF EXISTS "channels_options" ;
CREATE TABLE "channels_options" (
    "id" serial NOT NULL,
    "channel_id" integer NOT NULL,	     
    "title" varchar(255) NOT NULL,
    "co_value" varchar(255),
    "description" text,
    CONSTRAINT "channels_options_pkey" PRIMARY KEY ("id")
)
;

--parameters
DROP TABLE IF EXISTS "parameters" ;
CREATE TABLE "parameters" (
    "title" varchar(255) NOT NULL,
    "units_title" varchar(255) NOT NULL,
    "short_name" varchar(45) NOT NULL,
    "description" text,
    CONSTRAINT "parameters_pkey" PRIMARY KEY ("title")
)
;

-- sessions
DROP TABLE IF EXISTS "sessions";
CREATE TABLE "sessions" (
    "id" serial NOT NULL ,
    "time_begin" timestamp with time zone NOT NULL,
    "time_end" timestamp with time zone NOT NULL,
     CONSTRAINT "sessions_pkey" PRIMARY KEY ("id")
)
;

--sessions_options
DROP TABLE IF EXISTS "sessions_options" ;
CREATE TABLE "sessions_options" (
    "id" serial NOT NULL,
    "session_id" integer NOT NULL,	     
    "title" varchar(255) NOT NULL,
    "so_value" varchar(255),
    "description" text,
    CONSTRAINT "sessions_options_pkey" PRIMARY KEY ("id")
)
;

--measurament_points
DROP TABLE IF EXISTS "measurement_points";
CREATE TABLE "measurement_points" (
    "id" serial NOT NULL,  --in future BIGSERIAL!
    "time" timestamp with time zone NOT NULL,
    "x_geo" double precision,
    "y_geo" double precision,
    "z_geo" double precision,
--    "session_id" integer NOT NULL,
    CONSTRAINT "measurement_points_pkey" PRIMARY KEY ("id")
)
;

--measurements
DROP TABLE IF EXISTS "measurements" ;
CREATE TABLE "measurements" (
    "id" serial NOT NULL,   --in future BIGSERIAL!
    "level_marker" integer NOT NULL,
    "measurement" double precision NOT NULL,
    "relative_error" double precision,
    "parameter_title" varchar(255) NOT NULL,
    "channel_id" integer NOT NULL,
    "measurement_point_id" integer NOT NULL,
    "session_id" integer NOT NULL,
    CONSTRAINT "measurements_pkey" PRIMARY KEY ("id")
)
;

--units
DROP TABLE IF EXISTS "units";
CREATE TABLE "units" (
    "title" varchar(255) NOT NULL,
    "short_name" varchar(45) NOT NULL,
    "long_name" varchar(45) NOT NULL,
    "description" text,
    CONSTRAINT "units_pkey" PRIMARY KEY ("title")
)
;

--channels_have_parameters
DROP TABLE IF EXISTS "channels_have_parameters" ;
CREATE TABLE "channels_have_parameters" (
    "id" serial NOT NULL,
    "channel_id" integer NOT NULL,
    "parameter_title" varchar(255) NOT NULL,
    CONSTRAINT "channels_have_parameters_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "channels_have_parameters_channel_id_parameter_title_key" UNIQUE ("channel_id", "parameter_title")
)
;

--channels_have_sessions
DROP TABLE IF EXISTS "channels_have_sessions" ;
CREATE TABLE "channels_have_sessions" (
    "id" serial NOT NULL,
    "channel_id" integer NOT NULL,
    "session_id" integer NOT NULL,
    CONSTRAINT "channels_have_sessions_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "channels_have_sessions_channel_id_session_id_key" UNIQUE ("channel_id", "session_id")
)
;

--parameters_have_parameters
DROP TABLE IF EXISTS "parameters_have_parameters" ;
CREATE TABLE "parameters_have_parameters" (
    "id" serial NOT NULL,
    "parent_title" varchar(255) NOT NULL,
    "child_title" varchar(255) NOT NULL,
    CONSTRAINT "parameters_have_parameters_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "parameters_have_parameters_parent_child_key" UNIQUE ("parent_title", "child_title")
)
;

-- FOREIGN KEYS
ALTER TABLE "devices" 
    ADD CONSTRAINT "fk_devices_satellites"
    FOREIGN KEY ("satellite_title") 
    REFERENCES "satellites" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;
ALTER TABLE "channels" 
    ADD CONSTRAINT "fk_channels_devices"
    FOREIGN KEY ("device_id") 
    REFERENCES "devices" ("id")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;
ALTER TABLE "channels_options"
    ADD CONSTRAINT "fk_channels_options_channels"
    FOREIGN KEY ("channel_id") 
    REFERENCES "channels" ("id")
    MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE
;
ALTER TABLE "parameters"
    ADD CONSTRAINT "fk_parameters_units"
    FOREIGN KEY ("units_title") 
    REFERENCES "units" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;
ALTER TABLE "sessions_options"
    ADD CONSTRAINT "fk_sessions_options_sessions"
    FOREIGN KEY ("session_id") 
    REFERENCES "sessions" ("id")
    MATCH FULL ON DELETE CASCADE ON UPDATE CASCADE DEFERRABLE
;
--ALTER TABLE "measurement_points"
--    ADD CONSTRAINT "fk_measurement_points_sessions"
--    FOREIGN KEY ("session_id") 
--    REFERENCES "sessions" ("id")
--    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE-
--;
ALTER TABLE "measurements"
    ADD CONSTRAINT "fk_measurements_measurement_points"
    FOREIGN KEY ("measurement_point_id") 
    REFERENCES "measurement_points" ("id")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE ,

    ADD CONSTRAINT "fk_measurements_channels"
    FOREIGN KEY ("channel_id") 
    REFERENCES "channels" ("id")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE ,

    ADD CONSTRAINT "fk_measurements_parameters"
    FOREIGN KEY ("parameter_title") 
    REFERENCES "parameters" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE,

    ADD CONSTRAINT "fk_measurements_sessions"
    FOREIGN KEY ("session_id") 
    REFERENCES "sessions" ("id")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;
ALTER TABLE "channels_have_parameters"   
    ADD CONSTRAINT "fk_channels_have_parameters_parameters"
    FOREIGN KEY ("parameter_title") 
    REFERENCES "parameters" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE,

    ADD CONSTRAINT "fk_channels_have_parameters_channels"
    FOREIGN KEY ("channel_id") 
    REFERENCES "channels" ("id")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;
ALTER TABLE "channels_have_sessions" 
    ADD CONSTRAINT "fk_channels_have_sessions_chanels"
    FOREIGN KEY ("channel_id") 
    REFERENCES "channels" ("id")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE,

    ADD CONSTRAINT "fk_channels_have_sessions_sessions"
    FOREIGN KEY ("session_id") 
    REFERENCES "sessions" ("id")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;
ALTER TABLE "parameters_have_parameters"
    ADD CONSTRAINT "fk_parameters_have_parameters_parameters_parents"
    FOREIGN KEY ("parent_title") 
    REFERENCES "parameters" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE ,

    ADD CONSTRAINT "fk_parameters_have_parameters_parameters_children"
    FOREIGN KEY ("child_title") 
    REFERENCES "parameters" ("title")
    MATCH FULL ON DELETE RESTRICT ON UPDATE CASCADE DEFERRABLE
;

COMMIT;
