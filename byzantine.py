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
        if self.allVictimsExtracted():
            return True
        queue = [sig]
        while(len(queue) > 0):
            sig = queue.pop()
            exs = {}
            for share in self.extractedShares:
                shareSig = self.extractedShares[share]
                if shareSig.subset(sig) and shareSig.toString() != sig.toString():
                    extracted = sig.subtract(shareSig)
                    if extracted.toString() not in self.extractedShares:
                        exs[extracted.toString()] = extracted
            for ex in exs:
                self.extractedShares[ex] = exs[ex]
                queue.append(exs[ex])
        for victim in self.victims:
            if str(victim) in self.extractedShares:
                self.extracted[victim] = True
                return True

    def canExtract(self, sig):
        print(sig.toString())
        for victim in self.victims:
            if self.extracted[victim]:
                break
            if sig.include(victim):
                tmpSig = copy.deepcopy(sig.signatures)
                #tmpSig = [x for i, x in enumerate(sig.signatures) if x != victim]
                tmpSig.remove(victim)
                subsets = list(self.powerset(tmpSig))
                for subset in subsets:
                    if self.extracted[victim]:
                        break
                    print(subset)
                    for share in self.individualShares:
                        if share.len() == len(subset):
                            flag = True
                            for s in subset:
                                if not share.include(s):
                                    flag = False
                                    break
                            if flag:
                                self.extracted[victim] = True
                                print ("YAAAAAAAY")
                                for s in self.individualShares:
                                    print(s.signatures)
                                print("%%%%%")
                                break

    def allVictimsExtracted(self):
        for victim in self.victims:
            if not self.extracted[victim]:
                return False
        return True

    def powerset(self, iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        return chain.from_iterable(combinations(iterable, r) for r in range(1, len(iterable) + 1))