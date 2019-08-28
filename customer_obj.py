class customer():

    def __init__(self):
        
        # Dictionary holds customer name, contact person, 
        # telephone number and email adress
        self._contact = {}

        # xxx holds all notification sources
        self._sources = {}

        print()


    ###### Getter ######
    def get_contact(self, key):
        contact = self._contact

        return contact[key]

    def get_source(self, key):
        source = self._sources

        return source[key]

    def name(self):
        '''
        :return: name of customer
        '''
        contact = self._contact

        return contact["name"]
    
    
    ###### Setter ######
    def set_contact(self, key, value):
        contact = self._contact

        contact[key] = value

    def set_source(self, key, value):
        sources = self._sources

        sources[key] = value
    
    
    def main(self):
        pass
    


if __name__ == "__main__":
    CS = customer()
    
    pass
