import random

pchelka = "81ss;qiq9012h2"
sluch_simbol = pchelka[random.randint(0, len(pchelka) - 1)]
print(sluch_simbol)

class Story:
    stories = []

    def __init__(self, name, events, duration):
        self.name = name
        self.events = events
        self.duration = duration

        Story.stories.append(self)