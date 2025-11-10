import importlib.util
import pathlib
import unittest


ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT_DIR / "arrays-and-hashing" / "two-sum.py"
SPEC = importlib.util.spec_from_file_location("two_sum", MODULE_PATH)
two_sum_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(two_sum_module)
Solution = two_sum_module.Solution


class TestTwoSum(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_returns_indices_for_basic_case(self):
        nums = [2, 7, 11, 15]
        target = 9

        result = self.solution.twoSum(nums, target)

        self.assertCountEqual(result, [0, 1])

    def test_handles_duplicate_values(self):
        nums = [3, 3]
        target = 6

        result = self.solution.twoSum(nums, target)

        self.assertCountEqual(result, [0, 1])

    def test_uses_distinct_indices_with_duplicate_values(self):
        nums = [3, 2, 4]
        target = 6

        result = self.solution.twoSum(nums, target)

        self.assertCountEqual(result, [1, 2])

    def test_supports_negative_numbers(self):
        nums = [-1, -2, -3, -4, -5]
        target = -8

        result = self.solution.twoSum(nums, target)

        self.assertCountEqual(result, [2, 4])

    def test_supports_zero_values(self):
        nums = [0, 4, 3, 0]
        target = 0

        result = self.solution.twoSum(nums, target)

        self.assertCountEqual(result, [0, 3])

    def test_returns_none_when_no_solution_exists(self):
        nums = [1, 2, 3]
        target = 7

        result = self.solution.twoSum(nums, target)

        self.assertIsNone(result)

    def test_minimum_length_input(self):
        nums = [1, 2]
        target = 3

        result = self.solution.twoSum(nums, target)

        self.assertCountEqual(result, [0, 1])


if __name__ == "__main__":
    unittest.main()

