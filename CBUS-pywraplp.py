from ortools.linear_solver import pywraplp

def solve_cbus():
    # Input
    n, k = map(int, input().split())
    dist = []
    for _ in range(2*n + 1):
        dist.append(list(map(int, input().split())))
    
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Variables
    x = {}
    for i in range(2*n + 1):
        for j in range(2*n + 1):
            if i != j:
                x[i,j] = solver.BoolVar(f'x_{i}_{j}')
    
    visit = {}
    load = {}
    for i in range(2*n + 1):
        visit[i] = solver.IntVar(0, 2*n, f'visit_{i}')
        load[i] = solver.IntVar(0, k, f'load_{i}')
    
    # Circuit constraints
    for i in range(2*n + 1):
        solver.Add(sum(x[i,j] for j in range(2*n + 1) if j != i) == 1)
        solver.Add(sum(x[j,i] for j in range(2*n + 1) if j != i) == 1)
    
    # Pickup before delivery - fixed
    solver.Add(visit[0] == 0)
    for i in range(1, n+1):
        solver.Add(visit[i] + 1 <= visit[i+n])
    
    # MTZ subtour elimination
    for i in range(2*n + 1):
        for j in range(2*n + 1):
            if i != j and i != 0 and j != 0:
                solver.Add(visit[i] - visit[j] + (2*n + 1) * x[i,j] <= 2*n)
    
    # Load tracking
    solver.Add(load[0] == 0)
    for i in range(1, n+1):
        for j in range(2*n + 1):
            if j != i:
                solver.Add(load[j] >= load[i] + 1 - k * (1 - x[i,j]))
            if j != i+n:
                solver.Add(load[j] >= load[i+n] - 1 - k * (1 - x[i+n,j]))
    
    # Objective
    objective = solver.Objective()
    for i in range(2*n + 1):
        for j in range(2*n + 1):
            if i != j:
                objective.SetCoefficient(x[i,j], dist[i][j])
    objective.SetMinimization()
    
    solver.SetTimeLimit(300000)
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print(int(solver.Objective().Value()))
    else:
        print(-1)

if __name__ == "__main__":
    solve_cbus()