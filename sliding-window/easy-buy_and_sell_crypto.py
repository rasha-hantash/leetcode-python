class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        res = 0
        lowest = prices[0]

        for price in prices:
            if price < lowest:
                lowest = price
            res = max(res, price - lowest)
        return res

        

'''
you have 2 variables. res, lowest

loop through prices 

and get the max profit compared to res
'''