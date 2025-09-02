from collections import OrderedDict
from contextlib import contextmanager

class TrackableDict(OrderedDict):
    def __init__(self, *args, _parent=None, _parent_path=None, **kwargs):
        super().__init__()
        self._assignments = OrderedDict()
        self._tracking_enabled = True
        self._parent = _parent
        self._parent_path = _parent_path or []
        
        data = dict(*args, **kwargs)
        for key, value in data.items():
            if isinstance(value, dict) and not isinstance(value, TrackableDict):
                value = TrackableDict(value, _parent=self, _parent_path=self._parent_path + [key])
                value._tracking_enabled = self._tracking_enabled
            super().__setitem__(key, value)
    
    def __setitem__(self, key, value):
        if isinstance(value, dict) and not isinstance(value, TrackableDict):
            value = TrackableDict(value, _parent=self, _parent_path=self._parent_path + [key])
            value._tracking_enabled = self._tracking_enabled
        
        super().__setitem__(key, value)
        
        if self._tracking_enabled:
            self._track_assignment(key, value)
            if self._parent is not None:
                self._parent._track_assignment(self._parent_path[-1] if self._parent_path else key, self)
    
    def _track_assignment(self, key, value, path=None):
        if path is None:
            path = self._parent_path.copy()
        current_path = path + [key]
        
        # Only track leaf values
        if not isinstance(value, TrackableDict):
            # Convert path to "['key1']['key2']" format
            path_str = ''.join(f"['{p}']" for p in current_path)
            self._assignments[path_str] = value
    
    @property
    def assignments(self):
        result = OrderedDict(self._assignments)
        # Merge nested assignments
        for value in self.values():
            if isinstance(value, TrackableDict):
                result.update(value.assignments)
        return result

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
        original = self.assignments.copy()
        self.clear_assignments()
        self.enable_tracking()
        try:
            yield self
        finally:
            scope_assignments = self.assignments
            self._assignments = OrderedDict(original)
            self._assignments.update(scope_assignments)




t2 = TrackableDict({
    "Common": {
        "ToFile": {"VoltageExport": 0, "CurrentExport": 1},
        "Settings": {"Mode": "manual", "Timeout": 30}
    },
    "name": "John",
    "age": 31
})

with t2.track_scope():
    t2['Common']['ToFile']['VoltageExport'] = 5
    t2['Common']['Settings']['Timeout'] = 60
    t2['name'] = 'Alice'
    t2['new_field'] = 'added0'

print(t2.assignments)



