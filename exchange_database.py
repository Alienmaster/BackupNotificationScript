import sqlite3

class exchange_database():

    def __init__(self):
        filename = "database.db"

        connection = sqlite3.connect(filename, check_same_thread=False)
        cursor = connection.cursor()

        self._connection = connection
        self._cursor = cursor

        # Init Tables
        self.init_tables()

    def init_tables(self):
        cursor = self._cursor

        sql_command_Mail = """
        CREATE TABLE IF NOT EXISTS Mail (
            ID VARCHAR PRIMARY KEY,
            MailID VARCHAR(100) UNIQUE,
            Subject VARCHAR(100),
            Mailadress VARCHAR(100),
            SenderID INTEGER,
            Body VARCHAR(100),
            Date DATETIME);"""

        sql_command_Customer = """
        CREATE TABLE IF NOT EXISTS Customer (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100),
            BackupMail VARCHAR(100),
            ContactPerson VARCHAR(100),
            ContactMail VARCHAR(100),
            ContactTelephone VARCHAR(100));"""
        
        sql_command_Solution = """
        CREATE TABLE IF NOT EXISTS Solution (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100),
            KeywordsInit VARCHAR(100),
            KeywordsSuccessful VARCHAR(100),
            KeywordsFailure VARCHAR(100));"""

        sql_command_CustomerSolution = """
        CREATE TABLE IF NOT EXISTS CustomerSolution (
            ID INTEGER PRIMARY KEY,
            CustomerID INTEGER,
            SolutionID INTEGER,
            FOREIGN KEY(CustomerID) REFERENCES Customer(ID));"""

        sql_command_Device = """
        CREATE TABLE IF NOT EXISTS Device (
            ID INTEGER PRIMARY KEY,
            Name VARCHAR(100),
            SolutionID INTEGER,
            FOREIGN KEY(SolutionID) REFERENCES Solution(ID));"""

        cursor.execute(sql_command_Mail)
        cursor.execute(sql_command_Customer)
        cursor.execute(sql_command_Solution)
        cursor.execute(sql_command_CustomerSolution)
        cursor.execute(sql_command_Device)

    def load_database(self):
        pass

    def add_mail(self, MailID, Subject, Mailadress, Body, Date):
        cursor = self._cursor
        connection = self._connection
        print(Date)
        cursor.execute("INSERT OR IGNORE INTO Mail (MailID, Subject, Mailadress, Body, Date) VALUES (?, ?, ?, ?, ?);" , (MailID, Subject, Mailadress, Body, Date))
        connection.commit()
    def read_mail(self):
        cursor = self._cursor

        cursor.execute('SELECT Subject FROM Mail')
        result = cursor.fetchall()
        print(result)

    def main(self):
        pass

if __name__ == "__main__":
    db = exchange_database()
    db.main()