import random
import igraph
from igraph import Graph, plot
import plotly.graph_objects as go

import Tree as t

#def leaf():
#    return 0

#def graft(t1,t2):
#    return (t1,t2)

## -----------------------
#The art of computer programming, volume 4, chapter 7, section 7.2.1.6
#def algoRemy (nb_node):
#    #start_node = 0
#    #links list
#    link = [0]
#    #internal_nodes = n-1
#    for n in range(0, nb_node):
#        x = random.randint(0, 4*n+1)
#        b = x % 2
#        k = math.floor(x/2)
#        #to set our L_(2n-b), L_(2n-1+b) et L_k... but why?
#        if len(link) < (2*n+1):
#            link.extend([None] * (2*n+1 - len(link)))
#        link[2*n-b] = 2*n
#        link[2*n-1+b] = link[k]
#        link[k] = 2*n-1
#    return link
## ----------------------

def algoCroissance(n,s_max):
    if n == 0 :
        #s = 1
        if s_max != 1:
            return TypeError("cannot find an arrangement of ", n, " nodes with ", s_max, " strahler value."), None
        return t.Tree.leaf(), 1
    if n == 1 :
        #s = 2
        if s_max != 2:
            return TypeError("cannot find an arrangement of ", n, " nodes with ", s_max, " strahler value."), None
        return t.Tree.graft(t.Tree.leaf(),t.Tree.leaf()), 2
    

    #base: tree with single node
    tree = t.Tree.graft(t.Tree.leaf(),t.Tree.leaf())
    # basically, we start at s = 2 with our basic arragement..
    #s = 2
    if s_max < 2:
        return TypeError("cannot find an arrangement of ", n, " nodes with ", s_max, " strahler value."), None
    else:
        #wikipedia: intervalles d'entiers de 2 jusqu'à n
        for k in range(2,n+1):
            tree = insert_node(tree,s_max)
            #s = strahler(tree)
            # compare s_returned with s_max to determin if we return the tree already or add more nodes
            # stoppes if s exceeds the max allowed
            if tree.strahler >= s_max:
                break
    
    return tree, tree.strahler

def insert_node(tree,s_max):    
    #get the list of unblocked leaves of the tree
    unblockedLeaves = tree.listUnblockedLeaves()

    #if no any unblocked (open) leaves, just return the current tree and s
    if not unblockedLeaves:
        return tree
    
    while unblockedLeaves:
        #randomly choose one from the unblocked (open) leaves
        edge = random.choice(unblockedLeaves)

        #add the node at the chosen open leaf
        edge.isLeaf = False     #set the chosen leaf to false because it is no longer one
        edge.left = t.Tree.leaf()
        edge.right = t.Tree.leaf()  #why not just tree = t.Tree.graft() with edge in it ?

        #tree.unblockedLeaves.append(edge.left)
        #tree.unblockedLeaves.append(edge.right)
        #tree.unblockedLeaves.remove(edge)

        edge.left.parent = edge
        edge.right.parent = edge

        #new_s = strahler(tree)
        edge.update_strahler()
        tree.numberNodes = tree.update_node_count()

        #if new_s exceeds s_max, block leaf and undo insertion
        if edge.strahler >= s_max:
            edge.block()
            unblockedLeaves.remove(edge)
            #edge.isLeaf = True
            #edge.left = None
            #edge.right = None
            #tree.unblockedLeaves.remove(edge.left)
            #tree.unblockedLeaves.remove(edge.right)
        else:
            break
    
    return tree

#def strahler ( tree ):
#    #apply basic rule
#    if tree.isLeaf :
#        return 1
#    else :
#        #recursively calculate the Strahler numbers for both branches
#        leftStrahler = strahler(tree.left)
#        rightStrahler = strahler(tree.right)
#    
#        #apply the Strahler number rules
#        if leftStrahler == rightStrahler:
#            return leftStrahler + 1
#        else:
#            return max(leftStrahler, rightStrahler)

#chat gpt suggestion
def tree_to_tuples(tree, parent_id=None, edges=None, node_counter=None, vertices=None):
    if edges is None:
        edges = []
    if node_counter is None:
        node_counter = [0]  # Mutable counter for unique IDs
    if vertices is None:
        vertices = []   # Store vertex attributes

    # Assign unique ID to the current node
    current_id = node_counter[0]
    node_counter[0] += 1

    # Add vertex attribute for isLeaf
    #vertices.append({"isLeaf": tree.isLeaf})
    vertices.append(tree)

    if parent_id is not None:
        edges.append((parent_id, current_id))

    # Traverse left and right children if they exist
    if tree.left:
        tree_to_tuples(tree.left, current_id, edges, node_counter, vertices)
    if tree.right:
        tree_to_tuples(tree.right, current_id, edges, node_counter, vertices)

    return edges, vertices

def visualize_tree(tree):
    tupleTree, vertices = tree_to_tuples(tree)
    g = Graph.TupleList(tupleTree, directed=True)
    labelLeaves(g, vertices)
    visual_style = {
        #"vertex_size": 40,
        "vertex_color": [v["color"] for v in g.vs], #"blue",
        "vertex_label": [v["strahler"] for v in g.vs],
        "vertex_label_color": "white",
        #"vertex_label_size": 20,
    }
    layout = g.layout("rt")
    igraph.plot(g,"tree_graph.png", layout=layout, **visual_style, bbox=(1000, 1000))
    print(g.summary())

def labelLeaves (g, vertices):
    for i, vertex in enumerate(g.vs):
        vertex["isLeaf"] = vertices[i].isLeaf   #["isLeaf"]
        vertex["color"] = "red" if vertex["isLeaf"] else "blue"
        vertex["strahler"] = vertices[i].strahler

def main ():
    tree, s = algoCroissance(20000,13)
    print(tree)
    print("s = ", s)
    print("n = ", tree.numberNodes)

    # Visualize the tree
    visualize_tree(tree)
    
    #------------------------------------------------
    #tree = t.Tree.graft(t.Tree.leaf(),t.Tree.leaf())
    #t1 = t.Tree.graft(tree,tree)
    #t2 = t.Tree.graft(t1,t1)
    #t2.update_strahler()
    #print(t2.strahler)

if __name__ == "__main__":
    main()