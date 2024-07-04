class Solution:
    def isValid(self, s: str) -> bool:
        # hashmap will be used to check 
        # stack will be used to pop on or off a parenthesis 
        # if stack is empty return true 
        hashmap = {
            "]":"[",
            ")":"(",
            "}":"{"
        }
        stack = [] 
        for c in s:
            if c not in hashmap:
                stack.append(c)
                continue
            if not stack or stack[-1] != hashmap[c]:
                return False
            stack.pop()
        return not stack


'''
hashmap with contain a k,v pair of ending symbol -> beginning symbol

stack will only contain a list of ending symbols popped onto the stack 

the program should compaire to see if the last element in stack is the same has hashmap[c]
'''