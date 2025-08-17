
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------                                                                                                                             # Import os and sys modules for operating system and system-specific functions
#?                                                __  __ _              _ _                                                                                   # ASCII art for BMW logo
#?                                               |  \/  (_)___  ___ ___| | | __ _ _ __   ___  ___  _   _ ___                                                  # ASCII art for BMW logo
#?                                               | |\/| | / __|/ __/ _ \ | |/ _` | '_ \ / _ \/ _ \| | | / __|                                                 # ASCII art for BMW logo
#?                                               | |  | | \__ \ (_|  __/ | | (_| | | | |  __/ (_) | |_| \__ \                                                 # ASCII art for BMW logo
#?                                               |_|  |_|_|___/\___\___|_|_|\__,_|_| |_|\___|\___/ \__,_|___/                                                 # ASCII art for BMW logo
#?                                                                                                                                                            # 
#?-------------------------------------------------------------------------------------------------------------------------------------------------------------                                                                                                                             # End of ASCII art section
import os,sys                                                                                                                                                 # Import os and sys modules
sys.path.insert(1,os.getcwd() + '/Script/assets')                                                                                                             # Add Script/assets directory to Python path
import Dependencies as dp                                                                                                                                      # Import Dependencies module as dp

#?-------------------------------------------------------------------------------------------------------------------------------------------------------------                                                                                                                             # Class definition separator
class Misc :                                                                                                                                                  # Define Misc class
    def __init__(self):                                                                                                                                       # Define __init__ method

        self.TicToc                 =   self.TicTocGenerator()                  #! create an instance of the TicTocGen generator                                # Initialize TicToc generator
        self.mode                   =   ''                                                                                                                    # Initialize mode attribute
        self.map_index              =   ''                                                                                                                    # Initialize map_index attribute
        self.map_names              =   ''                                                                                                                    # Initialize map_names attribute
        self.maxThreads             =   1                                                                                                                    # Initialize maxThreads attribute

    def listMethods(self,Class):                                                                                                                              # Define listMethods method
        """
        listMethods(< Class >: Class Name)
        Prints out a list of all the methods defined
        inside a given class : Class

        Args:
            Class (Class): Python class
        """
        method_list =   [method for method in dir(Class) if method.startswith('__') is False]                                                                  # Create list of non-dunder methods
        print(method_list)                                                                                                                                     # Print method list

    def TicTocGenerator(self):                                                                                                                                 # Define TicTocGenerator method
        """
        Generator that returns time differences

        Yields:
            float: returns the time difference
        """
        ti = 0              # initial time                                                                                                                     # Initialize initial time
        tf = dp.time.time() # final time                                                                                                                      # Get current time
        while True:                                                                                                                                           # Infinite loop
            ti = tf                                                                                                                                           # Set initial time to previous final time
            tf = dp.time.time()                                                                                                                                # Get current time
            yield tf-ti                                                                                                                                       # Yield time difference

    def toc(self,tempBool=True):                                                                                                                               # Define toc method
        """
            Records a time in TicToc, marks the end of a time interval

        Args:
            tempBool (bool, optional): token used to mark the end. Defaults to True.

        Returns:
            float: time difference returned by generator.
        """
        tempTimeInterval = next(self.TicToc)                                                                                                                   # Get next time interval from generator
        if tempBool:                                                                                                                                           # Check if tempBool is True
            return tempTimeInterval                                                                                                                            # Return time interval

    def tic(self):                                                                                                                                             # Define tic method
        """
        Records a time in TicToc, marks the beginning of a time interval
        """
        self.toc(False)                                                                                                                                        # Call toc with False parameter

    def keys_exists(self,ref_dict,res_dict):                                                                                                                   # Define keys_exists method
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
        key_list    =   list(ref_dict.keys())                                                                                                                   # Get list of keys from reference dictionary
        if not isinstance(res_dict, dict):                                                                                                                     # Check if res_dict is a dictionary
            raise AttributeError('keys_exists() expects dict as first argument.')                                                                              # Raise error if not dictionary
        if len(key_list) == 0:                                                                                                                                 # Check if key list is empty
            raise AttributeError('keys_exists() expects at least two arguments, one given.')                                                                   # Raise error if empty

        _element = dp.copy.deepcopy(res_dict)                                                                                                                   # Create deep copy of result dictionary
        for key in key_list:                                                                                                                                   # Iterate through key list
            try:                                                                                                                                               # Try to access nested key
                _element = _element[key]                                                                                                                       # Access nested dictionary
            except KeyError:                                                                                                                                   # Handle KeyError
                break                                                                                                                                          # Break loop if key not found
            del res_dict[key]                                                                                                                                 # Delete key from result dictionary
        return res_dict                                                                                                                                       # Return modified dictionary

    def transform_key_paths(self,key_paths):                                                                                                                   # Define transform_key_paths method
        """
        Converts a list of dot-separated key paths into bracketed string key paths.

        Args:
            key_paths (list of str): A list of key paths represented as dot-separated strings (e.g., 'a.b.c').

        Returns:
            list of str: A list of transformed key paths in the format "['a']['b']['c']".
        """
        converted_keys = []                                                                                                                                    # Initialize empty list for converted keys
        for key in key_paths:                                                                                                                                  # Iterate through key paths
            new_key = "['" + "']['".join(key.split('.')) + "']"                                                                                                # Convert dot notation to bracket notation
            converted_keys.append(new_key)                                                                                                                     # Add converted key to list
        return converted_keys                                                                                                                                  # Return list of converted keys

    def update_dict_value(self,d, key_path, multiplier):                                                                                                       # Define update_dict_value method
        """
        Updates the value in a nested dictionary at the specified key path by applying a multiplier.

        Args:
            d (dict): The dictionary to update.
            key_path (str): The key path represented as a bracketed string (e.g., "['a']['b']['c']").
            multiplier (float): The multiplier to apply to the value at the specified key path.

        Returns:
            None: The input dictionary is modified in place.
        """
        keys = key_path.strip("[]").replace("']['", "/").replace("'", "").split("/")                                                                          # Parse key path into list of keys
        temp = d                                                                                                                                              # Initialize temporary dictionary
        for key in keys[:-1]:                                                                                                                                  # Iterate through all keys except last
            temp = temp.get(key, {})                                                                                                                          # Access nested dictionary
        last_key = keys[-1]                                                                                                                                    # Get last key
        if last_key in temp:                                                                                                                                   # Check if last key exists
            temp[last_key] = temp[last_key] + temp[last_key] * multiplier                                                                                      # Update value with multiplier

    def flatten_dict(self,d, parent_key='', sep='.'):                                                                                                           # Define flatten_dict method
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
        items = []                                                                                                                                            # Initialize empty list for items
        for k, v in d.items():                                                                                                                                # Iterate through dictionary items
            new_key = f"{parent_key}{sep}{k}" if parent_key else k                                                                                            # Create new key with separator
            if isinstance(v, dict):                                                                                                                            # Check if value is dictionary
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())                                                                                  # Recursively flatten nested dictionary
            else:                                                                                                                                              # Handle non-dictionary values
                if callable(v):                                                                                                                               # Check if value is callable
                    v = v()                                                                                                                                   # Execute callable
                if isinstance(v, str):                                                                                                                         # Check if value is string
                    v = f"'{v}'"                                                                                                                              # Wrap string in quotes
                items.append((new_key, v))                                                                                                                     # Add key-value pair to items
        return dict(items)                                                                                                                                     # Return flattened dictionary

    def dict_to_string(self,d, sep='.'):                                                                                                                       # Define dict_to_string method
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
        flattened_dict = self.flatten_dict(d, sep=sep)                                                                                                         # Flatten dictionary
        return '\n'.join(f"{key}={value};" for key, value in flattened_dict.items())                                                                           # Convert to string with key=value; format

    def InitializationCommands(self, input_file, output_file, flat_dict ,m_file):                                                                              # Define InitializationCommands method
        """
        Replaces lines containing `search_expr` in the input file with content from `flat_dict`.
        The modified content is written to `output_file`. Specifically, if `InitializationCommands ""`
        is found, it inserts the `flat_dict` content inside the quotes.

        Args:
            input_file (str)        : Path to the input file.
            output_file (str)       : Path to the output file.
            flat_dict (list): List of strings to replace the matching line.
        """
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:                                         # Open input and output files
            flattened_str_dot           = self.dict_to_string(flat_dict, sep='.')                                                                             # Convert dictionary to dot-separated string
            for line in infile:                                                                                                                               # Read input file line by line
                    if 'InitializationCommands ""' in line:                                                                                                   # Check for target line
                        updated_line = line.split('""')[0] + ' "' + flattened_str_dot + "\n" +'"'                                                             # Create updated line with dictionary content
                        outfile.write(updated_line)                                                                                                            # Write updated line
                    else:                                                                                                                                      # For non-target lines
                        outfile.write(line)                                                                                                                    # Write original line
        os.makedirs(os.path.dirname(m_file), exist_ok=True)                                                                                                  # Create directories for m_file if needed
        with open(m_file, 'w', encoding='utf-8') as m_out:                                                                                                    # Open m_file for writing
            m_out.write(flattened_str_dot)                                                                                                                    # Write flattened string to m_file
        m_out.close()                                                                                                                                         # Close m_file