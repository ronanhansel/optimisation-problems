from ortools.sat.python import cp_model

def solve_cvrp():
    # Read input
    n, K, Q = map(int, input().split())
    demands = [0] + list(map(int, input().split()))  # Add 0 for depot
    
    # Read distance matrix
    dist = []
    for _ in range(n + 1):
        dist.append(list(map(int, input().split())))
    
    # Create model
    model = cp_model.CpModel()
    
    # Variables
    # x[i][j][k] = 1 if truck k goes from i to j
    x = {}
    for i in range(n + 1):
        for j in range(n + 1):
            for k in range(K):
                if i != j:
                    x[i,j,k] = model.NewBoolVar(f'x_{i}_{j}_{k}')
    
    # truck_load[k] = total load of truck k
    truck_load = {}
    for k in range(K):
        truck_load[k] = model.NewIntVar(0, Q, f'load_{k}')
    
    # Constraints
    # 1. Each client visited exactly once
    for j in range(1, n + 1):
        model.Add(sum(x[i,j,k] for i in range(n + 1) for k in range(K) if i != j) == 1)
    
    # 2. Flow conservation
    for k in range(K):
        for j in range(n + 1):
            model.Add(
                sum(x[i,j,k] for i in range(n + 1) if i != j) ==
                sum(x[j,i,k] for i in range(n + 1) if i != j)
            )
    
    # 3. Capacity constraints
    for k in range(K):
        model.Add(
            sum(demands[j] * sum(x[i,j,k] for i in range(n + 1) if i != j)
                for j in range(1, n + 1)) <= Q
        )
    
    # 4. Subtour elimination using MTZ formulation
    u = {}
    for i in range(n + 1):
        for k in range(K):
            u[i,k] = model.NewIntVar(0, n, f'u_{i}_{k}')
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(K):
                if i != j:
                    model.Add(u[i,k] - u[j,k] + n * x[i,j,k] <= n - 1)
    
    # Objective: minimize total distance
    total_dist = sum(dist[i][j] * x[i,j,k] 
                    for i in range(n + 1) 
                    for j in range(n + 1) 
                    for k in range(K) 
                    if i != j)
    model.Minimize(total_dist)
    
    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        print(int(solver.ObjectiveValue()))
    else:
        print(-1)

if __name__ == "__main__":
    solve_cvrp()