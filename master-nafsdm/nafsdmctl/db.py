# nafsdmctl
# db
# database functions for nafsdmctl

import sqlite3

# general db connection
def dbConnection():
    try:
        connection = sqlite3.connect("/home/master-nafsdm/data/domains.sql")
    except Exception:
        # if it can't connect to the file
        print("Could not read from domains.sql file! If this is the first time running, please run the master atleast once.")
        exit(1)

    cursor = connection.cursor()
    return connection, cursor

def addDomain(sysArg):
    connection, cursor = dbConnection()

    format_str = """
INSERT INTO domain (id, domain, masterIP, comment, assignedNodes, dnssec)
VALUES (NULL, "{domain}", "{masterIP}", "{comment}", "{assignedNodes}", "{dnssec}");"""

    sql_command = format_str.format(domain=sysArg[2], masterIP=sysArg[3], comment=sysArg[4], assignedNodes = sysArg[5], dnssec = sysArg[6])
    cursor.execute(sql_command)

    # close connection
    connection.commit()
    connection.close()

def removeDomain(domain):
    connection, cursor = dbConnection()

    sql_command = '''
DELETE FROM domain
WHERE domain="''' + domain + '''";'''


    # execute
    cursor.execute(sql_command)

    # test if we succeeded
    if len(cursor.fetchall()) == 0:
        return False

    # close connection
    connection.commit()
    connection.close()

    return True

def listDomains():
    connection, cursor = dbConnection()

    cursor.execute("SELECT * FROM domain")
    result = cursor.fetchall()
    for r in result:
        print(r)
    print("\n")

def editDomain(domain, masterIP, comment, assignedNodes, dnssec):
    connection, cursor = dbConnection()

    # find the domain the user asked for
    sql_command = '''
SELECT * FROM domain
WHERE domain= "''' + domain + '''";'''

    result = cursor.fetchall()

    # check if we get valid reply
    if len(cursor.fetchall()) == 0:
        print("nafsdmctl: invalid domain")
        return False
    result = cursor.fetchall()

    format_str = '''
UPDATE domain
SET masterIP = "{masterIP}", comment = "{comment}", assignedNodes = "{assignedNodes}", dnssec = "{dnssec}");
WHERE domain = "''' + domain + '''";'''

    if masterIP = None:
        masterIP = result[0][2]
    if comment = None:
        comment = result[0][3]
    if assignedNodes = None:
        assignedNodes = result[0][4]
    if dnssec = None:
        dnssec = result[0][5]

    sql_command = format_str.format(masterIP=masterIP, comment=comment, assignedNodes=assignedNodes, dnssec = dnssec)

    # execute update
    cursor.execute(sql_command)

    # close connection
    connection.commit()
    connection.close()

    return True
