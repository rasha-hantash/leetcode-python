class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        hashset = set()
        for num in nums:
            if num in hashset:
                return True
            hashset.add(num)
        return False

# sorting takes 
    # O(nlogn) time 
# hashset 
    # O(n) time 
    # O(n) space complexity because of the hashset
# hashmap
    #   they are like hashset but they store the count of the elements. 
    #   the key value pairs do not allow for duplicate keys