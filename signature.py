class Signature:

    def __init__(self):
        self.signatures = []
        self.processesNumber = 0

    def __init__(self, initialId):
        self.signatures = []
        self.signatures.append(initialId)
        self.processesNumber = 0

    def include(self, signature):
        if signature in self.signatures:
            return True
        return False

    def append(self, sigs):
        kk = 0
        for sig in sigs.signatures:
            kk += 1
            if sig not in self.signatures:
                self.processesNumber += 1
            self.signatures.append(sig)

    def isQuorom(self, committeeSize):
        if self.processesNumber >= (2/3)*committeeSize:
            return True
        return False

    def len(self):
        return len(self.signatures)