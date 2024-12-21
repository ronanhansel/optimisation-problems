from ortools.sat.python import cp_model

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
    
    # Model
    model = cp_model.CpModel()
    
       # Variables
    x = [model.NewBoolVar(f'x_{i}') for i in range(m)]
    delay = [model.NewIntVar(0, L, f'd_{i}') for i in range(n+1)]
    
    # Tree constraints
    # Must use exactly n-1 edges
    model.Add(sum(x) == n-1)
    
    # Connectivity: each non-source node must have incoming edge
    for v in range(1, n+1):
        if v != s:
            incoming = []
            for i, (u, end, _, _) in enumerate(edges):
                if end == v:
                    incoming.append(x[i])
                elif u == v:
                    incoming.append(x[i])
            model.Add(sum(incoming) >= 1)
    
    # Delay propagation
    model.Add(delay[s] == 0)  # Source delay
    for i, (u, v, t, _) in enumerate(edges):
        # If edge used, enforce delay constraint both ways
        model.Add(delay[v] >= delay[u] + t).OnlyEnforceIf(x[i])
        model.Add(delay[u] >= delay[v] + t).OnlyEnforceIf(x[i])
        model.Add(delay[v] <= L).OnlyEnforceIf(x[i])
        model.Add(delay[u] <= L).OnlyEnforceIf(x[i])
    
    # Objective: minimize total cost
    total_cost = sum(c * x[i] for i, (_, _, _, c) in enumerate(edges))
    model.Minimize(total_cost)
    
    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        print(int(solver.ObjectiveValue()))
    else:
        print("NO_SOLUTION")

if __name__ == "__main__":
    solve_broadcast()