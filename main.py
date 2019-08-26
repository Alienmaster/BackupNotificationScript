from exchangelib import Credentials, Account, Configuration, DELEGATE, Folder, EWSTimeZone, EWSDateTime
from exchangelib.util import PrettyXmlHandler
import configparser, logging

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
        tz = EWSTimeZone.localzone()
        # tz.localize(EWSDateTime.now())

        # Credentials and account
        self._credentials = Credentials(username = _Login["user"]
                            , password = _Login["password"])

        # Autodiscover fails w/o mail_config. See issue #337 on github exchangelib
        self._mail_config = Configuration(server = 'outlook.office365.com'
                            , credentials = self._credentials)

        self._account = Account(default_timezone=tz, primary_smtp_address = _Login["Primary_SMTP_Adress"], config = self._mail_config, credentials=self._credentials, autodiscover=False, access_type=DELEGATE)


    def analyze_mails(self):
        mails = self._mails

        for item in mails:
            print(item.subject)
        pass

    def folder_print(self):
        a = self._account
        a.root.refresh()
        # a.public_folders_root.refresh()
        # a.archive_root.refresh()
        backupFolder = a.root // "Oberste Ebene des Informationsspeichers" // "Posteingang" // "!backup"
        
        for item in backupFolder.all()[:10]:
            if "finished" in item.body:
                print(item.subject)

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