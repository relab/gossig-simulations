from process import Process

class FreeRider(Process):

    def __init__(self, id, maxParticipation):
        Process.__init__(self, id)
        self.maxParticipation = maxParticipation
        self.countParticipation = 0

    def send(self, k, committee):
        if self.countParticipation < self.maxParticipation:
            self.countParticipation += 1
            return Process.send(self, k, committee)
        else:
            return []
