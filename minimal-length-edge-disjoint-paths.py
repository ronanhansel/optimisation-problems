from ortools.graph.python import min_cost_flow

def solve():
    # Read input
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, c = map(int, input().split())
        edges.append((u-1, v-1, c))  # Convert to 0-based indexing
    
    # Create graph
    start_node = 0
    end_node = n-1
    
    # Initialize min cost flow solver
    smcf = min_cost_flow.SimpleMinCostFlow()
    
    # Add each edge with capacity 1
    for u, v, c in edges:
        smcf.add_arc_with_capacity_and_unit_cost(u, v, 1, c)
    
    # Set supplies and demands
    smcf.set_node_supply(start_node, 2)  # Source sends 2 units
    smcf.set_node_supply(end_node, -2)   # Sink receives 2 units
    
    # Find solution
    status = smcf.solve()
    
    if status != smcf.OPTIMAL:
        print("NOT_FEASIBLE")
        return
    
    # Calculate total cost
    total_cost = smcf.optimal_cost()
    print(total_cost)

if __name__ == "__main__":
    solve()