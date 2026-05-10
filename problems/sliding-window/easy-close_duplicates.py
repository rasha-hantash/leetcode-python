def close_duplicates(nums, k):
    window = set()
    l = 0
    for r in range(len(nums)):
        # you need to add 1 to the window size because the window is 0-indexed
        # k = 3 means window size of 0-2 index elements
        if r - l + 1 > k:   
            window.remove(nums[l])
            l += 1
        if nums[r] in window:
            return True
        window.add(nums[r])
    return False


print(close_duplicates([1,2,3,1], 2))
print(close_duplicates([1,0,1,1], 3))


def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
    window = set()
    l = 0
    
    for r in range(len(nums)):
        # you need to add 1 to the window size because the window is 0-indexed
        # k = 3 means window size of 0-2 index elements
        if r - l > k:   
            window.remove(nums[l])
            l += 1
        if nums[r] in window:
            return True
        window.add(nums[r])
    return False

print(containsNearbyDuplicate([1,2,3,1], 2))
print(containsNearbyDuplicate([1,0,1,1], 3))
