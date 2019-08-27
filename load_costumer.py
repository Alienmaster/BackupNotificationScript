import os, configparser

class load_customer():
        
    def __init__(self):
        # choose Directory of customer ini files
        self._directory = "configurations"

        # Read all ini files of the "directory" and store it
        self.make_a_list_with_all_ini_files()

        # parse a List of sublists for every customer
        self.create_list_of_parser()

    def make_a_list_with_all_ini_files(self):
        directory = self._directory
        customerFileList = []
        
        FileList = os.listdir(directory)
        for f in FileList:
            if ".ini" in f:
                customerFileList.append(f)
        self._customerList = customerFileList
        

    def create_list_of_parser(self):
        customerFileList = self._customerList
        directory = self._directory

        customerList = []
        customer = configparser.ConfigParser()
        customer.read("%s/MRWare.txt", directory)
        
        for c in customerFileList:
            customer = configparser.ConfigParser()
            customer.read("%s/%s" % (directory, c))
            # customerList.append()
            print(customer.items("customer"))
            customerList[c].append(customer.items("customer"))
            for d in customer.items("customer"):
                print(d)
            
        # print(customer.sections())
        # for item in CL:
        #     customer = configparser.ConfigParser()
        #     customer.read("MRWare.txt")
        #     # abc = customer["MRW"]
        #     print(customer[Default])
        #     # CLP.append()
            
        self._customerList = customerList
            
    def main(self):
        
        print(self._customerList)

if __name__ == "__main__":
    LS = load_customer()
    LS.main()