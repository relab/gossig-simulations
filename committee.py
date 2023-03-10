from process import Process
from byzantine import Byzantine
import random

class Committee:

    def __init__(self, size, m, k):
        self.m = m
        self. byzantineNumber = (int)(m* size)
        self.correctNumber = size - self.byzantineNumber
        self.size = size
        self.k = k
        self.validators = []

        j = 0
        for i in range(self.correctNumber):
            self.validators.append(Process(j))
            j+=1
        for i in range(self.byzantineNumber):
            self.validators.append(Byzantine(j,[0]))
            j+=1

    def start(self):
        samples = random.sample(self.validators, 1)
        leader = samples[0]

        queue = []

        messages = leader.send(self.k, self.validators)

        for tuple in messages:
            queue.append(tuple)

        while(True):
            if leader.hasQuorom(self.size):
                for v in self.validators:
                    if isinstance(v, Byzantine):
                        if v.allVictimsExtracted():
                            return True
                return False
            (receiver , sig) = queue.pop(0)
            print(sig.signatures)
            receiver.receive(sig)
            messages = receiver.send(self.k, self.validators)
            for tuple in messages:
                queue.append(tuple)


