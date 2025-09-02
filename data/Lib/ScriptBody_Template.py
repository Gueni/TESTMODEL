class TrackableDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignments = {}
        # Convert all nested dictionaries to TrackableDict during initialization
        self._convert_nested_dicts()
    
    def _convert_nested_dicts(self):
        """Convert all nested dictionaries to TrackableDict"""
        for key, value in list(self.items()):
            if isinstance(value, dict) and not isinstance(value, TrackableDict):
                trackable_value = TrackableDict(value)
                super().__setitem__(key, trackable_value)
                # Record this initial assignment
                path = f"dict['{key}']"
                self.assignments[path] = trackable_value
    
    def __setitem__(self, key, value):
        # Handle nested dictionaries - convert them to TrackableDict
        if isinstance(value, dict) and not isinstance(value, TrackableDict):
            value = TrackableDict(value)
        
        # Store the assignment with full path as key
        path = f"dict['{key}']"
        self.assignments[path] = value
        
        # If it's a nested TrackableDict, merge its assignments with updated paths
        if isinstance(value, TrackableDict):
            for nested_path, nested_value in value.assignments.items():
                # Update the path to include the current key
                full_nested_path = f"dict['{key}']{nested_path[4:]}"
                self.assignments[full_nested_path] = nested_value
        
        super().__setitem__(key, value)
    
    def get_assignments(self):
        return self.assignments


# Usage
t2 = TrackableDict({
    "Common": {
        "ToFile": {
            "VoltageExport": 0,
            "CurrentExport": 1
        },
        "Settings": {
            "Mode": "manual",
            "Timeout": 30
        }
    },
    "name": "John",
    "age": 31
})

# Make assignments
t2['Common']['ToFile']['VoltageExport'] = 0
t2['Common']['Settings']['Timeout'] = 30
t2['name'] = 'John'
t2['age'] = 30
t2['new_field'] = 'added'

# Get all assignments as a dictionary
assignments = t2.get_assignments()
print(assignments)


