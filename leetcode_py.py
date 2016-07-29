# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 21:25:52 2016

@author: val
"""

class Solution(object):
    def reverseString(self, s):
        """
        :type s: str
        :rtype: str
        """
#        return''.join(reversed(s))
#        return ''.join((s[i] for i in xrange(len(s)-1, -1, -1)))
        return s[::-1]
    def getSum(self, a, b):
        """
        :type a: int
        :type b: int
        :rtype: int
        """
        return a+b
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        m=0
        z=[]
        for (x,y) in zip(l1,l2):
            k=(x+y+m)%10
            m=(x+y+m)/10
            z.append(k)
        return z
    def isUgly(self, num):
        """
        :type num: int
        :rtype: bool
        """
        if num<=0:
            return False
        while True:
            if num%2==0:
                num/=2
                continue
            if num%3==0:
                num/=3
                continue
            if num%5==0:
                num/=5
                continue
            if num==1:
                return True
            else:
                return False
    def isHappy(self, n):
        """
        :type n: int
        :rtype: bool
        """
        z=[]
        while True:
            if n in z:return False
            z.append(n)
            if n==1:
                return True
            n=sum(map(lambda x:int(x)**2,str(n)))
    def reverse(self, x):
        import sys
        """
        :type x: int
        :rtype: int
        """
        if int(str(abs(x))[::-1])>sys.maxint:
            return 0
        if x<0:
            return int('-'+str(-x)[::-1])
        else:
            return int(str(x)[::-1])
    def climbStairs(self, n):
        """
        :type n: int
        :rtype: int
        """
        if n==1 or n==2:
            return n
        return Solution().climbStairs(n-1)+Solution().climbStairs(n-2)      
         
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
