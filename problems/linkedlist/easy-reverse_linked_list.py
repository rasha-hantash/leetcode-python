# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev, curr = None, head

        while curr: 
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev 
        

'''
nxt = 1 (nxt.next = 2)
prev = null 
curr = 1 
curr.next = 2 


(next iteration)

prev = 1
curr = 2
curr.next = 3


essentially you want every .next pointer to point to the prev variable 
'''