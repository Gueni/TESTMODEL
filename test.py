filter_non_xi = lambda lst: [s for s in lst if not (s.startswith('X') and s[1:].isdigit())]


print(filter_non_xi(['hello', 'X1', 'world', 'X22', 'test', 'X', 'X123']))

