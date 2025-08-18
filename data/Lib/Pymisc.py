
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
#?                                                __  __ _              _ _
#?                                               |  \/  (_)___  ___ ___| | | __ _ _ __   ___  ___  _   _ ___
#?                                               | |\/| | / __|/ __/ _ \ | |/ _` | '_ \ / _ \/ _ \| | | / __|
#?                                               | |  | | \__ \ (_|  __/ | | (_| | | | |  __/ (_) | |_| \__ \
#?                                               |_|  |_|_|___/\___\___|_|_|\__,_|_| |_|\___|\___/ \__,_|___/
#?
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
import os,sys
sys.path.insert(1,os.getcwd() + '/Script/assets')
import Dependencies as dp

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------
class Misc :
    def __init__(self):

        self.TicToc                 =   self.TicTocGenerator()                  #! create an instance of the TicTocGen generator
        self.mode                   =   ''
        self.map_index              =   ''
        self.map_names              =   ''
        self.maxThreads             =   1

    def listMethods(self,Class):
        """
        listMethods(< Class >: Class Name)
        Prints out a list of all the methods defined
        inside a given class : Class

        Args:
            Class (Class): Python class
        """
        method_list =   [method for method in dir(Class) if method.startswith('__') is False]
        print(method_list)

    def TicTocGenerator(self):
        """
        Generator that returns time differences

        Yields:
            float: returns the time difference
        """
        ti = 0              # initial time
        tf = dp.time.time() # final time
        while True:
            ti = tf
            tf = dp.time.time()
            yield tf-ti

    def toc(self,tempBool=True):
        """
            Records a time in TicToc, marks the end of a time interval

        Args:
            tempBool (bool, optional): token used to mark the end. Defaults to True.

        Returns:
            float: time difference returned by generator.
        """
        # return the time difference yielded by generator instance TicToC
        tempTimeInterval = next(self.TicToc)
        if tempBool:
            return tempTimeInterval

    def tic(self):
        """
        Records a time in TicToc, marks the beginning of a time interval
        """
        self.toc(False)

    def keys_exists(self,ref_dict,res_dict):
        """
        Checks if a set of keys from a given dictionary exists in the other dictionary
        then removes those keys and returns the rest as dictionary.

        Args:
            ref_dict (dict): reference dictionary for keys.
            res_dict (dict): source dictionary to scrape for existing keys.

        Raises:
            AttributeError: raises error if attribut is not of type dictionary.
            AttributeError: raises error if length of key_list is null.

        Returns:
            dict            : result dictionary without exisiting keys.
        """
        key_list    =   list(ref_dict.keys())
        if not isinstance(res_dict, dict):
            raise AttributeError('keys_exists() expects dict as first argument.')
        if len(key_list) == 0:
            raise AttributeError('keys_exists() expects at least two arguments, one given.')

        _element = dp.copy.deepcopy(res_dict)
        for key in key_list:
            try:
                _element = _element[key]
            except KeyError:
                break
            # res_dict.pop(key)
            del res_dict[key]
        return res_dict

    def transform_key_paths(self,key_paths):
        """
        Converts a list of dot-separated key paths into bracketed string key paths.

        Args:
            key_paths (list of str): A list of key paths represented as dot-separated strings (e.g., 'a.b.c').

        Returns:
            list of str: A list of transformed key paths in the format "['a']['b']['c']".
        """
        converted_keys = []
        for key in key_paths:
            new_key = "['" + "']['".join(key.split('.')) + "']"
            converted_keys.append(new_key)
        return converted_keys

    def update_dict_value(self,d, key_path, multiplier):
        """
        Updates the value in a nested dictionary at the specified key path by applying a multiplier.

        Args:
            d (dict): The dictionary to update.
            key_path (str): The key path represented as a bracketed string (e.g., "['a']['b']['c']").
            multiplier (float): The multiplier to apply to the value at the specified key path.

        Returns:
            None: The input dictionary is modified in place.
        """
        keys = key_path.strip("[]").replace("']['", "/").replace("'", "").split("/")
        temp = d
        for key in keys[:-1]:
            temp = temp.get(key, {})
        last_key = keys[-1]
        if last_key in temp:
            temp[last_key] = temp[last_key] + temp[last_key] * multiplier

    def flatten_dict(self,d, parent_key='', sep='.'):
        """
        Flatten a nested dictionary into a single-level dictionary, where nested keys
        are joined by the specified separator.

        Args:
            d (dict): The dictionary to be flattened.
            parent_key (str, optional): The base key to prepend to each key (default is '').
            sep (str, optional): The separator to use between nested keys (default is '.').

        Returns:
            dict: A flattened dictionary with keys joined by the separator.

        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                # If the value is callable, execute it
                if callable(v):
                    v = v()  # Execute the function to get its result
                # If the value is a string, we wrap it in quotes
                if isinstance(v, str):
                    v = f"'{v}'"  # Wrap the string in single quotes, including paths
                items.append((new_key, v))
        return dict(items)

    def dict_to_string(self,d, sep='.'):
        """
        Convert a flattened dictionary into a formatted string where each key-value pair
        is represented as `key=value;` with each pair on a new line.

        Args:
            d (dict): The dictionary to be converted to a string.
            sep (str, optional): The separator used for flattening (default is '.').

        Returns:
            str: A string representing the flattened dictionary, with each key-value pair
                on a new line in the format `key=value;`.
        """
        flattened_dict = self.flatten_dict(d, sep=sep)
        # Convert dictionary to string with `key=value;` format, each pair on a new line
        return '\n'.join(f"{key}={value};" for key, value in flattened_dict.items())
