# nafsdm
# __main__
# masterd startup file
# (c) Vilhelm Prytz 2018
# https://github.com/mrkakisen/nafsdm

# imports
import os.path
from setup import *
from daemonlog import log
from version import version
from versionCheck import checkUpdate

log("*******************************************************")
log("master-nafsdm manager - running version " + version)
log("*******************************************************")

log("Performing pre-start checks..")

# pre checks
if not os.path.isfile("/home/master-nafsdm/.ssh/nafsdm_rsa"):
    log("SSH directory not found. Performing first time setup!")
    setupSSH()

# check for upgrade script
if os.path.isfile("/home/master-nafsdm/manager/tempUpgrade/temp_upgrade.sh"):
    log("Upgrade script found. Please change the data file and remove upgrade script!")
    exit(1)

# check for the legacy domains.txt file (before version 1.2.3)  and help the user migrate
if os.path.isfile("/home/master-nafsdm/data/domains.txt"):
    if not os.path.isfile("/home/master-nafsdm/data/domains.sql"):
        log("Legacy domains.txt file found, no domains.sql file found.")
        log("Do you wan't to migrate all data to the new domains.sql file?")

        # let the user choose to migrate old data to new SQL format
        confirmLoop = False
        while confirmLoop is False:
            confirm = raw_input("Confirm? (y/n): ")
            if confirm == "y" or confirm == "Y" or confirm == "yes":
                log("Confirmed. Migrating data...")
                migrateData()
                exit(0)
            elif confirm == "n" or confirm == "N" or confirm == "no":
                log("Exit.")
                exit(0)
            else:
                log("Please type yes or no.")
    else:
        log("Legacy domains.txt file found - but there is a domains.sql file present. Please delete the domains.txt file.")
        exit(1)

# check if the new (after version 1.2.3) domains.sql file is present
if not os.path.isfile("/home/master-nafsdm/data/domains.sql"):
    log("Could not find the domains.sql file. Configuring database..")
    setupDatabase()

# check for the slave alive folder
if not os.path.exists("/home/master-nafsdm/slaveAlive"):
    log("Creating slaveAlive directory..")
    os.makedirs("/home/master-nafsdm/slaveAlive")

if numberColumns() != 7:
    # this is an upgrade to 1.4-stable from prior versions
    if numberColumns() == 6:
        # we need to alter the table to add the new column
        updateTable()

        # set the new column to just 0
        setAllValues("zoneManaged", 0)
    else:
        log("Invalid amount of columns in database.")
        log("Is the database corrupt?")
        exot(1)


# check for new update
checkUpdate()

log("nafsdm-master is now ready.")
