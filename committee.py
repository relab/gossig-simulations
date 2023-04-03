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

    def allVictimsExtracted(self):
        for v in self.validators:
            if isinstance(v, Byzantine):
                if v.allVictimsExtracted():
                    return True
        return False

    def exchangeShares(self, sender):
        for v in self.validators:
            if isinstance(v, Byzantine):
                for share in sender.extractedShares:
                    if share not in v.extractedShares:
                        v.extractedShares[share] = sender.extractedShares[share]

    def start(self):
        samples = random.sample(self.validators, 1)
        leader = samples[0]

        queue = []

        messages = leader.send(self.k, self.validators)

        for tuple in messages:
            queue.append(tuple)

        while(True):
            if self.allVictimsExtracted():
                return True
            if leader.hasQuorom(self.size):
                print(len(queue))
                while len(queue)>0:
                    if self.allVictimsExtracted():
                        return True
                    (receiver , sig) = queue.pop(0)
                    receiver.receive(sig)
                return self.allVictimsExtracted()

            (receiver , sig) = queue.pop(0)
            #print(sig.signatures)
            receiver.receive(sig)
            if isinstance(receiver, Byzantine):
                self.exchangeShares(receiver)
            messages = receiver.send(self.k, self.validators)
            for tuple in messages:
                queue.append(tuple)
            #print(leader.signature.signatures)


