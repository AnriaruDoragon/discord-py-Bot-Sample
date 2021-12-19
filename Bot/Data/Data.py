import sqlite3, logging

class Database:

    def __init__(self):
        try:
            self.connection = sqlite3.connect("Bot/Data/client.db")
            self.cursor = self.connection.cursor()
        except sqlite3.Error as error:
            logging.critical(error)
        else:
            logging.info("Database connected.")
