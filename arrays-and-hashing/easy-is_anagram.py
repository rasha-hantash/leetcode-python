class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        dictS = {}
        dictT = {}

        for i in range(len(s)):
            dictS[s[i]] = 1 + dictS.get(s[i], 0)
            dictT[t[i]] = 1 + dictT.get(t[i], 0)
        return dictS == dictT
'''
dictS.get(s[i], 0) -> returns a default value of 0 
if the key is not there

ensure the length is the same 

create two dicts

'''
        