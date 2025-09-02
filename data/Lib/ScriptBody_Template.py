class TrackableDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignments = {}
        self._tracking_enabled = True
        # Convert all nested dictionaries to TrackableDict during initialization
        self._convert_nested_dicts()
    
    def _convert_nested_dicts(self):
        """Convert all nested dictionaries to TrackableDict"""
        for key, value in list(self.items()):
            if isinstance(value, dict) and not isinstance(value, TrackableDict):
                trackable_value = TrackableDict(value)
                super().__setitem__(key, trackable_value)
                # Record this initial assignment
                if self._tracking_enabled:
                    path = f"dict['{key}']"
                    self.assignments[path] = trackable_value
    
    def __setitem__(self, key, value):
        # Handle nested dictionaries - convert them to TrackableDict
        if isinstance(value, dict) and not isinstance(value, TrackableDict):
            value = TrackableDict(value)
            value._tracking_enabled = self._tracking_enabled
        
        # Store the assignment with full path as key (only if tracking is enabled)
        if self._tracking_enabled:
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
    
    def clear_assignments(self):
        """Clear all tracked assignments"""
        self.assignments.clear()
    
    def enable_tracking(self):
        """Enable assignment tracking"""
        self._tracking_enabled = True
    
    def disable_tracking(self):
        """Disable assignment tracking"""
        self._tracking_enabled = False
    
    def track_scope(self):
        """Context manager for tracking assignments within a scope"""
        return TrackingScope(self)

class TrackingScope:
    def __init__(self, trackable_dict):
        self.trackable_dict = trackable_dict
        self.original_assignments = trackable_dict.assignments.copy()
    
    def __enter__(self):
        self.trackable_dict.enable_tracking()
        self.trackable_dict.clear_assignments()
        return self.trackable_dict
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Keep only the assignments made during this scope
        scope_assignments = self.trackable_dict.assignments.copy()
        self.trackable_dict.assignments = self.original_assignments
        self.trackable_dict.assignments.update(scope_assignments)
        return False

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

def my_function():
    # Use the context manager to track assignments only within this function
    with t2.track_scope():
        # Make assignments - only these will be tracked
        t2['Common']['ToFile']['VoltageExport'] = 0
        t2['Common']['Settings']['Timeout'] = 30
        t2['name'] = 'John'
        t2['age'] = 30
        t2['new_field'] = 'added'
    
    # Get assignments made during the function scope
    return t2.get_assignments()

# Call the function
function_assignments = my_function()
print("Assignments made inside the function:")
print(function_assignments)
