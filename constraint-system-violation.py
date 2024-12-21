def calculate_violations(variables, constraints):
    violations = 0
    for constraint_type, *args in constraints:
        if constraint_type == "AllDifferent":
            violations += len(variables) - len(set(variables))  # Count duplicate values
        elif constraint_type == "IsEqual":
            i, j = args
            violations += abs(variables[i - 1] - variables[j - 1])  # Absolute difference
        elif constraint_type == "LessThanEqual":
            i, j = args
            violations += max(0, variables[i - 1] - variables[j - 1])  # Positive difference
    return violations

# Example usage:
N = int(input())
variables = list(map(int, input().split()))
constraints = []

while True:
    try:
        line = input()
        if line == "#":
            break

        action = line.split()
        if action[0] == "post":
            constraints.append(action[1:])  # Add constraint
        elif action[0] == "update":
            i, v = map(int, action[1:])
            variables[i - 1] = v  # Update variable value
        elif action[0] == "violations":
            violations = calculate_violations(variables, constraints)
            print(violations)  # Output violations

    except EOFError:
        break  # End of input