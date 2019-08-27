from exchangelib import Credentials, Account, Configuration, DELEGATE, Folder, EWSTimeZone, EWSDateTime, CalendarItem
from exchangelib.util import PrettyXmlHandler
import configparser, logging
import load_costumer

class BackupNotificationScript():
    def __init__(self):
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

        # Set Timezone to local Timezone
        self._tz = EWSTimeZone.localzone()
        # tz.localize(EWSDateTime.now())

        # Credentials and account
        self._credentials = Credentials(username = _Login["user"]
                            , password = _Login["password"])

        # Autodiscover fails w/o mail_config. See issue #337 on github exchangelib
        self._mail_config = Configuration(server = 'outlook.office365.com'
                            , credentials = self._credentials)

        self._account = Account(default_timezone=self._tz, primary_smtp_address = _Login["Primary_SMTP_Adress"], config = self._mail_config, credentials=self._credentials, autodiscover=False, access_type=DELEGATE)

    def generate_user(self):
        # For every txt File in Costumer generate a list/dictionary of values
        pass



    def analyze_mails(self):
        mails = self._mails

        # for item in mails:
        #     # print(item.subject)
        #     pass

    
    def create_Calender_item(self, _end, _subject, _body, _start = EWSDateTime.now()):
        tz = self._tz
        a = self._account

        startTime = tz.localize(_start)
        endTime = tz.localize(_end)
        subject = _subject
        body = _body

        newCalenderItem = CalendarItem(start=startTime, end=endTime, folder=a.calendar, subject=subject, body=body)
        newCalenderItem.save()

    def folder_print(self):
        tz = self._tz
        a = self._account
        # notaware DateTime
        endTime = EWSDateTime(2019,8,27,17,00,0)
        # aware DateTime
        # endTime = tz.localize(endTime)

        a.root.refresh()
        # a.public_folders_root.refresh()
        # a.archive_root.refresh()
        backupFolder = a.root // "Oberste Ebene des Informationsspeichers" // "Posteingang" // "!backup"


        for item in backupFolder.all()[:10]:
            if "finished" in item.body:
                print(item.subject)
                self.create_Calender_item(_start=EWSDateTime.now(), _end=endTime, _subject=item.subject, _body="MRWare Computer /n Erfolg")

        # print(a.root.tree())
        # print(inbox.children)


    def main(self):
        account = self._account

        # for item in account.inbox.all().order_by('-datetime_received')[:10]:
        #     print(item.subject, item.sender)

        self._mails = account.inbox.all().order_by('-datetime_received')[:10]
        
        self.analyze_mails()
        self.folder_print()

if __name__ == "__main__":
    BNS = BackupNotificationScript()
    BNS.main()