# Dump Heroku Database to Working Dir.
heroku pg:backups:download -a pymultiposter

# Restoring Dumped Database
pg_restore --verbose --clean --no-acl --username=postgres -h localhost -d postgres latest.dump
