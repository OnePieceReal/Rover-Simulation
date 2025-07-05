import unittest
import RoverSimulation
from RoverSimulation import create_map, Rover

class TestRoverMovement(unittest.TestCase):

    def test_rover_moves_1(self):
        # case 1: Covers all areas of the map except the mines
        rover_map = create_map()
        rover_moves = "MLMMLMRRMMRMLMLMLLMM"
        new_rover = Rover(1, rover_moves, rover_map)
        new_rover.move()
        expected_moves = [['*', '1', '*'], ['*', '*', '*'], ['1', '*', '*'], ['*', '*', '*']]
        self.assertEqual(new_rover.map, expected_moves)

    def test_rover_moves_2(self):
        #case 2: Diffuses the first mine
        rover_map = create_map()
        rover_moves = "MLMLMD"
        new_rover = Rover(1, rover_moves, rover_map)
        new_rover.move()
        expected_moves = [['*', '*', '0'], ['*', '*', '0'], ['1', '0', '0'], ['0', '0', '0']]
        self.assertEqual(new_rover.map, expected_moves)

    def test_rover_moves_3(self):
        #case 3: Fails to defuse the first mine
        rover_map = create_map()
        rover_moves = "MLMLMRRMM"
        new_rover = Rover(1, rover_moves, rover_map)
        new_rover.move()
        expected_moves = [['*', '1', '0'], ['*', '*', '0'], ['1', '0', '0'], ['0', '0', '0']]
        self.assertEqual(new_rover.map, expected_moves)

    def test_rover_moves_4(self):
        # case 4: Rover ignores mine and covers approx. half of the map
        rover_map = create_map()
        rover_moves = "MLMRMMRM"
        new_rover = Rover(1, rover_moves, rover_map)
        new_rover.move()
        expected_moves = [['*', '1', '0'], ['*', '*', '0'], ['1', '*', '0'], ['*', '*', '0']]
        self.assertEqual(new_rover.map, expected_moves)

    def test_rover_moves_5(self):
        # case 4: rover cover all parts of the map (diffuses both mines, traverses parts of the map which have already been traversed)
        #Rover also attempts to move beyond the specified boundry of the map
        rover_map = create_map()
        rover_moves = "LMDMLMMRMRMRMMLMDLMMLLMLMLMRRMM"
        new_rover = Rover(1, rover_moves, rover_map)
        new_rover.move()
        expected_moves = [['*', '*', '*'], ['*', '*', '*'], ['*', '*', '*'], ['*', '*', '*']]
        self.assertEqual(new_rover.map, expected_moves)

    def test_rover_moves_6(self):
        # case 5: rover difuses the nearest mine but before diffusing the rover performs the actions 'L' and 'R'
        #before digging up the mine
        rover_map = create_map()
        rover_moves = "MLMLMLRD"
        new_rover = Rover(1, rover_moves, rover_map)
        new_rover.move()
        expected_moves = [['*', '*', '0'], ['*', '*', '0'], ['1', '0', '0'], ['0', '0', '0']]
        self.assertEqual(new_rover.map, expected_moves)


if __name__ == "__main__":
    unittest.main()
