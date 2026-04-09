#MINMAX ALGORITHM USED IN GAMING
import math
def minmax(depth,index,maxi,score,target):
    if depth==target:
        return score[index]
    if maxi:
        return max(
            minmax(depth+1,index*2,False,score,target)
            ,minmax(depth+1,index*2+1,False,score,target)
        )
    else:
        return min(
            (minmax(depth+1,index*2,True,score,target))
            ,minmax(depth+1,index*2+1,True,score,target)
            )
 #COdE FOR TESTING FUNCTION
score=[3,6,9,15,18,11,2,5]
tree=int(math.log2(len(score))) 
print("The optimal value is:",minmax(0,0,True,score,tree))
