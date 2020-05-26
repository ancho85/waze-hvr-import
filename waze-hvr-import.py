# encoding: ISO8859-1
#!/usr/bin/env python
import sys
import os
import re
import ConfigParser

HERE = os.path.dirname(os.path.realpath(__file__))
CONFIGPATH = os.path.join(HERE, "waze-hvr-import.cfg")

def getConfig():
    config = ConfigParser.ConfigParser()
    f = open(CONFIGPATH, "r")
    config.readfp(f)  # the configuration file can change, so it must be opened every time
    f.close()
    return config

def executeSQL(txt):
    """validates sql string using command line"""
    config = getConfig()
    config = getConfig()
    if config.get("mysql", "dbname") == "databasename":
        print "MySQL database is not configured. Check waze-hvr-import.cfg file"
        return
    if config.get("mysql", "pass") == "******":
        print "MySQL password is not configured. Check waze-hvr-import.cfg file"
        return
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
    sql += "segnodes_modified INTEGER,\n"
    sql += "segnodes_deleted INTEGER,\n"
    sql += "seg_split_merges INTEGER,\n"
    sql += "venues_handled INTEGER,\n"
    sql += "road_closures_handled INTEGER,\n"
    sql += "map_problems_closed INTEGER,\n"
    sql += "update_requests_closed INTEGER,\n"
    sql += "house_number_handled INTEGER,\n"
    sql += "UNIQUE INDEX date_user (date, user),\n"
    sql += "INDEX user (user)\n"
    sql += "\n)DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs"
    sql += "\nENGINE=InnoDB"
    executeSQL(sql)

def cvs_importer():
    for root, dirnames, filenames in os.walk(os.path.join(HERE, "import")):
        for fname in filenames:
            if not fname.endswith(".csv"):
                continue
            print "importing", fname
            f = open(os.path.join(HERE, "import", fname), "r")
            if not f:
                print "file %s not found" % fname
                continue
            linenr = -1
            for row in f.readlines():
                linenr += 1
                if linenr == 0:
                    continue
                the_date = "%s/%s/%s" % (fname.split("-")[1], fname.split("-")[2], fname.split("-")[3])
                line = row.split(",")
                fieldnames = ["user", "rank", "total_edits"]
                fieldnames += ["segnodes_created", "segnodes_modified", "segnodes_deleted"]
                fieldnames += ["seg_split_merges", "venues_handled", "road_closures_handled"]
                fieldnames += ["map_problems_closed", "update_requests_closed", "house_number_handled"]
                sql = "INSERT INTO waze_hvr (date,%s) VALUES (" % ",".join(fieldnames)
                values = ["'%s'" % the_date]
                for idx, fn in enumerate(fieldnames):
                    if fn == "user":
                        values.append("'%s'" % line[idx])
                    else:
                        values.append(line[idx])
                sql += ",".join(values) + ");\n"
                executeSQL(sql)
            f.close()


if __name__ == '__main__':
    sql_table_creator()
    cvs_importer()
    sys.exit(0)
