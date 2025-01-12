from ortools.linear_solver import pywraplp

def solve_broadcast():
    # Input
    n, m, s, L = map(int, input().split())
    edges = []
    graph = [[] for _ in range(n+1)]
    
    for _ in range(m):
        u, v, t, c = map(int, input().split())
        edges.append((u, v, t, c))
        graph[u].append((v, t, c))
        graph[v].append((u, t, c))
    
    # Create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Variables
    x = [solver.BoolVar(f'x_{i}') for i in range(m)]
    delay = [solver.IntVar(0, L, f'd_{i}') for i in range(n+1)]
    
    # Tree constraints
    # Must use exactly n-1 edges
    solver.Add(sum(x) == n-1)
    
    # Connectivity: each non-source node must have incoming edge
    for v in range(1, n+1):
        if v != s:
            incoming = []
            for i, (u, end, _, _) in enumerate(edges):
                if end == v or u == v:
                    incoming.append(x[i])
            solver.Add(sum(incoming) >= 1)
    
    # Delay propagation
    solver.Add(delay[s] == 0)  # Source delay
    M = L + 1  # Big-M constant
    for i, (u, v, t, _) in enumerate(edges):
        # If edge used, enforce delay constraints
        solver.Add(delay[v] >= delay[u] + t - M * (1 - x[i]))
        solver.Add(delay[u] >= delay[v] + t - M * (1 - x[i]))
        solver.Add(delay[v] <= L)
        solver.Add(delay[u] <= L)
    
    # Objective
    objective = solver.Objective()
    for i, (_, _, _, c) in enumerate(edges):
        objective.SetCoefficient(x[i], c)
    objective.SetMinimization()
    
    # Solve
    solver.SetTimeLimit(300000)  # 5 minutes
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print(int(solver.Objective().Value()))
    else:
        print("NO_SOLUTION")

if __name__ == "__main__":
    solve_broadcast()