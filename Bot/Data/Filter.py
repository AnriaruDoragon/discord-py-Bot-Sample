import sqlite3, logging

class Filter:

    def __init__(self, database):
        self.db = database
        try:
            self.db.cursor.execute("""CREATE TABLE IF NOT EXISTS "Filter" ("Guild" INTEGER NOT NULL, "Word" TEXT NOT NULL);""")
            self.db.connection.commit()
        except sqlite3.Error as error:
            logging.critical(error)
    
    def Get(self, Guild:int):
        try:
            self.db.cursor.execute("""SELECT "Word" FROM "Filter" WHERE "Guild" = ?;""", (Guild,))
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

    def Add(self, Guild:int, Words):
        data = [(Guild, word) for word in Words]
        try:
            self.db.cursor.executemany("""INSERT INTO "Filter" ("Guild", "Word") VALUES (?, ?);""", data)
            self.db.connection.commit()
        except sqlite3.Error as error:
            logging.error(error)
            return False
        except BaseException as error:
            logging.critical(error)
            return False
        else:
            return True

    def Remove(self, Guild:int, Words):
        data = [(Guild, word,) for word in Words]
        try:
            self.db.cursor.executemany("""DELETE FROM "Filter" WHERE "Guild" = ? AND "Word" = ?;""", data)
            self.db.connection.commit()
        except sqlite3.Error as error:
            logging.error(error)
            return False
        except BaseException as error:
            logging.critical(error)
            return False
        else:
            return True
