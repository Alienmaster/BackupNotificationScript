import os, configparser, logging
import customer_obj

class load_customer():
        
    def __init__(self):
        # choose Directory of customer ini files
        self._directory = "configurations"

        # Read all ini files of the "directory" and store it
        self.make_a_list_with_all_ini_files()
        
        # parse a List of sublists for every customer
        self.create_list_of_parser()


    def make_a_list_with_all_ini_files(self):
        '''
        Lists every file in the directory and adds every .ini File
        into the customerFileList
        '''
        directory = self._directory
        customerFileList = []
        #TODO Check if directory exists
        #TODO Check if files exists
        FileList = os.listdir(directory)
        for f in FileList:
            if ".ini" in f:
                customerFileList.append(f)
        self._customerFileList = customerFileList
        
    def create_list_of_parser(self):
        '''
        For every .ini File in the customeFileList it reads the config with
        the configparser and creates an customer_object in and 
        stores in the customerList dict.
        customerList key = name of customer
        customerList value = object of custumer
        '''
        customerFileList = self._customerFileList
        directory = self._directory

        customerList = {}
        customer = configparser.ConfigParser()
        customer.read("%s/MRWare.txt", directory)
        
        for c in customerFileList:
            customer = configparser.ConfigParser()
            customer.read("%s/%s" % (directory, c))
            co = customer_obj.customer()
            for d in customer.items("customer"):
                co.set_contact(d[0], d[1])
            customerList[co.name()] = co

        print(customerList)
        self._customerList = customerList
        # print(customerList["MRWare Computer"].get_contact("mail"))
            
    ##### Getter #####
    def get_customer_list(self):
        return self._customerList

    ##### Setter #####
    # I think i dont need any^^

 
    def main(self):
        # pass
        # write Test
        # print(self._customerList)

        # logger
        logging.basicConfig(level=logging.INFO)
        self._logger = logging.getLogger(__name__)

if __name__ == "__main__":
    LS = load_customer()
    LS.main()