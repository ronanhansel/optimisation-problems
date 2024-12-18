from ortools.sat.python import cp_model

def solve():
    # Read input
    m, n = map(int, input().split())
    preferences = {}
    for i in range(1, m+1):
        prefs = list(map(int, input().split()))
        preferences[i] = prefs[1:]
    
    k = int(input())
    conflicts = set()
    for _ in range(k):
        c1, c2 = map(int, input().split())
        conflicts.add((c1, c2))
        conflicts.add((c2, c1))
    
    # Create model
    model = cp_model.CpModel()
    
    # Course assignment variables
    course_teacher = {}
    for course in range(1, n+1):
        course_teacher[course] = model.NewIntVar(1, m, f'c{course}')
    
    # Teacher load variables
    teacher_load = {}
    for teacher in range(1, m+1):
        teacher_load[teacher] = model.NewIntVar(0, n, f't{teacher}')
    
    max_load = model.NewIntVar(0, n, 'max_load')
    
    # Preferences constraint
    for course in range(1, n+1):
        allowed_teachers = [t for t in range(1, m+1) if course in preferences[t]]
        for teacher in range(1, m+1):
            if teacher not in allowed_teachers:
                model.Add(course_teacher[course] != teacher)
    
    # Conflicts constraint
    for c1, c2 in conflicts:
        model.Add(course_teacher[c1] != course_teacher[c2])
    
    # Load calculation using boolean variables
    for teacher in range(1, m+1):
        teaches_vars = []
        for course in range(1, n+1):
            teaches = model.NewBoolVar(f'teaches_{teacher}_{course}')
            model.Add(course_teacher[course] == teacher).OnlyEnforceIf(teaches)
            model.Add(course_teacher[course] != teacher).OnlyEnforceIf(teaches.Not())
            teaches_vars.append(teaches)
        model.Add(teacher_load[teacher] == sum(teaches_vars))
        model.Add(max_load >= teacher_load[teacher])
    
    # Minimize maximum load
    model.Minimize(max_load)
    
    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        print(solver.Value(max_load))
    else:
        print(-1)

if __name__ == "__main__":
    solve()