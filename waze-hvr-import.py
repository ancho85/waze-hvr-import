# encoding: ISO8859-1
#!/usr/bin/env python
import sys
import os
import re
import ConfigParser
CONFIGPATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "waze-hvr-import.cfg")

def getConfig():
    config = ConfigParser.ConfigParser()
    f = open(CONFIGPATH, "r")
    config.readfp(f)  # the configuration file can change, so it must be opened every time
    f.close()
    return config

def executeSQL(txt, config):
    """validates sql string using command line"""

    import subprocess
    mysqlcmd = ["%s/mysql" % config.get("mysql", "%spath" % os.name)]
    mysqlcmd.append("-u%s" % config.get('mysql', 'user'))
    pwd = config.get('mysql', 'pass')
    if pwd: mysqlcmd.append("-p%s" % pwd)
    mysqlcmd.append("-h%s" % config.get('mysql', 'host'))
    mysqlcmd.append("-P%s" % config.get('mysql', 'port'))
    mysqlcmd.append("-D%s" % config.get('mysql', 'dbname'))
    mysqlcmd.append("--batch")
    mysqlcmd.append("--execute")
    mysqlcmd.append("%s" % txt)
    subprocess.Popen(mysqlcmd) # , stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def sql_table_creator():
    sql = "CREATE TABLE IF NOT EXISTS waze_hvr(\n"
    sql += "internalId INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,\n"
    sql += "date DATE,\n"
    sql += "user VARCHAR(100),\n"
    sql += "rank INTEGER,\n"
    sql += "total_edits INTEGER,\n"
    sql += "segnodes_created INTEGER,\n"
    sql += "segnodes_edited INTEGER,\n"
    sql += "segnodes_modified INTEGER,\n"
    sql += "segnodes_deleted INTEGER,\n"
    sql += "seg_split_merges INTEGER,\n"
    sql += "venues_handled INTEGER,\n"
    sql += "road_closures_handled INTEGER,\n"
    sql += "map_problems_closed INTEGER,\n"
    sql += "update_requests_closed INTEGER,\n"
    sql += "house_number_handled INTEGER,\n"
    sql += "editing_age VARCHAR(100),\n"
    sql += "UNIQUE INDEX date_user (date, user)\n"
    sql += "\n)DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs"
    sql += "\nENGINE=InnoDB"
    return sql

def main():
    config = getConfig()
    if config.get("mysql", "dbname") == "databasename":
        return "MySQL database is not configured. Check waze-hvr-import.cfg file"
    if config.get("mysql", "pass") == "******":
        return "MySQL password is not configured. Check waze-hvr-import.cfg file"
    executeSQL(sql_table_creator(), config)
    return True




if __name__ == '__main__':
    res = main()
    if not res: print res
    sys.exit(0)
