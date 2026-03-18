class ResearchMemory:

    def __init__(self):
        self.sources = []

    def add(self, insight, source):

        self.sources.append({"insight": insight, "source": source})

    def get_all(self):

        return self.sources


memory = ResearchMemory()
