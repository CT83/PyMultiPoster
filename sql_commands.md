# Dump Heroku Database to Working Dir.
heroku pg:backups:capture -a pymultiposter
heroku pg:backups:download -a pymultiposter

# Restoring Dumped Database Local
pg_restore --verbose --clean --no-acl --username=postgres -h localhost -d postgres latest.dump

# Restoring Dumped Database Heroku
heroku pg:backups:restore "https://s3.amazonaws.com/temp-storage-ct83/PMP_DB.dump" DATABASE_URL -a pymultiposter-2

# Connecting to local PSQL Server
psql --host=localhost --port=5432 --username postgres --password --dbname=postgres

# Dumping Local PSQL Database to file
pg_dump -d postgres -U postgres -f PMP_DB.dump -F c


# Delete all Tables in Database [PG Commands]
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;