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
a stack that has list of beginning symbols 

hashmap that maps ending symbols to beginning symbols 

return a statement around if stack is empty -> return not stack 

core logic: if the last element in the stack is the same is Map[c] the pop it and ensure stack is not empty to handle a case of "]"
'''