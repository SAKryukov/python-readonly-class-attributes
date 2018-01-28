# using class attributes:
class DefinitionSet:
    greetings = "Hello!"
    myNameFormat = "My name is {}."
    durationSeconds = 3.5
    color = { "opacity": 0.7, "wavelength": 400 }

#...
print (DefinitionSet.durationSeconds)  

# using instance attributes:
class DefinitionSet:
    def __init__(self):
        self.greetings = "Hello!"
        self.myNameFormat = "My name is {}."
        self.durationSeconds = 3.5
        self.color = { "opacity": 0.7, "wavelength": 400 }
definitionSet = DefinitionSet()

#...
print (definitionSet.durationSeconds) 