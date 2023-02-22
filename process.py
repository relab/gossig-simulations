from signature import Signature
import random

class Process:

    def __init__(self, id):
        self.id = id
        self.signature = Signature(id)

    def receive(self, sig):
        self.signature.append(sig)

    def send(self, k, committee):
        samples = []
        while(True):
            samples = random.sample(committee, k)
            if self not in samples:
                break
        receivers = []
        for sample in samples:
            receivers.append((sample, self.signature))
        return receivers

    def hasQuorom(self, size):
        if self.signature.isQuorom(size):
            return True
        return False
