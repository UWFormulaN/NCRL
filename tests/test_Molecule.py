import unittest
import re
import numpy as np
from ncrl import Molecule

class MolecueTest(unittest.TestCase):

    def setUp(self):

        self.name = "Propane"
        self.filePath = "tests/Resources/Propane.xyz"
        self.molecule = Molecule(self.name, self.filePath)

        self.columns = ["Atom", "X", "Y", "Z"]
        self.atomNum = 11

    def test_contructor(self):

        molecule = Molecule(self.name, self.filePath)

        self.assertIsNotNone(molecule)
        self.assertEqual(self.name, molecule.name)
        self.assertEqual(self.filePath, molecule.filePath)

        self.assertIsNotNone(molecule.positions)
        self.assertEqual(4, len(molecule.positions.columns))
        self.assertEqual("Atom", molecule.positions.columns[0])
        self.assertEqual("X", molecule.positions.columns[1])
        self.assertEqual("Y", molecule.positions.columns[2])
        self.assertEqual("Z", molecule.positions.columns[3])
        self.assertEqual(self.atomNum, len(molecule.positions["Atom"]))

    def test_constructor_error(self):

        with self.assertRaises(TypeError):
            Molecule(1, self.filePath)

        with self.assertRaises(TypeError):
            Molecule(self.name, 1)

        with self.assertRaises(ValueError):
            Molecule("", self.filePath)

        with self.assertRaises(ValueError):
            Molecule(self.name, "")

        with self.assertRaises(ValueError):
            Molecule(" ", self.filePath)

        with self.assertRaises(ValueError):
            Molecule(self.name, " ")

        with self.assertRaises(FileNotFoundError):
            Molecule(self.name, "nonExistantFile.xyz")

    def test_getContent(self):

        molecule = Molecule(self.name, self.filePath)
        positions = molecule.getContent()
        lines = positions.split("\n")

        self.assertEqual(self.atomNum, len(lines))

        pattern = re.compile(
            r"^[A-Z][a-z]?\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+$"
        )

        for line in lines:
            self.assertRegex(line.strip(), pattern)
    
    def test_translate(self):
        """ 
        Asserts if the method returns the intended output based on the test values
        Note: np.allclose is used due to the inpredictability of float rounding
        """
        inital_positions = self.molecule.positions.copy()
        self.molecule.translate(np.array([1.0, -1.0, 2.0])) 
        self.assertTrue(np.allclose(self.molecule.positions["X"].values, inital_positions["X"].values + 1.0))
        self.assertTrue(np.allclose(self.molecule.positions["Y"].values, inital_positions["Y"].values - 1.0))
        self.assertTrue(np.allclose(self.molecule.positions["Z"].values, inital_positions["Z"].values + 2.0))

    def test_translate_invalid(self):
        """ 
        Checks if the invalid inputs are properly being catched with the TypeError
        """
        with self.assertRaises(TypeError):
            self.molecule.translate(np.array(["", -1.0, 2.0]))
        with self.assertRaises(TypeError):
            self.molecule.translate(np.array([1.0, "a", 2.0]))
        with self.assertRaises(TypeError):
            self.molecule.translate(np.array([1.0, -1.0, " "]))

    def test_rotate(self): 
        """ 
        Asserts if the method returns the intended output based on the test values
        Note: In this an identity matrix is used because it is easiest to test, as it should not change the output
        Note: np.allclose is used due to the inpredictability of float rounding
        """
        inital_positions = self.molecule.positions.copy()
        rotation_matrix = np.eye(3) #Identity matrix 
        self.molecule.rotate(rotation_matrix)
        self.assertTrue(np.allclose(self.molecule.positions[["X", "Y", "Z"]], inital_positions[["X", "Y", "Z"]]))

    def test_rotate_invalid(self):
        """ 
        Checks if the invalid inputs are properly being catched with the ValueError
        Note: In this case, an illogical shape is entered (you cannot do matrix vector product between a 2x2 matrix and 3D vector)
        """
        with self.assertRaises(ValueError):
            self.molecule.rotate(np.ones((2, 2))) #tests for invalid shape

    def test_scale(self):
        """ 
        Asserts if the method returns the intended output based on the test values
        Note: np.allclose is used due to the inpredictability of float rounding
        """
        inital_positions = self.molecule.positions.copy()
        self.molecule.scale(2.0, 3.0, 4.0) 
        self.assertTrue(np.allclose(self.molecule.positions["X"].values, inital_positions["X"].values * 2.0))
        self.assertTrue(np.allclose(self.molecule.positions["Y"].values, inital_positions["Y"].values * 3.0))
        self.assertTrue(np.allclose(self.molecule.positions["Z"].values, inital_positions["Z"].values * 4.0))

    def test_scale_invalid(self):
        """ 
        Checks if the invalid inputs are properly being catched with the TypeError
        """
        with self.assertRaises(TypeError):
            self.molecule.scale("", 2.0, 3.0)
        with self.assertRaises(TypeError):
            self.molecule.scale(1.0, "a", 3.0)
        with self.assertRaises(TypeError):
            self.molecule.scale(1.0, 2.0, " ")

