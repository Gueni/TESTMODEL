import xmlrpc.client  # For connecting to PLECS RPC server
import os             # For file path manipulations
import json           # For decoding JSON from RPC Binary objects




import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:1080")

# List all available methods (correct way)
print("Available methods:")
methods = proxy.system.listMethods()
for method in methods:
    print(f"  {method}")

#   plecs.simulate
#   plecs.scope
#   system.listMethods
#   plecs.load
#   system.methodHelp
#!   plecs.webserver
#!   plecs.getModelTree
#!   plecs.codegen
#   plecs.close
#   plecs.analyze
#   plecs.get
#!   plecs.statistics
#   plecs.set


def get_scopes(proxy, model_path):
    """
    Load a PLECS model via XML-RPC and return all scope paths in the model.

    Parameters:
        proxy (xmlrpc.client.ServerProxy): The connected PLECS RPC server proxy
        model_path (str): Absolute path to the .plecs model file

    Returns:
        list of str: Full paths of all scopes in the model
    """
    # --------------------------
    # Step 1: Load the model file
    # --------------------------
    proxy.plecs.load(model_path)  # Load the .plecs model into the PLECS session

    # --------------------------
    # Step 2: Compute model handle
    # --------------------------
    # PLECS expects the absolute path without the '.plecs' extension as the handle
    model_handle = os.path.splitext(model_path)[0]
    # --------------------------
    # Step 3: Retrieve model tree
    # --------------------------
    tree = proxy.plecs.getModelTree(model_handle)  # Get hierarchical structure of the model

    # --------------------------
    # Step 4: Decode Binary objects
    # --------------------------
    if isinstance(tree, xmlrpc.client.Binary):
        # If the returned tree is a Binary object, decode as UTF-8 and parse JSON
        tree = json.loads(tree.data.decode('utf-8'))

    # --------------------------
    # Step 5: Prepare storage for scopes
    # --------------------------
    scopes = []  # List to store the full paths of all scopes

    # --------------------------
    # Step 6: Recursive scan function
    # --------------------------
    def scan(node, path=""):
        """
        Recursively traverse the model tree to find all scopes.

        Parameters:
            node (dict or list): Current node in the model tree
            path (str): Accumulated path of parent blocks
        """
        if isinstance(node, dict):  # If node is a dictionary (block or property)
            name = node.get("name", "")  # Get block name, default empty string
            kind = node.get("kind", "")  # Get kind of element, e.g., 'circuit', 'scope'

            # Build full path by appending current node name
            current_path = f"{path}/{name}" if path else name
            # If node represents a scope, add it to the scopes list
            if kind.lower() == "scope" or node.get("type") == "Scope":
                scopes.append(current_path)

            # Recursively scan all children nodes
            for child in node.get("children", []):
                scan(child, current_path)

        elif isinstance(node, list):  # If node is a list of nodes
            for item in node:
                scan(item, path)  # Recursively scan each item

    # --------------------------
    # Step 7: Start scanning from the root of the tree
    # --------------------------
    scan([tree] if isinstance(tree, dict) else tree)  # Wrap dict in list if needed

    # --------------------------
    # Step 8: Return collected scopes
    # --------------------------
    return scopes  # Return list of full scope paths


# --------------------------
# Example usage
# --------------------------
if __name__ == "__main__":
    proxy = xmlrpc.client.ServerProxy("http://localhost:1080")  # Connect to PLECS RPC server
    model_path = r"D:/WORKSPACE/TESTMODEL/ACfilterOBC.plecs"  # Path to your model file

    # Call the function to retrieve all scopes
    scopes = get_scopes(proxy, model_path)

    # Print the found scopes
    print("Scopes found:", scopes)