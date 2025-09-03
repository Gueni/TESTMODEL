from collections import OrderedDict, abc
from contextlib import contextmanager
import copy

class TrackableDict(OrderedDict):
    """
    A dictionary that tracks assignments to its values, including nested dictionaries.
    
    This class extends OrderedDict to provide tracking functionality that records
    all value assignments, even in nested structures. It's useful for monitoring
    changes to configuration objects or tracking modifications to complex data structures.
    
    Features:
    - Tracks assignments at any nesting level
    - Supports scope-based tracking with context manager
    - Converts nested dictionaries to TrackableDict automatically
    - Maintains order of assignments
    - Provides clean serializable output of changes
    
    Attributes:
        _assignments (OrderedDict): Stores tracked assignments with full path as key
        _tracking_enabled (bool): Controls whether assignments are currently being tracked
        _parent (TrackableDict): Reference to parent dictionary (for nested structures)
        _parent_path (list): Path from root to this dictionary
    """
    
    def __init__(self, *args, _parent=None, _parent_path=None, **kwargs):
        """
        Initialize a TrackableDict.
        
        Args:
            *args: Positional arguments passed to dict constructor
            _parent (TrackableDict, optional): Parent dictionary for nested structures
            _parent_path (list, optional): Path from root to this dictionary
            **kwargs: Keyword arguments passed to dict constructor
        """
        super().__init__()
        self._assignments = OrderedDict()  # Stores tracked assignments: {path: value}
        self._tracking_enabled = False  # Disable tracking during initialization
        self._parent = _parent  # Reference to parent dictionary
        self._parent_path = _parent_path or []  # Path from root to this node
        
        # Process initial data if provided
        if args or kwargs:
            data = dict(*args, **kwargs)
            for key, value in data.items():
                self._set_item_deep(key, value, _init_mode=True)
        
        # Enable tracking after initialization is complete
        self._tracking_enabled = True
    
    def _set_item_deep(self, key, value, _init_mode=False):
        """
        Recursively convert nested structures to TrackableDict during initialization.
        
        This method ensures that all nested dictionaries become TrackableDict instances
        so they can also participate in the tracking system.
        
        Args:
            key: The key where the value will be stored
            value: The value to be stored (may be converted if it's a mapping)
            _init_mode (bool): Whether we're in initialization mode
        """
        # Convert regular mappings to TrackableDict
        if isinstance(value, abc.Mapping) and not isinstance(value, TrackableDict):
            # Create new TrackableDict with proper parent reference and path
            new_td = TrackableDict(_parent=self, _parent_path=self._parent_path + [key])
            for k, v in value.items():
                new_td._set_item_deep(k, v, _init_mode=_init_mode)
            value = new_td
        # Handle sequences (lists, tuples) that might contain mappings
        elif isinstance(value, (list, tuple)):
            new_seq = []
            for i, item in enumerate(value):
                if isinstance(item, abc.Mapping) and not isinstance(item, TrackableDict):
                    # Convert dictionaries within sequences to TrackableDict
                    new_td = TrackableDict(_parent=self, _parent_path=self._parent_path + [key, f"[{i}]"])
                    for k, v in item.items():
                        new_td._set_item_deep(k, v, _init_mode=_init_mode)
                    new_seq.append(new_td)
                else:
                    new_seq.append(item)
            value = type(value)(new_seq)
        
        # Temporarily disable tracking to avoid recording initial values as assignments
        tracking_was_enabled = self._tracking_enabled
        if _init_mode:
            self._tracking_enabled = False
        
        # Store the value (which might now be a TrackableDict)
        super().__setitem__(key, value)
        
        # Restore tracking state
        if _init_mode:
            self._tracking_enabled = tracking_was_enabled
    
    def __setitem__(self, key, value):
        """
        Set an item in the dictionary and track the assignment if enabled.
        
        This method overrides the standard dictionary assignment to:
        1. Convert nested structures to TrackableDict if needed
        2. Record the assignment in the tracking system
        3. Maintain the parent-child relationship for nested dictionaries
        
        Args:
            key: The key to set
            value: The value to assign
        """
        # Convert the value to TrackableDict if it's a mapping
        value = self._convert_value(value, self._parent_path + [key])
        
        # Always set the item (even if values are equal - we track all assignments)
        super().__setitem__(key, value)
        
        # Record assignment if tracking is enabled and it's not a TrackableDict
        # (TrackableDict values track their own assignments internally)
        if self._tracking_enabled and not isinstance(value, TrackableDict):
            path_str = self._get_path_string(self._parent_path + [key])
            self._assignments[path_str] = value
    
    def _convert_value(self, value, path):
        """
        Convert a value to TrackableDict if it's a mapping, preserving structure.
        
        This is used during assignment to ensure nested dictionaries become trackable.
        
        Args:
            value: The value to potentially convert
            path: The path to this value from the root
            
        Returns:
            The original value or a converted TrackableDict
        """
        if isinstance(value, abc.Mapping) and not isinstance(value, TrackableDict):
            # Convert regular dict to TrackableDict with proper parent reference
            new_td = TrackableDict(_parent=self, _parent_path=path)
            for k, v in value.items():
                new_td[k] = self._convert_value(v, path + [k])
            return new_td
        elif isinstance(value, (list, tuple)):
            # Handle sequences that might contain dictionaries
            new_seq = []
            for i, item in enumerate(value):
                if isinstance(item, abc.Mapping) and not isinstance(item, TrackableDict):
                    new_td = TrackableDict(_parent=self, _parent_path=path + [f"[{i}]"])
                    for k, v in item.items():
                        new_td[k] = self._convert_value(v, path + [f"[{i}]", k])
                    new_seq.append(new_td)
                else:
                    new_seq.append(item)
            return type(value)(new_seq)
        return value
    
    def _get_path_string(self, path):
        """
        Convert a path list to a string representation for assignment tracking.
        
        Example: ['Common', 'Settings', 'Mode', 'CurrentExport'] becomes 
        "['Common']['Settings']['Mode']['CurrentExport']"
        
        Args:
            path: List of path components
            
        Returns:
            String representation of the path
        """
        path_str = ""
        for p in path:
            if isinstance(p, str) and p.startswith('[') and p.endswith(']'):
                # Already formatted as array index (e.g., "[0]")
                path_str += p
            else:
                # Format as dictionary key
                path_str += f"['{p}']"
        return path_str
    
    @property
    def assignments(self):
        """
        Property that returns all tracked assignments including nested ones.
        
        The @property decorator makes this method accessible as an attribute
        without parentheses: trackable_model.assignments instead of 
        trackable_model.assignments()
        
        Returns:
            OrderedDict: All assignments with full paths as keys and values
        """
        # Start with current level assignments
        all_assignments = OrderedDict(self._assignments)
        
        # Recursively collect assignments from nested TrackableDicts
        for key, value in self.items():
            if isinstance(value, TrackableDict):
                nested_assignments = value.assignments
                for nested_path, nested_value in nested_assignments.items():
                    # Ensure values are basic types (not TrackableDict instances)
                    if isinstance(nested_value, TrackableDict):
                        nested_value = dict(nested_value)
                    all_assignments[nested_path] = nested_value
        
        # Convert any remaining TrackableDict values to regular dicts
        for path, value in all_assignments.items():
            if isinstance(value, TrackableDict):
                all_assignments[path] = dict(value)
        
        return all_assignments
    
    def clear_assignments(self):
        """Clear all tracked assignments from this dictionary and nested dictionaries."""
        self._assignments.clear()
        for value in self.values():
            if isinstance(value, TrackableDict):
                value.clear_assignments()
    
    def enable_tracking(self):
        """Enable assignment tracking for this dictionary and nested dictionaries."""
        self._tracking_enabled = True
        for value in self.values():
            if isinstance(value, TrackableDict):
                value.enable_tracking()
    
    def disable_tracking(self):
        """Disable assignment tracking for this dictionary and nested dictionaries."""
        self._tracking_enabled = False
        for value in self.values():
            if isinstance(value, TrackableDict):
                value.disable_tracking()
    
    @contextmanager
    def track_scope(self):
        """
        Context manager for scoped assignment tracking.
        
        The @contextmanager decorator allows this method to be used with
        the 'with' statement. It creates a scope where only assignments
        made within that scope are tracked.
        
        Usage:
            with trackable_model.track_scope():
                trackable_model['key'] = value  # This assignment will be tracked
                
        Yields:
            self: The TrackableDict instance
        """
        # Store current state before entering the scope
        original_assignments = copy.deepcopy(self._assignments)
        original_tracking_state = self._tracking_enabled
        
        # Prepare for scoped tracking
        self.clear_assignments()  # Clear previous assignments
        self.enable_tracking()    # Ensure tracking is enabled
        
        try:
            # Yield control to the code inside the 'with' block
            yield self
        finally:
            # This block executes when exiting the 'with' block
            # Get assignments made during the scope
            scope_assignments = copy.deepcopy(self.assignments)
            
            # Restore original state
            self.disable_tracking()
            self._assignments = original_assignments
            self._tracking_enabled = original_tracking_state
            
            # Merge scope assignments with original ones
            self._assignments.update(scope_assignments)


# Example usage and demonstration
from collections import OrderedDict

nested_od = OrderedDict({
    'Common': OrderedDict({
        'ToFile': OrderedDict({'VoltageExport': 0, 'CurrentExport': 1}),
        'Settings': OrderedDict({'Mode': OrderedDict({'VoltageExport': 0, 'CurrentExport': 1}), 'Timeout': 30})
    }),
    'name': 'John',
    'age': 31
})

def create_trackable_model_vars(dictt):
    """
    Convert a regular dictionary to a TrackableDict.
    
    Args:
        dictt: Regular dictionary to convert
        
    Returns:
        TrackableDict: Trackable version of the input dictionary
    """
    # Deep copy to avoid modifying the original dictionary
    model_vars_copy = copy.deepcopy(dictt)
    return TrackableDict(model_vars_copy)

# Demonstration
if __name__ == "__main__":
    trackable_model = create_trackable_model_vars(nested_od)

    for i in range(4):
        with trackable_model.track_scope():
            trackable_model['Common']['Settings']['Mode']['CurrentExport'] = 1 + i

        print("Assignments:", trackable_model.assignments)



# How the Tracking System Works
# Initialization: When a TrackableDict is created, it converts all nested dictionaries to TrackableDict instances

# Assignment Tracking: When a value is assigned, if tracking is enabled and the value isn't a TrackableDict, the assignment is recorded with its full path

# Nested Tracking: Each TrackableDict tracks its own assignments and recursively collects assignments from its children

# Scope Management: The track_scope() context manager isolates assignments made within a specific block of code

# Serialization: The assignments property returns a clean dictionary with basic data types that can be easily serialized and used elsewhere

