import random

def read_input():
    n = int(input())
    distance_matrix = []
    for _ in range(n):
        distance_matrix.append(list(map(int, input().split())))
    return n, distance_matrix

def calculate_total_distance(tour, distance_matrix):
    total_distance = 0
    for i in range(len(tour)):
        total_distance += distance_matrix[tour[i] - 1][tour[(i + 1) % len(tour)] - 1]
    return total_distance

def local_search(n, distance_matrix):
    current_tour = list(range(1, n + 1))
    random.shuffle(current_tour)
    current_distance = calculate_total_distance(current_tour, distance_matrix)
    
    improved = True
    while improved:
        improved = False
        for i in range(n):
            for j in range(i + 1, n):
                new_tour = current_tour[:]
                new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
                new_distance = calculate_total_distance(new_tour, distance_matrix)
                if new_distance < current_distance:
                    current_tour = new_tour
                    current_distance = new_distance
                    improved = True
    return current_tour

def main():
    n, distance_matrix = read_input()
    best_tour = local_search(n, distance_matrix)
    print(n)
    print(' '.join(map(str, best_tour)))

if __name__ == "__main__":
    main()