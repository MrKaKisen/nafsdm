# nafsdm
# versionCheck
# checks if a new version is available

from version import version
from daemonlog import log
import os
import requests

def checkUpdate(config):
    log("Checking if a new version is available..")
    r = requests.get("https://raw.githubusercontent.com/MrKaKisen/nafsdm/master/version.txt")

    # check if we got a good code, requests has builtin codes which are OK
    if (r.status_code == requests.codes.ok):
        if (r.text.split("\n")[0] == version):
            log("You're running the latest version, " + version + "!")
        else:
            log("NOTICE: There is a new version available! New version: " + r.text.split("\n")[0])
            if (os.path.exists("/home/slave-nafsdm/tempUpgrade")):
                log("WARN: folder already exists?")
            else:
                os.makedirs("/home/slave-nafsdm/pythondaemon/tempUpgrade")
                # shortcut to make the shit importable
                f = open("/home/slave-nafsdm/pythondaemon/tempUpgrade/__init__.py", "w")
                f.write(" ")
                f.close()

            # url must change from development to master before release!!
            url = ("https://raw.githubusercontent.com/MrKaKisen/nafsdm/development/scripts/upgradeSlave.sh")
            r = requests.get(url)
            if (r.status_code == requests.codes.ok):
                f = open("/home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh", "w")
                f.write(r.content)
                f.close()
                import subprocess
                outputNull = subprocess.check_output(["chmod", "+x", "/home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.sh"])

                url = ("https://raw.githubusercontent.com/MrKaKisen/nafsdm/development/scripts/upgradeSlave.py")
                r = requests.get(url)
                if (r.status_code == requests.codes.ok):
                    f = open("/home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.py", "w")
                    f.write(r.content)
                    f.close()
                    import subprocess
                    outputNull = subprocess.check_output(["chmod", "+x", "/home/slave-nafsdm/pythondaemon/tempUpgrade/temp_upgrade.py"])

                    from tempUpgrade.temp_upgrade import initUpgrade
                    upgradeStatus = initUpgrade(config)
                    if upgradeStatus == "exception":
                        log("FATAL: An error occured during upgrade. Either you use a unsupported version or the script failed mid-through (that would break your installation). Please retry or run the script manually.")
                        exit(1)
                    else:
                        f = open("/home/slave-nafsdm/upgradeLog.log", "w")
                        f.write(upgradeStatus)
                        f.close()
                        log("INFO: Upgrade completed. Please update your configuration as the upgradeLog.log says.")
                        log("INFO: nafsdm will continue to boot but into the old version (libs already loaded :P)")
                else:
                    log("FATAL: Couldn't connect to GitHub! Quitting...")
                    exit(1)
            else:
                log("FATAL: Couldn't connect to GitHub! Quitting..")
                exit(1)
    else:
        log("FATAL: Couldn't receive latest version (on GitHub). Quitting.")
        exit(1)
