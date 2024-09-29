#!/bin/bash

export PGUSER=postgres

# create test database
psql <<- EOSQL
    CREATE DATABASE "$DB_NAME_TEST";
    ALTER DATABASE "$DB_NAME_TEST" OWNER TO $DB_USERNAME;
    GRANT ALL PRIVILEGES ON DATABASE "$DB_NAME_TEST" TO $DB_USERNAME;
EOSQL

psql "$DB_NAME_TEST" <<- EOSQL
    CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public;
    COMMENT ON EXTENSION unaccent IS 'text search dictionary that removes accents';
EOSQL

psql -U dev $DB_NAME_TEST < "/tmp/sql/dump.sql"
