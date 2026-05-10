
# Find the length of the longest subarray with the same value in each position 
def longestSubarrayTwoPointers(nums) -> int:
    # Note this is solved using two pointers, not using a sliding window
    longestSubarray = 0

    l,r = 0,0

    while r < len(nums): 
        if nums[l] != nums[r]: 
            # you can immediately set it to the right pointer because 
            # you already know all previous values were duplicates 
            l = r
            continue
        longestSubarray = max(longestSubarray, r - l + 1)
        r += 1
    return longestSubarray


# print(longestSubarrayTwoPointers([4,2,2,3,3,3]))
# print(longestSubarrayTwoPointers([1,1,1,1,1]))
# print(longestSubarrayTwoPointers([1,2,3,4,5]))


def longestSubarraySlidingWindow(nums) -> int:
    windowSet = set() 
    longestLength = 0

    for num in nums: 
        if num in windowSet: 
            windowSet.add(num)
        else: 
            longestLength = max(longestLength, len(windowSet))
            windowSet = set()
    return longestLength

print(longestSubarraySlidingWindow([4,2,2,3,3,3]))
print(longestSubarraySlidingWindow([1,1,1,1,1]))
print(longestSubarraySlidingWindow([1,2,3,4,5]))


