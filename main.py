from exchangelib import Credentials, Account, Configuration, DELEGATE, Folder, EWSTimeZone, EWSDateTime, CalendarItem
from exchangelib.util import PrettyXmlHandler
import configparser, logging
import datetime
import load_customer
import exchange_database

import inspect

class BackupNotificationScript():
    def __init__(self):
        # Set Timezone to local Timezone
        self._tz = EWSTimeZone.localzone()

        # set start and end time of Calendarentry
        self.init_time()

        # Logger
        logging.basicConfig(level=logging.WARNING, handlers=[PrettyXmlHandler()])

        # Config Parser
        config = configparser.ConfigParser()
        config.read('config.txt')
        try:
            LoginData = config["Credentials"]
        except KeyError as error:
            print('The key ' + str(error) + ' were not found in the config file')
            exit()

        _Login = {  
                                    "user": LoginData['user'],
                                    "password": LoginData['password'],
                                    "Primary_SMTP_Adress": LoginData['Primary SMTP Adress']
                            }

        # Credentials and account
        self._credentials = Credentials(username = _Login["user"]
                            , password = _Login["password"])

        # Autodiscover fails w/o mail_config. See issue #337 on github exchangelib
        self._mailConfig = Configuration(server = 'outlook.office365.com'
                            , credentials = self._credentials)

        self._account = Account(default_timezone=self._tz, 
                                primary_smtp_address = _Login["Primary_SMTP_Adress"], 
                                config = self._mailConfig, 
                                credentials=self._credentials, 
                                autodiscover=False, 
                                access_type=DELEGATE)

        # Init Database
        self._db = exchange_database.exchange_database()

    def init_time(self):
        '''
        Initialize the time with start and endTime
        saves a localized EWSDateTime formatted start and endtime
        '''
        tz = self._tz

        today = datetime.date.today()
        st = datetime.time(hour=21, minute=00)
        et = datetime.time(hour=22, minute=00)
        # forgive me father because I have sinned
        self._startTime = EWSDateTime.from_datetime(tz.localize(datetime.datetime.combine(today, st)))
        self._endTime = EWSDateTime.from_datetime(tz.localize(datetime.datetime.combine(today, et)))

    def load_customer(self):
        CL = load_customer.load_customer()
        CL = CL.get_customer_list()

        print(CL)
        
    def analyze_mails(self):
        mails = self._mails

        # for item in mails:
        #     # print(item.subject)
        #     pass

    
    def create_Calender_item(self, subject, body,):
        '''
        creates Calendar item
        uses the global startTime and endTime
        :param str _subject: Subject of the calendar entry
        :param str _body: content of the calendar entry
        '''

        startTime = self._startTime
        endTime = self._endTime
        
        a = self._account

        newCalenderItem = CalendarItem(start=startTime, end=endTime, folder=a.calendar, subject=subject, body=body)
        newCalenderItem.save()

    def update_Calender_item(self):

        pass


    def folder_print(self):
        '''
        Does actual to much stuff
        Kind of testing method for playing purposes
        '''
        tz = self._tz
        a = self._account

        a.root.refresh()
        # a.public_folders_root.refresh()
        # a.archive_root.refresh()
        folder = a.root // "Oberste Ebene des Informationsspeichers" // "Posteingang" // "!backup"
        # folder = a.root // "Oberste Ebene des Informationsspeichers" // "Posteingang"


        for item in folder.all()[:10]:
            if "finished" in item.body:
                print(item.subject)
                self.create_Calender_item(subject=item.subject, body="MRWare Computer /n Erfolg")

    def get_mails(self):
        account = self._account

        # Get the last 10 Mails of the inbox in order and put them into _mails
        self._mails = account.inbox.all().order_by('-datetime_received')[:20]

    def write_mails_to_database(self):
        db = self._db
        mails = self._mails

        for m in mails:
            # print(m.datetime_received.strftime("%m/%d/%Y, %H:%M:%S"))

            db.add_mail(m.id, m.subject, m.sender.email_address, m.body, m.datetime_received.strftime("%m/%d/%Y, %H:%M:%S"))
            # print( m.id)

        db.get_mail()


    def main(self):
        self.get_mails()
        self.write_mails_to_database()
        self.analyze_mails()

        # self.analyze_mails()
        # self.folder_print()

if __name__ == "__main__":
    BNS = BackupNotificationScript()
    BNS.main()