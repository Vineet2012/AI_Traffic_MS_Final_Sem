import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)  # Ensures reproducibility

def fitness_function(C, g, x, c):
    a = (1 - (g / C)) ** 2
    p = 1 - ((g / C) * x)
    if p == 0:
        p = 1e-6  # Prevent division by zero

    d1i = (0.38 * C * a) / p

    a2 = 173 * (x ** 2)
    ri1_val = (x - 1) + (x - 1) ** 2 + ((16 * x) / c)
    ri1 = np.sqrt(max(0, ri1_val))  # Prevent invalid sqrt

    d2i = a2 * ri1

    return d1i + d2i

def fairness_penalty(green_times, congestion, cycle_time):
    # Penalize only if green times are not aligned with congestion
    penalty = 0
    for i in range(len(green_times)):
        for j in range(i + 1, len(green_times)):
            ideal_diff = (congestion[i] - congestion[j]) * cycle_time
            actual_diff = green_times[i] - green_times[j]
            penalty += abs(actual_diff - ideal_diff)
    return penalty * 0.1  # Reduced penalty weight

def initialize_population(pop_size, num_lights, green_min, green_max, cycle_time, cars):
    population = []
    road_capacity = [20] * num_lights
    normalized_cars = np.array(cars) / np.max(cars)

    while len(population) < pop_size:
        green_times = np.random.randint(green_min, green_max + 1, num_lights)
        if np.sum(green_times) <= cycle_time:
            total_delay = np.sum([
                fitness_function(cycle_time, green_times[i], normalized_cars[i], road_capacity[i])
                for i in range(num_lights)
            ])
            fairness = fairness_penalty(green_times, normalized_cars, cycle_time)
            total_delay += fairness
            if not np.isnan(total_delay):
                population.append((green_times, total_delay))
    return sorted(population, key=lambda x: x[1])

def roulette_wheel_selection(population, total_delays, beta):
    total_delays = np.array(total_delays)
    if np.any(np.isnan(total_delays)) or np.any(np.isinf(total_delays)):
        raise ValueError("Delays contain invalid values.")

    worst_delay = max(total_delays)
    probabilities = np.exp(-beta * total_delays / worst_delay)

    if np.sum(probabilities) == 0 or np.isnan(np.sum(probabilities)):
        raise Exception("Probabilities contain NaN or sum to zero.")

    probabilities /= np.sum(probabilities)
    return np.random.choice(len(population), p=probabilities)

def crossover(parent1, parent2, num_lights):
    point = np.random.randint(1, num_lights)
    child1 = np.concatenate([parent1[:point], parent2[point:]])
    child2 = np.concatenate([parent2[:point], parent1[point:]])
    return child1, child2

def mutate(individual, mutation_rate, green_min, green_max):
    num_lights = len(individual)
    mutated = individual.copy()
    for _ in range(int(mutation_rate * num_lights)):
        idx = np.random.randint(0, num_lights)
        sigma = np.random.choice([-1, 1]) * 0.02 * (green_max - green_min)
        mutated[idx] = np.clip(individual[idx] + sigma, green_min, green_max)
    return mutated

def inversion(individual, num_lights):
    idx1, idx2 = np.random.randint(0, num_lights, 2)
    if idx1 > idx2:
        idx1, idx2 = idx2, idx1
    individual[idx1:idx2+1] = individual[idx1:idx2+1][::-1]
    return individual

def genetic_algorithm(pop_size, num_lights, max_iter, green_min, green_max, cycle_time, mutation_rate, pinv, beta, cars):
    population = initialize_population(pop_size, num_lights, green_min, green_max, cycle_time, cars)
    best_sol = population[0]
    best_delays = [best_sol[1]]

    road_capacity = [20] * num_lights
    normalized_cars = np.array(cars) / np.max(cars)

    for _ in range(max_iter):
        total_delays = [ind[1] for ind in population]
        new_population = []

        while len(new_population) < pop_size:
            try:
                i1 = roulette_wheel_selection(population, total_delays, beta)
                i2 = roulette_wheel_selection(population, total_delays, beta)
            except Exception as e:
                print(f"[Warning] Selection issue: {e}")
                break

            parent1, parent2 = population[i1][0], population[i2][0]
            child1, child2 = crossover(parent1, parent2, num_lights)

            for child in [child1, child2]:
                if np.sum(child) <= cycle_time:
                    child = mutate(child, mutation_rate, green_min, green_max)
                    child = np.clip(child, green_min, green_max)
                    total_delay = np.sum([
                        fitness_function(cycle_time, child[i], normalized_cars[i], road_capacity[i])
                        for i in range(num_lights)
                    ])
                    fairness = fairness_penalty(child, normalized_cars, cycle_time)
                    total_delay += fairness
                    if not np.isnan(total_delay):
                        new_population.append((child, total_delay))

        while len(new_population) < pop_size:
            i = np.random.randint(0, len(population))
            individual = inversion(population[i][0], num_lights)
            if np.sum(individual) <= cycle_time:
                individual = mutate(individual, mutation_rate, green_min, green_max)
                total_delay = np.sum([
                    fitness_function(cycle_time, individual[i], normalized_cars[i], road_capacity[i])
                    for i in range(num_lights)
                ])
                fairness = fairness_penalty(individual, normalized_cars, cycle_time)
                total_delay += fairness
                if not np.isnan(total_delay):
                    new_population.append((individual, total_delay))

        population += new_population
        population = sorted(population, key=lambda x: x[1])[:pop_size]

        if population[0][1] < best_sol[1]:
            best_sol = population[0]

        best_delays.append(best_sol[1])

    return best_sol, best_delays

def optimize_traffic(traffic_data):
    pop_size = 400
    num_lights = 4
    max_iter = 25
    green_min = 10
    green_max = 60
    total_cycle_time = 160 - 12  # total available green time in a cycle
    mutation_rate = 0.02
    pinv = 0.2
    beta = 8

    directions = ['north', 'south', 'west', 'east']
    vehicle_counts = []
    ambulance_direction = None

    # Extract vehicle counts and find if ambulance is present
    for dir in directions:
        entry = next((item for item in traffic_data if item['direction'] == dir), None)
        if entry:
            vehicle_counts.append(entry['vehicle_count'])
            if entry.get('ambulance_detected'):
                ambulance_direction = dir
        else:
            vehicle_counts.append(0)

    result = {}

    if ambulance_direction:
        # Give full 60 seconds green to ambulance direction
        fixed_green = {d: 0 for d in directions}
        fixed_green[ambulance_direction] = 60
        remaining_time = total_cycle_time - 60

        # Prepare input for other directions
        other_dirs = [d for d in directions if d != ambulance_direction]
        other_counts = [vehicle_counts[directions.index(d)] for d in other_dirs]

        # Optimize for remaining directions
        best_sol, _ = genetic_algorithm(
            pop_size=pop_size,
            num_lights=3,
            max_iter=max_iter,
            green_min=green_min,
            green_max=green_max,
            cycle_time=remaining_time,
            mutation_rate=mutation_rate,
            pinv=pinv,
            beta=beta,
            cars=other_counts
        )

        # Fill result
        for i, d in enumerate(other_dirs):
            result[d] = {
                "green_time": int(best_sol[0][i])
            }
        # Add ambulance direction with message
        result[ambulance_direction] = {
            "green_time": 60,
            "message": "Ambulance detected"
        }

    else:
        # No ambulance, optimize for all directions
        best_sol, _ = genetic_algorithm(
            pop_size, num_lights, max_iter, green_min, green_max,
            total_cycle_time, mutation_rate, pinv, beta, vehicle_counts
        )

        for i, d in enumerate(directions):
            result[d] = {
                "green_time": int(best_sol[0][i])
            }

    # Debug output
    print('Optimal Solution:')
    for d in directions:
        if "message" in result[d]:
            print(f'{d.capitalize()} Green Time = {result[d]["green_time"]} seconds ({result[d]["message"]})')
        else:
            print(f'{d.capitalize()} Green Time = {result[d]["green_time"]} seconds')

    return result



# Example test
if __name__ == "__main__":
    cars = [30, 25, 20, 35]  # Adjust to test different congestions
    optimize_traffic(cars)
