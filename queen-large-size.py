from ortools.sat.python import cp_model

def solve_nqueens(n):
    model = cp_model.CpModel()

    # Create variables: x[i] represents the row of the queen in column i
    x = [model.NewIntVar(1, n, f'x[{i}]') for i in range(n)]

    # Constraints:
    # 1. No two queens on the same row
    model.AddAllDifferent(x)

    # 2. No two queens on the same diagonal
    for i in range(n):
        for j in range(i + 1, n):
            model.Add(x[i] - x[j] != i - j)  # Upward diagonal
            model.Add(x[i] - x[j] != j - i)  # Downward diagonal

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print(n)
        print(' '.join(str(solver.Value(x[i])) for i in range(n)))

if __name__ == "__main__":
    solve_nqueens(int(input()))