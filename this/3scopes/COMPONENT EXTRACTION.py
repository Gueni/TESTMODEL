import xmlrpc.client
import json
from datetime import datetime

# ==============================
# CONFIGURATION
# ==============================

PLECS_SERVER = "http://localhost:1080/RPC2"

MODEL_CURRENT = "D:\WORKSPACE\OBC\OBC\PLECS SIMULATION\Model\Buck_converter.plecs"
MODEL_PREVIOUS = "D:\WORKSPACE\OBC\OBC\PLECS SIMULATION\Model\Buck_converterV2.plecs"

IGNORE_GRAPHICS = True

OUTPUT_DOC = "model_documentation.txt"
OUTPUT_DIFF = "model_change_report.txt"


# ==============================
# CONNECT TO PLECS
# ==============================

plecs = xmlrpc.client.ServerProxy(PLECS_SERVER)


# ==============================
# TREE UTILITIES
# ==============================

def walk(node):

    yield node

    for c in node.get("children", []):
        yield from walk(c)


# ==============================
# COMPONENT EXTRACTION
# ==============================

def extract_components(tree):

    comps = {}

    for n in walk(tree):

        if n.get("kind") == "component":

            name = n["name"]
            comps[name] = {
                "type": n.get("type"),
                "parameters": {},
                "properties": {}
            }

            for c in n.get("children", []):

                if c.get("kind") == "parameter":

                    pname = c["name"]
                    val = c["children"][0]["value"]

                    comps[name]["parameters"][pname] = val

                if c.get("kind") == "property":

                    pname = c["name"]
                    val = c["children"][0]["value"]

                    comps[name]["properties"][pname] = val

    return comps


# ==============================
# SIMULATION PARAMETERS
# ==============================

def extract_simulation(tree):

    sim = {}

    for n in tree.get("children", []):

        if n.get("kind") == "parameter":

            name = n["name"]
            val = n["children"][0]["value"]

            sim[name] = val

    return sim


# ==============================
# DOCUMENTATION GENERATOR
# ==============================

def generate_documentation(model):

    tree = plecs.plecs.getModelTree(model)

    comps = extract_components(tree)
    sim = extract_simulation(tree)

    doc = []
    doc.append("PLECS MODEL DOCUMENTATION")
    doc.append("=========================")
    doc.append("")
    doc.append(f"Model: {model}")
    doc.append(f"Generated: {datetime.now()}")
    doc.append("")

    doc.append("COMPONENTS")
    doc.append("----------")

    for name,data in comps.items():

        doc.append(f"{name} : {data['type']}")

        for p,v in data["parameters"].items():
            doc.append(f"   {p} = {v}")

    doc.append("")
    doc.append("SIMULATION SETTINGS")
    doc.append("-------------------")

    for k,v in sim.items():
        doc.append(f"{k} = {v}")

    return "\n".join(doc)


# ==============================
# MODEL COMPARISON
# ==============================

def compare_models(model1, model2):

    tree1 = plecs.plecs.getModelTree(model1)
    tree2 = plecs.plecs.getModelTree(model2)

    comp1 = extract_components(tree1)
    comp2 = extract_components(tree2)

    names1 = set(comp1.keys())
    names2 = set(comp2.keys())

    added = names2 - names1
    removed = names1 - names2
    common = names1 & names2

    report = []

    report.append("PLECS MODEL CHANGE REPORT")
    report.append("=========================")
    report.append("")
    report.append(f"Base model : {model1}")
    report.append(f"New model  : {model2}")
    report.append(f"Generated  : {datetime.now()}")
    report.append("")

    # -----------------
    # ADDED COMPONENTS
    # -----------------

    report.append("ADDED COMPONENTS")
    report.append("----------------")

    if added:
        for c in added:
            report.append(f"+ {c} ({comp2[c]['type']})")
    else:
        report.append("None")

    report.append("")

    # -----------------
    # REMOVED COMPONENTS
    # -----------------

    report.append("REMOVED COMPONENTS")
    report.append("------------------")

    if removed:
        for c in removed:
            report.append(f"- {c} ({comp1[c]['type']})")
    else:
        report.append("None")

    report.append("")

    # -----------------
    # PARAMETER CHANGES
    # -----------------

    report.append("MODIFIED PARAMETERS")
    report.append("-------------------")

    changes_found = False

    for c in common:

        p1 = comp1[c]["parameters"]
        p2 = comp2[c]["parameters"]

        for param,val1 in p1.items():

            val2 = p2.get(param)

            if val2 and val1 != val2:

                changes_found = True

                report.append(
                    f"{c}.{param}: {val1}  →  {val2}"
                )

    if not changes_found:
        report.append("None")

    report.append("")

    # -----------------
    # PROPERTY CHANGES
    # -----------------

    if not IGNORE_GRAPHICS:

        report.append("PROPERTY CHANGES")
        report.append("----------------")

        prop_changes = False

        for c in common:

            pr1 = comp1[c]["properties"]
            pr2 = comp2[c]["properties"]

            for p,val1 in pr1.items():

                val2 = pr2.get(p)

                if val2 and val1 != val2:

                    prop_changes = True

                    report.append(
                        f"{c}.{p}: {val1} → {val2}"
                    )

        if not prop_changes:
            report.append("None")

    return "\n".join(report)


# ==============================
# MAIN EXECUTION
# ==============================

print("Generating documentation...")

doc = generate_documentation(MODEL_CURRENT)

with open(OUTPUT_DOC,"w") as f:
    f.write(doc)

print("Documentation saved:", OUTPUT_DOC)


print("Generating model comparison...")

diff = compare_models(MODEL_PREVIOUS, MODEL_CURRENT)

with open(OUTPUT_DIFF,"w") as f:
    f.write(diff)

print("Change report saved:", OUTPUT_DIFF)