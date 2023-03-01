from process import Process
from itertools import chain, combinations
import copy

class Byzantine(Process):

    def __init__(self, id, victims):
        Process.__init__(self, id)
        self.victims = victims
        self.individualShares = []
        #self.extractedShares = []
        #self.extractedShares.append(self.signature)
        self.extracted = {}
        for victim in victims:
            self.extracted[victim] = False

    def receive(self, sig):
        Process.receive(self,sig)
        x = copy.deepcopy(sig)
        self.individualShares.append(x)
        self.canExtract(sig)

    def canExtract(self, sig):
        for victim in self.victims:
            if self.extracted[victim]:
                break
            if sig.include(victim):
                tmpSig = [x for i, x in enumerate(sig.signatures) if x != victim]
                subsets = list(self.powerset(tmpSig))
                for subset in subsets:
                    if self.extracted[victim]:
                        break
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
                                break

    def allVictimsExtracted(self):
        print (self.victims)
        for victim in self.victims:
            if not self.extracted[victim]:
                return False
        return True

    def powerset(self, iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        return chain.from_iterable(combinations(iterable, r) for r in range(1, len(iterable) + 1))