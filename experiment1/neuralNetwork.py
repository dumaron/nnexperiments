from perceptron import Perceptron


class NeuralNetwork:

    def __init__(self):
        self.inputNodes = []
        self.outputNodes = []
        self.hiddenNodes = []

    def all_nodes(self):
        return self.inputNodes + self.outputNodes + self.hiddenNodes

    def get_node_by_id(self, identifier):
        node = False

        for n in self.all_nodes():
            if n.id == identifier:
                node = n

        return node

    def generate(self, num_input_perceptrons, num_hidden_perceptrons, num_output_perceptrons):
        identifier = 1

        for count in range(0, num_output_perceptrons):
            self.outputNodes.append(Perceptron(identifier))
            identifier += 1

        for count in range(0, num_hidden_perceptrons):
            new_node = Perceptron(identifier)
            self.hiddenNodes.append(new_node)
            identifier += 1
            for node in self.outputNodes:
                new_node.connect(node)

        for count in range(0, num_input_perceptrons):
            new_node = Perceptron(identifier)
            self.inputNodes.append(new_node)
            identifier += 1
            for node in self.hiddenNodes:
                new_node.connect(node)

    def load_input_signals(self, signals):
        for index, signal in enumerate(signals):
            node = self.inputNodes[index]
            node.reset_signals()
            node.add_signal(signal)

    def get_output_signals(self):
        return [node.receivedSignals for node in self.outputNodes]

    def process(self):
        for node in self.inputNodes:
            node.broadcast()

        for node in self.hiddenNodes:
            node.broadcast()

    def add_node(self, identifier, location):
        if location == 'input':
            self.inputNodes.append(Perceptron(identifier))
        elif location == 'output':
            self.outputNodes.append(Perceptron(identifier))
        elif location == 'hidden':
            self.hiddenNodes.append(Perceptron(identifier))

    def evolve(self, stepper):
        new_net = NeuralNetwork()

        for p in self.outputNodes:
            new_net.add_node(p.id, 'output')

        for p in self.hiddenNodes:
            new_net.add_node(p.id, 'hidden')
            for identifier, weight in p.get_arcs().items():
                arc_start = new_net.get_node_by_id(p.id)
                arc_end = new_net.get_node_by_id(identifier)
                arc_start.connect(arc_end, weight + stepper())

        for p in self.inputNodes:
            new_net.add_node(p.id, 'input')
            for identifier, weight in p.get_arcs().items():
                arc_start = new_net.get_node_by_id(p.id)
                arc_end = new_net.get_node_by_id(identifier)
                arc_start.connect(arc_end, weight + stepper())

        return new_net
