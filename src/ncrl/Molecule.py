import os
import pandas as pd
import numpy as np

class Molecule:

    def __init__(self, name: str, filePath: str):
        
        if (not isinstance(name, str)):
            raise TypeError("The name of the Molecule must be a string")
        
        if (not isinstance(filePath, str)):
            raise TypeError("The filePath of the Molecule must be a string")
        
        if len(name.strip()) == 0:
            raise ValueError("The name cannot be empty")
        
        if len(filePath.strip()) == 0:
            raise ValueError("The filePath cannot be empty")
        
        if (not os.path.exists(filePath)):
            raise FileNotFoundError(f"The file located at {filePath} does not exist")
        
        self.name: str = name
        self.filePath: str = filePath
        self.positions: pd.DataFrame = self._readXYZ(filePath)

    def _readXYZ(self, filePath: str):
        """_readXYZ(self, filePath : str)

        Extracts the Atom type and XYZ Coordinates from a `.xyz` file, returns the structure as a Pandas Dataframe

        Parameters:
            filePath (str) - The path to the XYZ File to load

        Returns:
            pd.Dataframe - Pandas Dataframe containing the following Columns, [Atom, X, Y, Z], where XYZ are the Positions
        """

        if not os.path.exists(filePath):
            raise FileNotFoundError(f"The file located at {filePath} does not exist ({os.getcwd()})")

        return pd.read_csv(
            filePath,
            sep=r"\s+",
            skiprows=2,
            names=["Atom", "X", "Y", "Z"],
            engine="python",
        )
        
    def getContent(self) -> str:
        return self.positions.to_string(header=False, index=False)

    def translate(self, vector:np.ndarray) -> None: 
        """ 
        Translates the given molecule X, Y, and Z units 

        Parameters: 
            vector(np.ndarray): Vector that stores molecule's X, Y, and Z coordinates 
        """

        if not isinstance(vector, np.ndarray):
            raise TypeError("Input must be a NumPy array.")
        
        if not isinstance((vector[0]), (int, float)):
            raise TypeError(f"{vector[0]} must be an int or float")
        
        if not isinstance((vector[1]), (int, float)):
            raise TypeError(f"{vector[1]} must be an int or float")

        if not isinstance((vector[2]), (int, float)):
            raise TypeError(f"{vector[2]} must be an int or float")

        self.positions["X"] += vector[0] 
        self.positions["Y"] += vector[1]
        self.positions["Z"] += vector[2] 
        
    def rotate(self, rotation_matrix:np.ndarray) -> None:
        """ 
        Rotates the given molecule X, Y, and Z units 

        Parameters: 
            rotation_matrix(np.ndarray): 3x3 rotation matrix
        """
        if rotation_matrix.shape != (3,3):
            raise ValueError("The rotation matrix must be a 3x3 matrix")
        
        coords = self.positions[["X", "Y", "Z"]].values 
        rotated = coords @ rotation_matrix.T  #Transpose the matrix to ensure correct shape

        self.positions[["X", "Y", "Z"]] = rotated

    def scale(self, X:float, Y:float, Z:float) -> None: 
        """ 
        Scales the X, Y, Z coordintes of the given molecule

        Parameters: 
            X(float): X scale factor
            Y(float): Y scale factor
            Z(float): Z scale factor
        """
        if not isinstance((X), (int, float)):
            raise TypeError(f"{X} must be an int or float")
        
        if not isinstance((Y), (int, float)):
            raise TypeError(f"{Y} must be an int or float")

        if not isinstance((Z), (int, float)):
            raise TypeError(f"{Z} must be an int or float")
                
        self.positions["X"] *= X
        self.positions["Y"] *= Y
        self.positions["Z"] *= Z
    