
# This code flattens a list of lists into a single list using the sum function.
# x = [[1], [2], [3], [4], [5]]
# x2 = sum(x, [])
# print(x2)  # [1, 2, 3, 4, 5]

# # This code creates a list of lists using a list comprehension.
# x = [[i] for i in range(0, 10)]
# print(x)  # [[1], [2], [3], [4], [5]]


# # Returns "WCA" if any inner list has length > 1
# # Otherwise returns "Normal" if any inner list has length 1 and value != 0
# # Otherwise returns "Unknown"
# x = [[1], [2], [3]]           # -> "Normal"
# # x = [[1, 2], [3], [4]]        # -> "WCA" (has inner list with len > 1)
# result = "WCA" if any(len(inner) > 1 for inner in x) else "Normal" if any(len(inner) == 1  for inner in x) else "Unknown"
# print(result)
# if result == "WCA":
#     print("Has inner list with length > 1")
# elif result == "Normal":
#     print("Has inner list with length == 1")
#     # This code creates a list of lists using a list comprehension.
#     x = sum(x, [])
# print('x =' ,x)  # [[1], [2], [3], [4], [5]]




import json
import math

def binary_index(iteration, index):
    """
    Calculate the binary index for a given iteration and index.
    """
    bin_idx = math.floor(iteration / (2 ** index)) - 2 * math.floor(iteration / (2 ** (index + 1)))
    return bin_idx

def WCA(iteration, Xs):
    """
    Perform Worst Case Analysis on all variables.
    
    Args:
        iteration (int): The current iteration number
        Xs (list): List of lists containing variable data in format:
                 [[[nom, tol, min, max], [nom, tol, min, max], ...],  # X1
                  [[nom, tol, min, max], ...],                        # X2
                  ...]
    
    Returns:
        list: List with WCA values for each variable in format [value_after_tolerance, min, max]
    """
    def funtol(Abs_rel, iteration, index, nom, tol):
        if Abs_rel:
            if binary_index(iteration, index):
                return nom * tol
            else:
                return nom / tol
        else:
            if binary_index(iteration, index):
                return nom * (1 + tol)
            else:
                return nom * (1 - tol)
    
    results = []
    
    for i, var_data in enumerate(Xs):
        # Skip variables that are not used (have [[0]])
        if var_data == [[0]]:
            results.append([0, 0, 0])  # Keep as list for consistency
            continue
            
        # Calculate WCA for each value-tolerance-min-max tuple in the variable
        wca_values = []
        for j, (nom, tol, min_val, max_val) in enumerate(var_data):
            wca_value = funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol)
            # Apply min and max constraints
            min_value = min(funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol), min_val)
            max_value = max(funtol(Abs_rel=True, iteration=iteration, index=i, nom=nom, tol=tol), max_val)
            wca_values.append([wca_value, min_value, max_value])
        
        results.append(wca_values)
    
    return results

def load_variables_from_json(filename):
    """Load variables from JSON and return as list of lists"""
    with open(filename, 'r') as f:
        variables_data = json.load(f)
    
    variable_names = []
    Xs = []
    
    i = 1
    while f"X{i}" in variables_data:
        var_name = f"X{i}"
        value = variables_data[var_name]
        variable_names.append(var_name)
        if value != "[[0]]":
            Xs.append(eval(value))
        else:
            Xs.append([[0]])
        i += 1
    
    return variable_names, Xs


# Load variables
variable_names, Xs = load_variables_from_json('Input_vars.json')

print("Loaded variables:")
for name, data in zip(variable_names, Xs):
    print(f"  {name}: {data}")

print("\nWCA Results for each iteration (format: [value_after_tolerance, min, max]):")
for iteration in range(10):
    results = WCA(iteration, Xs)
    print(f"\nIteration {iteration}:")
    for name, result in zip(variable_names, results):
        print(f"  {name}: {result}")
    
print("matrix   = " ,results   )

# matrix = [X1_WCA, X2_WCA, X3_WCA, X4_WCA, X5_WCA, X6_WCA, X7_WCA, X8_WCA, X9_WCA, X10_WCA]
# matrix   =  [
#                 [[1.0, 1.0, 15], [4.0, 4.0, 25]], 
#                 [[200.0, 50, 200.0], [400.0, 150, 400.0]], 
#                 [[25.0, 3, 25.0], [50.0, 10, 50.0]], 
#                 [[5.0, 5.0, 60], [30.0, 30.0, 200]], 
#                 [[2.0, 0.5, 2.0], [4.0, 1, 4.0]], 
#                 [[32.0, 6, 32.0], [48.0, 10, 48.0]], 
#                 [0, 0, 0], 
#                 [0, 0, 0], 
#                 [0, 0, 0],
#                 [0, 0, 0]
#             ]