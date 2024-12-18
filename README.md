# Optimisation problems

This is a combination of solvers that I learned throughout the optimisation course at SOICT - HUST. The course code is IT3052E.

I do like to note that my solvers aren't necessarily the best as I used extensively external resources (due to my lack of CP skills or experience.)

## Problem: Capacitated Vehicle Routing

[Source code](capacitated-vehicle-routing.py)

### Problem statement

A fleet of K identical trucks having capacity Q need to be scheduled to deliver pepsi packages from a central depot 0 to clients 1,2,…,n. Each client i requests d[i] packages. The distance from location i to location j is c[i,j], 0≤i,j≤n. A delivery solution is a set of routes: each truck is associated with a route, starting from depot, visiting some clients and returning to the depot for delivering requested pepsi packages such that:

- Each client is visited exactly by one route
- Total number of packages requested by clients of each truck cannot exceed its capacity

Goal:

- Find a solution having minimal total travel distance

Note that:

- There might be the case that a truck does not visit any client (empty route)
- The orders of clients in a route is important, e.g., routes 0 -> 1 -> 2 -> 3 -> 0 and 0 -> 3-> 2 -> 1 -> 0 are different.

Input

- Line 1: n,K,Q (2≤n≤12,1≤K≤5,1≤Q≤50)
- Line 2: d[1],...,d[n] (1≤d[i]≤10)
- Line i+3 (i=0,…,n): the ith row of the distance matrix c (1≤c[i,j]≤30)

Output

- Minimal total travel distance

Example

Input

```text
4 2 15
7 7 11 2
0 12 12 11 14
14 0 11 14 14
14 10 0 11 12
10 14 12 0 13
10 13 14 11 0
```

Output

```text
70
```

### Problem solver (ORtool)

Using CP, we need to formulate the constraints. For this problem, the constraints are:

> Each client is visited exactly once.

```python
for j in range(1, n + 1):
        model.Add(sum(x[i,j,k] for i in range(n + 1) for k in range(K) if i != j) == 1)

```

The sum of boolean matrix `x` must be 1 for all entries from distance matrix.

> Total number of packages requested by clients cannot exceed its capacity.

```python
for k in range(K):
    model.Add(
        sum(demands[j] * sum(x[i,j,k] for i in range(n + 1) if i != j)
            for j in range(1, n + 1)) <= Q
    )
```

For a routing problem, we need to ensure:

- For each node, the sent package must be exhaustive. In other words, the number of incoming packages must be equal to the outgoing packages.

```python
for k in range(K):
    for j in range(n + 1):
        model.Add(
            sum(x[i,j,k] for i in range(n + 1) if i != j) ==
            sum(x[j,i,k] for i in range(n + 1) if i != j)
        )
```

- No subtour (circular routes that aren't the solution)

```python
u = {}
for i in range(n + 1):
    for k in range(K):
        u[i,k] = model.NewIntVar(0, n, f'u_{i}_{k}')

for i in range(1, n + 1):
    for j in range(1, n + 1):
        for k in range(K):
            if i != j:
                model.Add(u[i,k] - u[j,k] + n * x[i,j,k] <= n - 1)
```
