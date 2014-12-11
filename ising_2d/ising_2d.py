"""Simulate a 12x12 Ising paramagnet."""


import random
import math
import picture


__author__ = 'simoninoc@gmail.com (Simon Lin)'


def randomCandidate(size):#generate a configuration of size*size
    playground=[]
    for i in range(size):
        playground.append([])
        for j in range (size):
            n=random.randint(0,1)
            if n==0:
                playground[i].append(1)
            else:
                playground[i].append(-1)
    return playground


def mostEnergetic(size):
    playground=[]
    for i in range(size):
        playground.append([])
        for j in range (size):
            playground[i].append(1)
    return playground


def printlist(list):#print a 2D list in letters
    for i in range(len(list)):
        row=""
        for j in range(len(list[i])):
            row+=str(list[i][j])+" "
        print(row)


def dE(configuration,i,j):
    """calculate the energy difference if flipping s(i,j)"""
    size=len(configuration)
    ua,ub=i-1,j
    da,db=i+1,j
    la,lb=i,j-1
    ra,rb=i,j+1
    if i==0:
        ua=size-1
    if i==size-1:
        da=0
    if j==0:
        lb=size-1
    if j==size-1:
        rb=0
    upNeighbour=configuration[ua][ub]
    downNeighbour=configuration[da][db]
    leftNeighbour=configuration[la][lb]
    rightNeighbour=configuration[ra][rb]
    deltaE=2*(configuration[i][j])*(upNeighbour+downNeighbour+leftNeighbour+rightNeighbour)
    return deltaE


def main():
    n=eval(input("What's the size?"))
    T=eval(input("Temperature"))
    m=eval(input("How many steps?"))
    a=eval(input("Which candidate do you want to start with? 1, Random candidate 2, most energetic candidate "))
    if a==1:
        list=randomCandidate(n)
    elif a==2:
        list=mostEnergetic(n)
    canvas=module1.Picture(n*10,n*10)
    canvas.setFillColor(0,0,0)
    tiles=[]
    for i in range(len(list)):
        tiles.append([])
        for j in range(len(list[i])):
            tiles[i].append(" ")
    for i in range(len(list)):
        for j in range(len(list[i])):
            tiles[i][j]=canvas.drawRectFill(i*10,j*10,50,50)
    for i in range(len(list)):
        for j in range(len(list[i])):
            if list[i][j]==1:
                tiles[i][j].changeFillColor((255,255,255))
    canvas.display()

    #a candidate has already been constructed
    #BEGIN THE MARCOV CHAIN
    for i in range(m*(n^2)):
        print("Step"+str(i))
        row=random.randint(0,n-1)
        col=random.randint(0,n-1)
        deltaE=dE(list,row,col)
        print("delta E = "+str(deltaE))
        if deltaE<=0:
            if list[row][col]==1:
                list[row][col]==-1
                tiles[row][col].changeFillColor((0,0,0))
            else:
                list[row][col]==1
                tiles[row][col].changeFillColor((255,255,255))
        else:
            rand=random.uniform(0,1)
            if rand<math.exp(-deltaE/T):
                print(math.exp(-deltaE/T))
                if list[row][col]==1:
                    list[row][col]==-1
                    tiles[row][col].changeFillColor((0,0,0))
                else:
                    list[row][col]==1
                    tiles[row][col].changeFillColor((255,255,255))
        canvas.display()


if __name__ == '__main__':
    main()
