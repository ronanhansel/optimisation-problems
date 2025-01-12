from ortools.linear_solver import pywraplp

def solve_cvrp():
    # Read input
    n, K, Q = map(int, input().split())
    demands = [0] + list(map(int, input().split()))
    
    dist = []
    for _ in range(n + 1):
        dist.append(list(map(int, input().split())))
    
    # Create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    # Variables
    x = {}
    for i in range(n + 1):
        for j in range(n + 1):
            for k in range(K):
                if i != j:
                    x[i,j,k] = solver.BoolVar(f'x_{i}_{j}_{k}')
    
    truck_load = {}
    for k in range(K):
        truck_load[k] = solver.IntVar(0, Q, f'load_{k}')
    
    # 1. Each client visited exactly once
    for j in range(1, n + 1):
        solver.Add(sum(x[i,j,k] for i in range(n + 1) for k in range(K) if i != j) == 1)
    
    # 2. Flow conservation
    for k in range(K):
        for j in range(n + 1):
            solver.Add(
                sum(x[i,j,k] for i in range(n + 1) if i != j) ==
                sum(x[j,i,k] for i in range(n + 1) if i != j)
            )
    
    # 3. Capacity constraints
    for k in range(K):
        solver.Add(
            sum(demands[j] * sum(x[i,j,k] for i in range(n + 1) if i != j)
                for j in range(1, n + 1)) <= Q
        )
    
    # 4. Subtour elimination using MTZ
    u = {}
    for i in range(n + 1):
        for k in range(K):
            u[i,k] = solver.IntVar(0, n, f'u_{i}_{k}')
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(K):
                if i != j:
                    solver.Add(u[i,k] - u[j,k] + n * x[i,j,k] <= n - 1)
    
    # Objective
    objective = solver.Objective()
    for i in range(n + 1):
        for j in range(n + 1):
            for k in range(K):
                if i != j:
                    objective.SetCoefficient(x[i,j,k], dist[i][j])
    objective.SetMinimization()
    
    # Solve
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        print(int(solver.Objective().Value()))
    else:
        print(-1)

if __name__ == "__main__":
    solve_cvrp()