#import nb_nodes
import functools

@functools.cache
def generateTreesByNodes (n):
    trees = []
    if n < 0:
        return print("The nomber of nodes must be positive integer (0 or more) !")
    if n == 0:
        trees.append(0)
        return trees
    else :
        #for each n, we go in the loop, and match the left branches generated for i with the right branches generated for n-1-i
        for i in range(n):
            leftBranch = generateTreesByNodes(i)   #generateTreesByNodes returns already a list. here it will have all possible subtrees of i nodes.
            rightBranch = generateTreesByNodes(n-1-i)  #same here. it generates a list of all possible subtrees of n-1-i
            
            #here happens the matching for both branch arrangements..
            for left in leftBranch:
                for right in rightBranch:
                    trees.append((left,right))
        #test : pour voir la list de chaque branche à chaque itération
        #print("leftbranch : ", leftBranch)
    return trees

@functools.cache
def generateTreesByNodesHeight(n,h):
    trees = []
    if n < 0 or h < 0:
        return print("Height and/or nodes should be equal to or more than 0")
    if n == 0 and h == 0:
        trees.append(0)
        return trees
    if n == 0 or h == 0:
        return []

    # cas 3
    for i in range(n):
        leftBranch = generateTreesByNodesHeight(i,h-1)
        rightBranch = generateTreesByNodesHeight(n-1-i,h-1)
        
        for left in leftBranch:
            for right in rightBranch:
                trees.append((left,right))
    
    # cas 1
    for j in range(n):
        leftBranch = generateTreesByNodesHeight(j,h-1)
        for h_prime in range(h-1):
            rightBranch = generateTreesByNodesHeight(n-1-j,h_prime)
        
            for left in leftBranch:
                for right in rightBranch:
                    trees.append((left,right))
    
    # cas 2 - mirrored version of cas 1
    for k in range(n):
        rightBranch = generateTreesByNodesHeight(k,h-1)
        for h_prime in range(h-1):
            leftBranch = generateTreesByNodesHeight(n-1-k,h_prime)
        
            for left in leftBranch:
                for right in rightBranch:
                    trees.append((left,right))
    
    return trees

@functools.cache
def strahler ( t ):
    #apply basic rule
    if t == 0 :
        return 1
    else :
        leftBranch = t[0]
        rightBranch = t[1]
        #print(leftBranch)
        #print(rightBranch)
        
        #recursively calculate the Strahler numbers for both branches
        leftStrahler = strahler(leftBranch)
        rightStrahler = strahler(rightBranch)
    
        #apply the Strahler number rules
        if leftStrahler == rightStrahler:
            return leftStrahler + 1
        else:
            return max(leftStrahler, rightStrahler)

# only leaves arrangements of n nodes that have s strahler number
def nodesStrahler (n, s):
    remains = []
    originalArrangByNodes = generateTreesByNodes(n)
    for tree in originalArrangByNodes:
        if strahler(tree) == s:
            remains.append(tree)
    return remains

def nodesHeightStrahler(n,h,s):
    remains = []
    originalArrangByNodesHeight = generateTreesByNodesHeight(n,h)
    for tree in originalArrangByNodesHeight:
        if strahler(tree) == s:
            remains.append(tree)
    return remains

# produit un tableau de nombre d'arbres ayant un même nb de strahler pour le nb de noeuds donné
def nbNodesbyStrahler(n,s):
    print("n \ s |", ", ".join(str(strah) for strah in range(1,s+1)) )
    for node in range(0,n+1):
        print(node, end=" | ")
        for strahler in range(1,s+1):
            print(len(nodesStrahler(node,strahler)), end=", ")
        print("\n")

def nbNodesHeightByStrahler(n,h,s):
    for height in range(h+1):
        print("Height : ", height, "\n")
        for node in range(n+1):
            for strahler in range(1,s+1):
                print(len(nodesHeightStrahler(node,height,strahler)), end=", ")
            print("\n")
        print("-------------------------\n")


def denombrerArbresParNodesHauteur(n,h):
    # cas de base
    if (n == 0 and h == 0):
        return 1
    if (n == 0 or h == 0):
        return 0
    
    # cas 1 et 2 de la formule
    sum1 = 0
    for i in range(0,n):  
        left_trees = denombrerArbresParNodesHauteur(i, h-1)  
        sum_h_prime = sum(denombrerArbresParNodesHauteur(n-1-i, h_prime) for h_prime in range(h-1))  
        sum1 += left_trees * sum_h_prime
    sum1 *= 2

    # cas 3 de la formule
    sum2 = 0
    for i in range(0,n):
        sum2 += denombrerArbresParNodesHauteur(i, h-1) * denombrerArbresParNodesHauteur(n-1-i, h-1)
    
    # formule complète
    nombre = sum1 + sum2
    
    return nombre


def main ():
    #print("test generate tree arrangements of n nodes :")
    #t = generateTreesByNodes(4)
    #for arrangements in t:
    #    print(arrangements)
    #print(len(t))

    #print("test nb_strahler :")
    #t = (((0,0),0),(0,0))
    #print(strahler(t))

    #print("test generate arrangements of n nodes having s strahler number :")
    # list = nodesStrahler(4,3)
    # print(list)
    # print(len(list))

    nbNodesbyStrahler(6,6)
    #print(denombrerArbresParNodesHauteur(5,3))

    #print("test generate tree arrangements of n nodes and h height :")
    #t = generateTreesByNodesHeight(5,3)
    #for arrangements in t:
    #    print(arrangements)
    #print(len(t))

    #nbNodesHeightByStrahler(8,6,6)


if __name__ == "__main__":
    main()