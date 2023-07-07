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
        try:
            with open(self.filepath) as file:
                data = json.load(file)
                return data.get(key)
        except FileNotFoundError:
            print(f"Error: File '{self.filepath}' not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in file '{self.filepath}'.")
            return None


    def setdata(self, key, value):
        """Sets a key to a specific value in a json file
        Parameters
        ------------
        str key: The key to set
        str value: The value to set the key to
        """
        try:
            with open(self.filepath, 'r') as file:
                data = json.load(file)
                data[key] = value

            with open(self.filepath, 'w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            print(f"Error: File '{self.filepath}' not found.")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in file '{self.filepath}'.")
