from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        valueToIndexMap = {}


        for i, num in enumerate(nums):
            valueToIndexMap[num] = i 

        # nums = [2,5,5,1,0] target = 10       
        for i, num in enumerate(nums): 
            diff = target - num 
            if diff in valueToIndexMap and valueToIndexMap[diff] != i:
                return [i, valueToIndexMap[diff]]
        return None
        
