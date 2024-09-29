#!/bin/bash

export PGUSER=postgres

echo "Create User"

# create default database user
psql <<- EOSQL
    CREATE USER $DB_USERNAME WITH PASSWORD '$DB_PASSWORD';
    ALTER USER $DB_USERNAME WITH SUPERUSER;
EOSQL

echo "User created"

echo "Create database"

# create default database
psql <<- EOSQL
    CREATE DATABASE "$DB_NAME";
    ALTER DATABASE "$DB_NAME" OWNER TO $DB_USERNAME;
    GRANT ALL PRIVILEGES ON DATABASE "$DB_NAME" TO $DB_USERNAME;
EOSQL

psql "$DATABASE_NAME" <<- EOSQL
    CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public;
    COMMENT ON EXTENSION unaccent IS 'text search dictionary that removes accents';
EOSQL

echo "Database created"

psql -U $DB_USERNAME $DB_NAME < "/tmp/sql/dump.sql"
