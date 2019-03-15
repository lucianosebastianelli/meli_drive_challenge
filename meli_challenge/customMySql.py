from __future__ import print_function


import mysql.connector
from mysql.connector import errorcode


def checkTableExists(DBCON, TABLENAME):
    db_cur = DBCON.cursor()
    db_cur.execute("SHOW TABLES like '%s'" %(TABLENAME, ))
    if db_cur.fetchone():
        db_cur.close()
        return True
    db_cur.close()
    return False


class customMySql:
    def __init__(self,DB_PROPERTIES):
        self.DB_PROPERTIES = DB_PROPERTIES
    def createDbConnection(self):
        try:
            db_con = mysql.connector.connect(host=self.DB_PROPERTIES['host'],
                                             user=self.DB_PROPERTIES['user'],
                                             password=self.DB_PROPERTIES['password'])
            db_cur = db_con.cursor()
            db_cur.execute("CREATE DATABASE IF NOT EXISTS %s" %(self.DB_PROPERTIES['database'], ))
            db_con.connect(database=self.DB_PROPERTIES['database'])

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Algo salió mal con el nombre de usuario o contraseña. No se pudo conectar a MySQL.")
            else:
                print("Código de error: " + str(err.errno) + " " + str(err.msg))
        if (db_con.is_connected()):
            db_cur.close()

        return db_con

    def dbInit(self, DB_CON):
        FIRST_RUN = False
        if not checkTableExists(DB_CON, self.DB_PROPERTIES['f_table']):
            try:
                db_cur = DB_CON.cursor()
                db_cur.execute("CREATE TABLE %s (id VARCHAR(50), name VARCHAR(255) CHARACTER SET utf8 COLLATE "
                               "utf8_general_ci, extention VARCHAR(25),"
                               " owner VARCHAR(50), public BOOL,"
                               " modifiedTime VARCHAR(24), trashed BOOL)" % (self.DB_PROPERTIES['f_table'], ))
                # print("La tabla %s fue creada" % self.DB_PROPERTIES['f_table'])
                FIRST_RUN = True

            except mysql.connector.Error as err:
                print("Código de error: " + str(err.errno) + " " + str(err.msg))
        # else:
        #    print("La tabla %s ya existe" % self.DB_PROPERTIES['f_table'])

        if not checkTableExists(DB_CON, self.DB_PROPERTIES['p_h_table']):
            try:
                db_cur = DB_CON.cursor()
                db_cur.execute("CREATE TABLE %s (id VARCHAR(50), name VARCHAR(255) CHARACTER SET utf8 COLLATE "
                               "utf8_general_ci, extention VARCHAR(25),"
                               " owner VARCHAR(50), foundTime VARCHAR(24), trashed BOOL, ownedByMe BOOL)" % (
                               self.DB_PROPERTIES['p_h_table'],))
                # print("La tabla %s fue creada" % self.DB_PROPERTIES['p_h_table'])
                FIRST_RUN = True
            except mysql.connector.Error as err:
                print("Código de error: " + str(err.errno) + " " + str(err.msg))
        # else:
        #    print("La tabla %s ya existe" % self.DB_PROPERTIES['p_h_table'])

        if FIRST_RUN:
            db_cur.close()

        return FIRST_RUN




