from ortools.linear_solver import pywraplp

def solve():
    # Read input
    m, n = map(int, input().split())
    preferences = {}
    for i in range(1, m+1):
        prefs = list(map(int, input().split()))
        preferences[i] = prefs[1:]
    
    k = int(input())
    conflicts = set()
    for _ in range(k):
        c1, c2 = map(int, input().split())
        conflicts.add((c1, c2))
        conflicts.add((c2, c1))
    
    # Create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Variables
    # x[t,c] = 1 if teacher t teaches course c
    x = {}
    for t in range(1, m+1):
        for c in range(1, n+1):
            x[t,c] = solver.BoolVar(f'x_{t}_{c}')
    
    # Load variables
    load = {}
    for t in range(1, m+1):
        load[t] = solver.IntVar(0, n, f'load_{t}')
    
    max_load = solver.IntVar(0, n, 'max_load')
    
    # Constraints
    # Each course assigned to one teacher
    for c in range(1, n+1):
        solver.Add(sum(x[t,c] for t in range(1, m+1)) == 1)
    
    # Preferences
    for c in range(1, n+1):
        for t in range(1, m+1):
            if c not in preferences[t]:
                solver.Add(x[t,c] == 0)
    
    # Conflicts
    for c1, c2 in conflicts:
        for t in range(1, m+1):
            solver.Add(x[t,c1] + x[t,c2] <= 1)
    
    # Load calculation
    for t in range(1, m+1):
        solver.Add(load[t] == sum(x[t,c] for c in range(1, n+1)))
        solver.Add(max_load >= load[t])
    
    # Objective
    solver.Minimize(max_load)
    
    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print(int(max_load.solution_value()))
    else:
        print(-1)

if __name__ == "__main__":
    solve()