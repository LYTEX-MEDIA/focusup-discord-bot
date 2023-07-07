import json


class Config:
    def __init__(self, filepath):
        self.filepath = filepath

    def getdata(self, key):
        """Returns a key from a specific json file
        Parameters
        ------------
        str key: The key to get from the json file
        """
        with open(self.filepath) as file:
            data = json.load(file)
            return data.get(key)


    def setdata(self, key, value):
        """Sets a key to a specific value in a json file
        Parameters
        ------------
        str key: The key to set
        str value: The value to set the key to
        """
        with open(self.filepath) as file:
            data = json.load(file)
            data[key] = value
            
        with open(self.filepath, 'w') as file:
            json.dump(data, file, indent=4)
