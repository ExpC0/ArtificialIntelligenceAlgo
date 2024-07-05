import math

MAX_VAL, MIN_VAL = 100000, -100000

def alpha_beta_pruning(depth, nodeIndex, isMaximizer, values, alpha, beta, path):
    global max_depth
    max_depth = max(max_depth, depth)
    if depth == max_depth:
        return values[nodeIndex], path

    if isMaximizer:
        best = MIN_VAL
        best_path = None
        for i in range(0, 2):
            val, new_path = alpha_beta_pruning(depth + 1, nodeIndex * 2 + i, False, values, alpha, beta, path + [i])
            if val > best:
                best = val
                best_path = new_path
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best, best_path
    else:
        best = MAX_VAL
        best_path = None
        for i in range(0, 2):
            val, new_path =alpha_beta_pruning(depth + 1, nodeIndex * 2 + i, True, values, alpha, beta, path + [i])
            if val < best:
                best = val
                best_path = new_path
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best, best_path

values = [3, 4, 5, 6,7, 3, 9, 0]
alpha = MIN_VAL
beta = MAX_VAL
initial_path = []
total_nodes = len(values)
max_depth = math.ceil(math.log2(total_nodes))
optimal_value, optimal_path = alpha_beta_pruning(0, 0, True, values, alpha, beta, initial_path)
print("Optimal value:", optimal_value)
print("Optimal path:", optimal_path)

# output
# Optimal value: 7
# Optimal path: [1, 0, 0]