import pulp

def create_dobble_game(n):
    total_cards = total_symbols = n * n + n + 1
    symbols_per_card = n + 1

    # Create a new LP problem
    prob = pulp.LpProblem("DobbleGame", pulp.LpMinimize)

    # Variables: x[i, j] is 1 if card i contains symbol j, 0 otherwise
    x = pulp.LpVariable.dicts("x", ((i, j) for i in range(total_cards) for j in range(total_symbols)),
                              cat=pulp.LpBinary)

    # Auxiliary variables: y[i, k, j] is 1 if card i and k both contain symbol j
    y = pulp.LpVariable.dicts("y", ((i, k, j) for i in range(total_cards) for k in range(i + 1, total_cards) for j in range(total_symbols)),
                              cat=pulp.LpBinary)

    # Constraint: each card has exactly 'symbols_per_card' symbols
    for i in range(total_cards):
        prob += pulp.lpSum(x[i, j] for j in range(total_symbols)) == symbols_per_card

    # Constraints for y[i, k, j]
    for i in range(total_cards):
        for k in range(i + 1, total_cards):
            for j in range(total_symbols):
                prob += y[i, k, j] <= x[i, j]
                prob += y[i, k, j] <= x[k, j]
                prob += y[i, k, j] >= x[i, j] + x[k, j] - 1
            # Exactly one common symbol per card pair
            prob += pulp.lpSum(y[i, k, j] for j in range(total_symbols)) == 1

    # Continuing from the previous setup
    # Additional symmetry-breaking constraints
    for j in range(symbols_per_card):
        prob += x[0, j] == 1  # Ensure the first symbols are on the first card in ascending order

    for i in range(1, total_cards):
        prob += x[i, i - 1] == 1  # Encourage subsequent cards to include subsequent symbols in a sequence

    # Solve the problem
    status = prob.solve()

    # Check if a solution was found
    if status == pulp.LpStatusOptimal:
        print("Solution Found:")
        for i in range(total_cards):
            print(f'Card {i}:', end=' ')
            for j in range(total_symbols):
                if pulp.value(x[i, j]) == 1:
                    print(j, end=' ')
            print()
    else:
        print("No solution found. Status:", pulp.LpStatus[status])

# Let's try to create the game for n = 8
if __name__ == '__main__':
    create_dobble_game(4)
