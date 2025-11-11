import os
from .InputFile import InputFile
from .ICalculation import ICalculation

class Calculation(ICalculation):
    """Base class for all Calculations in NCRL
    
    Provides common functionality and defines the interface for all Calculation types.
    
    Inherit this class when implementing a new Calculation type. 
    Ensure that the calculate() method is overridden to provide specific calculation logic.
    
    
    
    
    """
    
    def __init__(self, inputFile : InputFile):
        
        if (not isinstance(inputFile, InputFile)):
            raise TypeError("The inputFile must be of type InputFile")
        
        self.baseCachePath = os.path.join(os.getcwd(), "Cache")
        self.inputFile = inputFile
    
    def calculate(self):
        raise NotImplementedError("Calculate function has not been implemented")
    
    def setup(self):
        if (not os.path.exists(self.baseCachePath)):
            os.mkdir(self.baseCachePath)
    
    def getInputFileName(self):
        return self.inputFile.name + self.inputFile.extension
    
    def getOutputFileName(self):
        return self.inputFile.name + ".out"