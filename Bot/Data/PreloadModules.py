import sqlite3, logging

class PreloadModules:

    def __init__(self, database):
        self.db = database
        try:
            self.db.cursor.execute("""CREATE TABLE IF NOT EXISTS "PreloadModules" ("Module" INTEGER NOT NULL);""")
            self.db.connection.commit()
        except sqlite3.Error as error:
            logging.critical(error)
    
    def Get(self):
        try:
            self.db.cursor.execute("""SELECT "Module" FROM "PreloadModules";""")
            results = self.db.cursor.fetchall()
            if results:
                # Convert [('1',), ('2',)] into ['1', '2']
                return [word for result in results for word in result]
            else:
                # Empty list []
                return results
        except sqlite3.Error as error:
            logging.critical(error)
        except Exception as error:
            logging.warning(error)
    
    def Add(self, Module:str):
        try:
            self.db.cursor.execute("""INSERT INTO "PreloadModules" ("Module") VALUES (?);""", (Module,))
            self.db.connection.commit()
        except sqlite3.Error as error:
            logging.error(error)
            return False
        except BaseException as error:
            logging.critical(error)
            return False
        else:
            return True
    
    def Remove(self, Module:str):
        try:
            self.db.cursor.execute("""DELETE FROM "PreloadModules" WHERE "Module" = ?;""", (Module,))
            self.db.connection.commit()
        except sqlite3.Error as error:
            logging.error(error)
            return False
        except BaseException as error:
            logging.critical(error)
            return False
        else:
            return True
