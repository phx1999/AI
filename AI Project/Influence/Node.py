
class Node(object):

    def __init__(self,state,thresh):
        self.state=state
        self.thresh=thresh
        self.outnei = []
        self.innei = []

    def add_innei(self,innei):
        self.innei.append(innei)

    def add_outnei(self,outnei):
        self.outnei.append(outnei)

    def set_thresh(self,thresh):
        self.thresh=thresh

    def get_innei(self):
        return self.innei

    def get_outnei(self):
        return self.outnei

    def unactive(self):
        self.state=0

    def active(self):
        self.state=1