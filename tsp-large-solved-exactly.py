from ortools.sat.python import cp_model

def solve_tsp():
    # Read input
    n = int(input())
    dist = []
    for _ in range(n):
        row = list(map(int, input().split()))
        dist.append(row)
    
    # Create model
    model = cp_model.CpModel()
    
    # Create variables for successor of each city
    succ = [model.NewIntVar(0, n-1, f'succ_{i}') for i in range(n)]
    
    # Create circuit
    arcs = []
    for i in range(n):
        for j in range(n):
            if i != j:
                lit = model.NewBoolVar(f'arc_{i}_{j}')
                model.Add(succ[i] == j).OnlyEnforceIf(lit)
                arcs.append((i, j, lit))
    
    model.AddCircuit(arcs)
    
    # Calculate total distance
    total_distance = model.NewIntVar(0, sum(max(row) for row in dist), 'total_distance')
    distance_terms = []
    
    for i in range(n):
        dist_var = model.NewIntVar(0, max(max(row) for row in dist), f'dist_{i}')
        distance_terms.append(dist_var)
        model.AddElement(succ[i], dist[i], dist_var)
    
    model.Add(total_distance == sum(distance_terms))
    model.Minimize(total_distance)
    
    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        # Reconstruct tour
        tour = [0]  # Start at city 0 (1 in 1-based indexing)
        current = 0
        for _ in range(n-1):
            current = solver.Value(succ[current])
            tour.append(current)
        
        # Output
        print(n)
        print(' '.join(str(x + 1) for x in tour))

if __name__ == "__main__":
    solve_tsp()

