import multiprocessing
import random

from experiment1.neuralNetwork import NeuralNetwork
from environment import Environment


# variabili per l'esecuzione
num_generations = 10000
networks_per_generation = 1000
steps_per_network = 100
core = 4

# da qui meglio non toccare
best_network = NeuralNetwork()
best_network.generate(36, 36, 4)
random.seed()
best_net_steps = 0
best_net_clean = 0


def evolution_step():
    possible_values = [-1, 1]
    change = random.random() > .7
    if change:
        return random.choice(possible_values)
    return 0


def signals_to_movement(signals):
    movement_x = signals[0] - signals[1]
    movement_y = signals[2] - signals[3]
    if movement_x > movement_y:
        return 'right' if movement_x > 0 else 'left'
    elif movement_y > movement_x:
        return 'bottom' if movement_y > 0 else 'top'
    else:
        return 'none'


def process_nets(begin, end, best_net, results):
    networks = [best_net]
    local_best_steps = 0
    local_best_network = False

    for _ in range(begin, end-1):
        networks.append(best_net.evolve(evolution_step))

    for network in networks:
        env = Environment(6, 6)
        steps = 0
        for step in range(0, steps_per_network):
            network.load_input_signals(env.get_signals())
            network.process()
            direction = signals_to_movement(network.get_output_signals())
            moved = env.move(direction)
            if moved:
                steps += 1
            else:
                break

        if local_best_steps < steps:
            local_best_steps = steps
            local_best_network = network

    results.append({
        'steps': local_best_steps,
        'net': local_best_network
    })


for generation in range(1, num_generations):

    manager = multiprocessing.Manager()
    best_results = manager.list()
    processes = []

    for c in range(0, core):
        offset = networks_per_generation // core
        start = offset * c
        stop = offset * (c+1)
        p = multiprocessing.Process(target=process_nets, args=(start, stop, best_network, best_results))
        processes.append(p)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    max_steps = max([r['steps'] for r in best_results])
    if max_steps > best_net_steps:
        best_network = [r for r in best_results if r['steps'] == max_steps][0]['net']
        best_net_steps = max_steps

    print(generation, best_net_steps)

# print(best_network)