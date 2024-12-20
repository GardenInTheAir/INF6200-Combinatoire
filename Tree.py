class Tree:
    def __init__(self, left=None, right=None, blocked=False, isLeaf=False, parent=None): # isLeaf=True ??
        self.left = left
        self.right = right
        self.blocked = blocked
        self.isLeaf = isLeaf
        self.parent = parent
        self.strahler = 1 if self.isLeaf else 2
        self.numberNodes = 0 if self.isLeaf else 1
        #self.unblockedLeaves = [self] if isLeaf and not blocked else []


    def leaf():
        return Tree(isLeaf=True)  

    def graft(t1, t2):
        tree = Tree(left=t1, right=t2)
        t1.parent = tree
        t2.parent = tree
        tree.numberNodes = t1.numberNodes + t2.numberNodes + 1
        #tree.unblockedLeaves = t1.unblockedLeaves + t2.unblockedLeaves
        tree.update_strahler()
        return tree
    
    def update_node_count(self):
        count = 1
        if self.isLeaf:
            count += 0
        if self.left:
            count += self.left.update_node_count()
        if self.right:
            count += self.right.update_node_count()
        return count

    def update_strahler(self):
        leftStrahler = self.left.strahler if self.left else 0
        rightStrahler = self.right.strahler if self.right else 0

        if leftStrahler == rightStrahler:
            new_strahler = leftStrahler + 1
        else :
            new_strahler = max(leftStrahler,rightStrahler)
        
        if new_strahler != self.strahler:
            self.strahler = new_strahler
            if self.parent:
                self.parent.update_strahler()
            
            #with a new addition of a node, we can have a new node of a strahler s
            #and the parent node has the same strahler, but depending on the node on
            #on the other side, the parent strahler will have to change...
            #so new condition is needed ??
            #if right, check left and vise versa. if left, check right.
    
    def isBlocked(self):
        return self.blocked
    
    def block(self):
        self.blocked = True

    ### old version : error max recursion exceeded with big trees !
    # def listUnblockedLeaves(self):
    #    #if our structure is only a leaf and it is not blocked
    #    #return the leaf itself
    #    if self.isLeaf and not self.blocked:
    #        return [self]
       
    #    #recursive calls of each branch to collect its unblocked leaves across the entire tree
    #    #using `+` instead of `extend()` because of the recurssion call
    #    elif not self.isLeaf:
    #        return self.left.listUnblockedLeaves() + self.right.listUnblockedLeaves()  # Here was the source of the error ! many recursion calls with biger (deeper) trees !!
    #    return []
    
    # using stack to avoid excessive recursion !
    def listUnblockedLeaves(self):
        unblocked_leaves = []
        stack = [self]

        while stack:
            node = stack.pop()

            if node.isLeaf and not node.blocked:
                unblocked_leaves.append(node)
            elif not node.isLeaf:
                if node.left:
                    stack.append(node.left)
                if node.right:
                    stack.append(node.right)

        return unblocked_leaves
    
    def __str__(self):
        if self.isLeaf:
            return "0"
        else:
            return f"({self.left}, {self.right})"
