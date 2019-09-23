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

        sql_command_Init = """
        PRAGMA foreign_keys = ON;
        """

        sql_command_Mail = """
        CREATE TABLE IF NOT EXISTS Mail (
            ID VARCHAR PRIMARY KEY,
            MailID VARCHAR(100) UNIQUE,
            Subject VARCHAR(100),
            Mailadress VARCHAR(100),
            SenderID INTEGER,
            Body VARCHAR(100),
            Date VARCHAR(100)
            FOREIGN KEY(SenderID) REFERENCES Customer(ID));"""

        sql_command_Customer = """
        CREATE TABLE IF NOT EXISTS Customer (
            ID INTEGER PRIMARY KEY UNIQUE,
            Name VARCHAR(100),
            BackupMail VARCHAR(100),
            ContactPerson VARCHAR(100),
            ContactMail VARCHAR(100),
            ContactTelephone VARCHAR(100));"""
        
        sql_command_Solution = """
        CREATE TABLE IF NOT EXISTS Solution (
            ID INTEGER PRIMARY KEY UNIQUE,
            Name VARCHAR(100),
            KeywordsInit VARCHAR(100),
            KeywordsSuccessful VARCHAR(100),
            KeywordsFailure VARCHAR(100));"""

        sql_command_CustomerSolution = """
        CREATE TABLE IF NOT EXISTS CustomerSolution (
            ID INTEGER PRIMARY KEY UNIQUE,
            CustomerID INTEGER,
            SolutionID INTEGER,
            FOREIGN KEY(CustomerID) REFERENCES Customer(ID));"""

        sql_command_Device = """
        CREATE TABLE IF NOT EXISTS Device (
            ID INTEGER PRIMARY KEY UNIQUE,
            Name VARCHAR(100),
            SolutionID INTEGER,
            FOREIGN KEY(SolutionID) REFERENCES Solution(ID));"""

        cursor.execute(sql_command_Init)
        cursor.execute(sql_command_Mail)
        cursor.execute(sql_command_Customer)
        cursor.execute(sql_command_Solution)
        cursor.execute(sql_command_CustomerSolution)
        cursor.execute(sql_command_Device)

    def load_database(self):
        pass

    ### Getter ###
    def get_mail(self):
        cursor = self._cursor

        cursor.execute('SELECT Subject FROM Mail')
        result = cursor.fetchall()
        print(result)

    def get_customer(self):
        cursor = self._cursor
        cursor.execute('SELECT * FROM Customer')
        result = cursor.fetchall()
        print(result)

    def get_device(self):
        cursor = self._cursor
        cursor.execute('SELECT * FROM Device')
        result = cursor.fetchall()
        print(result)

    ### Setter ###
    def add_mail(self, MailID, Subject, Mailadress, Body, Date):
        cursor = self._cursor
        connection = self._connection
        cursor.execute("INSERT OR IGNORE INTO Mail (MailID, Subject, Mailadress, Body, Date) VALUES (?, ?, ?, ?, ?);" , (MailID, Subject, Mailadress, Body, Date))
        connection.commit()

    def add_customer(self, Name, BackupMail, ContactPerson, ContactMail, ContactTelephone):
        cursor = self._cursor
        connection = self._connection
        cursor.execute("INSERT INTO Customer (Name, BackupMail, ContactPerson, ContactMail, ContactTelephone) VALUES (?, ?, ?, ?, ?);" , (Name, BackupMail, ContactPerson, ContactMail, ContactTelephone))
        connection.commit()

    def add_solution(self, Name, KeywordsInit, KeywordsSuccessful, KeywordsFailure):
        cursor = self._cursor
        connection = self._connection
        cursor.execute("INSERT INTO Solution (Name, KeywordsInit, KeywordsSuccessful, KeywordsFailure) VALUES (?, ?, ?, ?);" , (Name, KeywordsInit, KeywordsSuccessful, KeywordsFailure))
        connection.commit()
    
    def add_device(self, Name, SolutionID):
        cursor = self._cursor
        connection = self._connection
        cursor.execute("INSERT INTO Device (Name, SolutionID) VALUES (?, ?);", (Name, SolutionID))
        connection.commit()


    def main(self):
        pass

if __name__ == "__main__":
    db = exchange_database()
    db.main()
    db.add_customer("MRWare Computer", "mail@mrware.de", "M.R.", "werkstatt@mrware.de", "04174669790")
    db.add_solution("QNAP", "QNAP, qnap", "erfolgreich, successful", "failure")
    db.add_device("Klaus_NAS", 5)
    db.get_customer()
    db.get_device()
    db.get_mail()