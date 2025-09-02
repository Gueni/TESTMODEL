from collections import OrderedDict, abc
from contextlib import contextmanager
import copy

class TrackableDict(OrderedDict):
    def __init__(self, *args, _parent=None, _parent_path=None, **kwargs):
        super().__init__()
        self._assignments = OrderedDict()
        self._tracking_enabled = False  # disable during init
        self._parent = _parent
        self._parent_path = _parent_path or []
        
        # Process initial data
        if args or kwargs:
            data = dict(*args, **kwargs)
            for key, value in data.items():
                self._set_item_deep(key, value, _init_mode=True)
        
        # Enable tracking after initialization
        self._tracking_enabled = True
    
    def _set_item_deep(self, key, value, _init_mode=False):
        """Recursively convert nested structures to TrackableDict"""
        if isinstance(value, abc.Mapping) and not isinstance(value, TrackableDict):
            # Convert nested dict to TrackableDict
            new_td = TrackableDict(_parent=self, _parent_path=self._parent_path + [key])
            for k, v in value.items():
                new_td._set_item_deep(k, v, _init_mode=_init_mode)
            value = new_td
        elif isinstance(value, (list, tuple)):
            # Handle sequences (convert any dicts inside sequences)
            new_seq = []
            for i, item in enumerate(value):
                if isinstance(item, abc.Mapping) and not isinstance(item, TrackableDict):
                    new_td = TrackableDict(_parent=self, _parent_path=self._parent_path + [key, f"[{i}]"])
                    for k, v in item.items():
                        new_td._set_item_deep(k, v, _init_mode=_init_mode)
                    new_seq.append(new_td)
                else:
                    new_seq.append(item)
            value = type(value)(new_seq)
        
        # Set the item without triggering tracking during init
        tracking_was_enabled = self._tracking_enabled
        if _init_mode:
            self._tracking_enabled = False
        
        super().__setitem__(key, value)
        
        if _init_mode:
            self._tracking_enabled = tracking_was_enabled
    
    def __setitem__(self, key, value):
        old_value = self.get(key, object())
        
        # Convert the value if needed
        value = self._convert_value(value, self._parent_path + [key])
        
        if old_value == value:
            super().__setitem__(key, value)
            return
        
        super().__setitem__(key, value)
        
        # Record assignment if tracking is enabled
        if self._tracking_enabled and not isinstance(value, TrackableDict):
            path_str = self._get_path_string(self._parent_path + [key])
            self._assignments[path_str] = value
    
    def _convert_value(self, value, path):
        """Convert a value to TrackableDict if it's a mapping"""
        if isinstance(value, abc.Mapping) and not isinstance(value, TrackableDict):
            new_td = TrackableDict(_parent=self, _parent_path=path)
            for k, v in value.items():
                new_td[k] = self._convert_value(v, path + [k])
            return new_td
        elif isinstance(value, (list, tuple)):
            # Handle sequences
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
        """Convert path list to string representation"""
        path_str = ""
        for p in path:
            if isinstance(p, str) and p.startswith('[') and p.endswith(']'):
                path_str += p
            else:
                path_str += f"['{p}']"
        return path_str
    
    @property
    def assignments(self):
        """Return all assignments including nested ones"""
        all_assignments = OrderedDict(self._assignments)
        
        # Recursively collect assignments from nested TrackableDicts
        for key, value in self.items():
            if isinstance(value, TrackableDict):
                nested_assignments = value.assignments
                for nested_path, nested_value in nested_assignments.items():
                    all_assignments[nested_path] = nested_value
        
        return all_assignments
    
    def clear_assignments(self):
        self._assignments.clear()
        for value in self.values():
            if isinstance(value, TrackableDict):
                value.clear_assignments()
    
    def enable_tracking(self):
        self._tracking_enabled = True
        for value in self.values():
            if isinstance(value, TrackableDict):
                value.enable_tracking()
    
    def disable_tracking(self):
        self._tracking_enabled = False
        for value in self.values():
            if isinstance(value, TrackableDict):
                value.disable_tracking()
    
    @contextmanager
    def track_scope(self):
        """Track only assignments made within the context"""
        original_assignments = self.assignments.copy()  # Copy current assignments
        self.clear_assignments()  # Clear assignments for the scope
        self.enable_tracking()  # Enable tracking
        try:
            yield self
        finally:
            # Merge new assignments with original ones
            current_assignments = self.assignments  # Get assignments made in the scope
            self.clear_assignments()  # Clear again to avoid duplicates
            self._assignments.update(original_assignments)  # Restore original assignments
            self._assignments.update(current_assignments)  # Add new assignments




from collections import OrderedDict

nested_od = OrderedDict({
    'Common': OrderedDict({
        'ToFile': OrderedDict({'VoltageExport': 0, 'CurrentExport': 1}),
        'Settings': OrderedDict({'Mode': 'manual', 'Timeout': 30})
    }),
    'name': 'John',
    'age': 31
})



# Usage with your ModelVars
def create_trackable_model_vars():
    """Convert your ModelVars to a TrackableDict"""
    # First make a deep copy to avoid modifying the original
    model_vars_copy = copy.deepcopy(nested_od)
    return TrackableDict(model_vars_copy)

# Test it
trackable_model = create_trackable_model_vars()

with trackable_model.track_scope():
    trackable_model['Common']['Settings'] =363636

print("Assignments:", trackable_model.assignments)