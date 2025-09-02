from collections import OrderedDict, abc
from contextlib import contextmanager

class TrackableDict(OrderedDict):
    def __init__(self, *args, _parent=None, _parent_path=None, _init_mode=True, **kwargs):
        super().__init__()
        self._assignments = OrderedDict()
        self._tracking_enabled = False  # always disable tracking during init
        self._parent = _parent
        self._parent_path = _parent_path or []

        # recursively convert all nested mappings without tracking
        data = dict(*args, **kwargs)
        for key, value in data.items():
            super().__setitem__(key, self._deep_convert(value, path=self._parent_path + [key], _init_mode=True))

        # initialization done, enable tracking
        self._tracking_enabled = True

    def _deep_convert(self, obj, path, _init_mode=False):
        if isinstance(obj, abc.Mapping) and not isinstance(obj, TrackableDict):
            td = TrackableDict(_parent=self, _parent_path=path, _init_mode=True)
            for k, v in obj.items():
                td[k] = self._deep_convert(v, path + [k], _init_mode=True)
            td._tracking_enabled = False  # disable tracking for children during init
            return td
        return obj

    def __setitem__(self, key, value):
        value = self._deep_convert(value, path=self._parent_path + [key])
        old_value = self.get(key, object())
        if old_value == value:
            super().__setitem__(key, value)
            return

        super().__setitem__(key, value)

        # record assignment only if tracking enabled
        if self._tracking_enabled and not isinstance(value, TrackableDict):
            path_str = ''.join(f"['{p}']" for p in self._parent_path + [key])
            self._assignments[path_str] = value

    @property
    def assignments(self):
        """Return only the assignments made directly to this dict."""
        return OrderedDict(self._assignments)

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
        """Track only assignments made within the context."""
        original = self.assignments.copy()
        self.clear_assignments()
        self.enable_tracking()
        try:
            yield self
        finally:
            scope_assignments = self.assignments
            self._assignments = OrderedDict(original)
            self._assignments.update(scope_assignments)





from collections import OrderedDict

nested_od = OrderedDict({
    'Common': OrderedDict({
        'ToFile': OrderedDict({'VoltageExport': 0, 'CurrentExport': 1}),
        'Settings': OrderedDict({'Mode': 'manual', 'Timeout': 30})
    }),
    'name': 'John',
    'age': 31
})

t2 = TrackableDict(nested_od)

with t2.track_scope():
    t2['name'] = 'Alice'
    t2['new_field'] = 'added0'

print(t2.assignments)
