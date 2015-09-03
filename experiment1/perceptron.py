class Perceptron:

    def __init__(self, identifier):
        self.id = identifier
        self.arcs = {}
        self.receivedSignals = 0

    def connect(self, node, weight=0):
        self.arcs[node.id] = {
            'destination': node,
            'weight': weight
        }

    def add_signal(self, signal):
        self.receivedSignals += signal

    def reset_signals(self):
        self.receivedSignals = 0

    def send(self, receiver):
        weight = self.arcs[receiver.id]['weight']
        receiver.add_signal(weight)

    def is_active(self):
        return self.receivedSignals > 0

    def broadcast(self):
        if self.is_active():
            for identifier, arc in self.arcs.items():
                self.send(arc['destination'])
        self.reset_signals()

    def get_arcs(self):
        result = {}
        for key, arc in self.arcs.items():
            result[key] = arc['weight']
        return result
