signals = ["CT Trafo Primary Current AVG", "CT Trafo Secondary Current AVG", "Choke RC Snubber Capacitor Current AVG", 
           "Choke RC Snubber Resistance Current AVG", "Choke RC Snubber Par Res Current AVG", "RCD Clamp Capacitor Current AVG", 
           "RCD Clamp Resistance Current AVG", "Freewheeler Blocking Cap Current AVG", "Freewheeler Resistor Current AVG", 
           "Freewheeler Impedance Cap Current AVG", "Damping Resistor Current AVG", "LV Current Sensor Current AVG", 
           "HV X-Caps 1 Current AVG", "HV X-Caps 2 Current AVG", "HV Current Sensor Current AVG", "Blocking Capacitor Current AVG",
             "Transformer Snubber Cap Current AVG", "Transformer Snubber Res Current AVG", "MOSFET RC Snubber Cap Current AVG",
               "MOSFET RC Snubber Res Current AVG", "HV Y-Caps Current AVG", "LV FullBridge Snubber Cap Current AVG",
                 "LV FullBridge Snubber Res Current AVG", "HV Snubber Caps Current AVG", "Output Ceramic Capacitors Current AVG", 
                 "Output Electrolytic Capacitors Current AVG", "Output Y-Cap Current AVG", "HV Voltage Sensor Current AVG", 
                 "HV CMC Choke Current AVG", "LV Filter X-Cap 1 Current AVG", "LV Filter X-Cap 2 Current AVG", 
                 "LV Filter Elko-Cap Current AVG", "LV Filter Y-Cap Current AVG", "LV Filter DMC Current AVG", 
                 "LV Filter CMC Current AVG", "LV Filter Output Current RbPlus AVG", "LV Filter Output Current RbMinus AVG",
                   "RCD Clamp Transistor Current AVG", "RCD Clamp Bodydiode Current AVG", "LV Rectifiers Current 1 AVG",
                     "LV Rectifiers Current 2 AVG", "DC Choke Current AVG", "Freewheeler Switch Current 1 AVG", 
                     "Freewheeler Switch Current 2 AVG", "Short Circuit Current 1 AVG", "Short Circuit Current 2 AVG", "HV Left-Leg HS Current 1 AVG", "HV Left-Leg HS Current 2 AVG", "HV Right-Leg HS Current 1 AVG", "HV Right-Leg HS Current 2 AVG", "Transformer Primary Current AVG", "Transformer Secondary Current AVG", "Transformer Magnetizing Current AVG", "HV Left-Leg ON Current AVG", "HV Left-Leg OFF Current AVG", "HV Left-Leg Max Current1 AVG", "HV Left-Leg Max Current2 AVG", "HV Right-Leg ON Current AVG", "HV Right-Leg OFF Current AVG", "HV Right-Leg Max Current1 AVG", "HV Right-Leg Max Current2 AVG", "Pack Current AVG", "Relay Current Main AVG", "Relay Current DCDC AVG", "DC Link Current AVG", "KL30 Current AVG", "ENBN DCDC Current AVG", "ENBN Battery Current AVG", "LV Filter Input Current AVG", "LV Filter Output Current AVG", "CISPR Input Current AVG", "CISPR Output Current AVG", "Load L_F Current AVG", "Load L_B Current AVG", "CTRL Current AVG", "PECU Current AVG", "Rbox Current AVG"]


import re


# Regex pattern → look for keywords in the last 2 words
pattern = re.compile(r'\b(power|loss|dissipation|current|voltage|temperature)\b', re.I)

# Map keyword to unit
unit_map = {"current":"[A]", "voltage":"[V]", "temperature":"[C]", "power":"[W]", "loss":"[W]", "dissipation":"[W]"}

# One-liner using regex
mapped_list = [unit_map[pattern.search(" ".join(s.split()[-2:])).group().lower()] if pattern.search(" ".join(s.split()[-2:])) else "[-]" for s in signals]

print(mapped_list)
