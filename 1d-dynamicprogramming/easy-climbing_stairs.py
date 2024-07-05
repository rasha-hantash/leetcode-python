class Solution:
    def climbStairs(self, n: int) -> int:
        n1, n2 = 1,1
        for i in range(1, n):
            n1, n2 = n2, n1 + n2

        return n2

'''
todo: look up pro's of dynamic programming later

use a decision tree to try to visualize the problem 

if number exceeds n then return 0, 
if number == n return 1

you often are running into the same numbers, 
so you should store it in cache


doing depth first search 
Becomes O(n) because you are only solving 1 sub problem once 

Using memoization by caching the result


Bottom up dynamic programming approach by starting at the base case 

'''