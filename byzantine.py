from process import Process
from itertools import chain, combinations
import copy

class Byzantine(Process):

    def __init__(self, id, victims):
        Process.__init__(self, id)
        self.victims = victims
        self.individualShares = []
        x = copy.deepcopy(self.signature)
        self.individualShares.append(x)
        self.extractedShares = {}
        self.extractedShares[x.toString()] = x
        self.extracted = {}
        for victim in victims:
            self.extracted[victim] = False

    def receive(self, sig):
        Process.receive(self,sig)
        x = copy.deepcopy(sig)
        self.individualShares.append(x)
        self.extract(sig)

    def extract(self, sig):
        print(len(self.extractedShares))
        queue = [sig]
        while(len(queue) > 0):
            for victim in self.victims:
                if str(victim) in self.extractedShares:
                    self.extracted[victim] = True
            if self.allVictimsExtracted():
                return True
            sig = queue.pop()
            exs = {}
            for share in self.extractedShares:
                shareSig = self.extractedShares[share]
                if shareSig.subset(sig) and shareSig.toString() != sig.toString():
                    extracted = sig.subtract(shareSig)
                    if extracted.toString() not in self.extractedShares:
                        exs[extracted.toString()] = extracted
                        #print(extracted.toString())
                if len(self.extractedShares) > 2000:
                    return self.allVictimsExtracted()
            for ex in exs:
                self.extractedShares[ex] = exs[ex]
                queue.append(exs[ex])
        return self.allVictimsExtracted()

    def allVictimsExtracted(self):
        for victim in self.victims:
            if not self.extracted[victim]:
                return False
        return True

    def powerset(self, iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        return chain.from_iterable(combinations(iterable, r) for r in range(1, len(iterable) + 1))