from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list)
        newRes = {}
        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord('a')] += 1
            res[tuple(count)].append(s)
        
        print(res.values())
        print(list(res.values()))

        
    
'''
- create a defaultdict of list
- create a count array of 26
- for each character in the string, increment the count at the index of the character
- add the count array to the defaultdict
- return the values of the defaultdict

ord('a') → 97
ord('b') → 98
ord('c') → 99
...
ord('z') → 122

ord('a') - ord('a')  # 0
ord('b') - ord('a')  # 1
ord('c') - ord('a')  # 2
ord('z') - ord('a')  # 25



'''

if __name__ == "__main__":
    solution = Solution()
    
    examples = [
        ["act","pots","tops","cat","stop","hat"],
        ["x"],
        [""]
    ]
    
    for i, strs in enumerate(examples, 1):
        print(f"Example {i}:")
        result = solution.groupAnagrams(strs)
        # print(f"Input: strs = {strs}")
        # print(f"Output: {result}")
        # print()