from ortools.sat.python import cp_model

def solve_cbus():
    # Input
    n, k = map(int, input().split())
    dist = []
    for _ in range(2*n + 1):
        dist.append(list(map(int, input().split())))
    
    model = cp_model.CpModel()
    
    # Variables
    x = {}  # Binary variable for edges
    for i in range(2*n + 1):
        for j in range(2*n + 1):
            if i != j:
                x[i,j] = model.NewBoolVar(f'x_{i}_{j}')
    
    visit = [model.NewIntVar(0, 2*n, f'visit_{i}') for i in range(2*n + 1)]
    load = [model.NewIntVar(0, k, f'load_{i}') for i in range(2*n + 1)]
    
    # Circuit constraints
    for i in range(2*n + 1):
        # Outbound constraint: From each point, there must be exactly one outgoing edge.
        model.Add(sum(x[i,j] for j in range(2*n + 1) if j != i) == 1)
        # Inbound constraint: To each point, there must be exactly one incoming edge.
        model.Add(sum(x[j,i] for j in range(2*n + 1) if j != i) == 1)
    
    # Pickup before delivery
    model.Add(visit[0] == 0)  # Start at depot
    for i in range(1, n+1):
        model.Add(visit[i] < visit[i+n])  # Pickup i before delivery i+n
    
    # MTZ subtour elimination
    for i in range(2*n + 1):
        for j in range(2*n + 1):
            if i != j and i != 0 and j != 0:
                model.Add(visit[i] - visit[j] + (2*n + 1) * x[i,j] <= 2*n)
    
    # Load tracking
    model.Add(load[0] == 0)  # Start empty
    for i in range(1, n+1):
        # After pickup i
        for j in range(2*n + 1):
            if j != i:
                model.Add(load[j] >= load[i] + 1).OnlyEnforceIf(x[i,j])
        # After delivery i+n
        for j in range(2*n + 1):
            if j != i+n:
                model.Add(load[j] >= load[i+n] - 1).OnlyEnforceIf(x[i+n,j])
    
    # Objective
    total_dist = model.NewIntVar(0, 10000, 'total_dist')
    model.Add(total_dist == sum(dist[i][j] * x[i,j] 
                               for i in range(2*n + 1) 
                               for j in range(2*n + 1) if i != j))
    model.Minimize(total_dist)
    
    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        print(int(solver.Value(total_dist)))
    else:
        print(-1)

if __name__ == "__main__":
    solve_cbus()