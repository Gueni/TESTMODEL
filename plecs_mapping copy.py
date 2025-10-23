import json
from pathlib import Path

fix_json_strings = lambda folder: [f.write_text(json.dumps([s.replace(" ", "_").replace("-", "_") for s in json.loads(f.read_text())], indent=2)) for f in Path(folder).glob("*.json")]

fix_json_strings(r"D:\WORKSPACE\TESTMODEL\SIGNAL_MAPPING\DCDC_DUAL")


