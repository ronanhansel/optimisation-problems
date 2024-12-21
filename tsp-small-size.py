import ortools.sat.python.cp_model as cp_model

def solve_tsp():
    # Read input
    n = int(input())
    dist = []
    for _ in range(n):
        row = list(map(int, input().split()))
        dist.append(row)

    # Create model
    model = cp_model.CpModel()

    succ = [model.NewIntVar(0, n - 1, f'succ_{i}') for i in range(n)]

    arcs = []
    for i in range(n):
        for j in range(n):
            if i != j:
                lit = model.NewBoolVar(f'arc_{i}_{j}')
                model.Add(succ[i] == j).OnlyEnforceIf(lit)
                arcs.append((i, j, lit))

    model.AddCircuit(arcs)
    
    total_distance = model.NewIntVar(0, sum(max(row) for row in dist), 'total_distance')

    distance_terms = []

    for i in range(n):
        dist_var = model.NewIntVar(0, max(max(row) for row in dist), f'dist_{i}')
        distance_terms.append(dist_var)
        model.AddElement(succ[i], dist[i], dist_var)
    
    model.Add(total_distance == sum(distance_terms))
    model.Minimize(total_distance)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        tour = [0]
        current = 0
        for _ in range(n-1):
            current = solver.Value(succ[current])
            tour.append(current)
        print(int(solver.ObjectiveValue()))

if __name__ == "__main__":
    solve_tsp()