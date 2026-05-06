class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = s.lower()
        l, r = 0, len(s) -1
        while l < r:
            while l < r and not self.alphaNum(s[l]):
                l += 1
            while l < r and not self.alphaNum(s[r]):
                r -= 1
           
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True
    
    def alphaNum(self, c) -> bool:
        return (ord('a') <= ord(c) <= ord('z') or 
                ord('0') <= ord(c) <= ord('9'))

'''
ord function gets the ascii value of a character 
'''

'''
two pointers care about the two indiviual elements that the pointers are at 

sliding window care about the entire every unique value in the window 
or about the entire sum of the window

'''