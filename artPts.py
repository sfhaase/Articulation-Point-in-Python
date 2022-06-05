
# artPts.py

"""
  Find Articulation Points in an undirected graph.
  Articulation Points are nodes which, when removed from the graph,
    increase the number of connected regions in the graph.
  The approach works by assigning an incremental count, called the id, 
    to each node during a recursive DFS. Also assigned to each node is
    a low value, which is initially set to the same incremental count.
  If a link is found to an already visited node during a DFS, then the 
    low value is set to low[at] = min(low[at],ids[to])
  During the call back from the DFS, the low value is set to 
    low[at] = min(low[at], low[to])
  The approach causes the id at the beginning of a loop to propagate
    back through the low values in the loop.  The low value for each node
    in a loop is therefore the lowest id of any node encountered later 
    during the DFS, with emphasis on the word "later".          
  An articulation point is found during the call back from the DFS whenever 
    id[at]<=low[to]. Equality occurs when the call back reaches the 
    beginning of a loop , and at each node of a line except the node 
    at the end of the line. 
  The basic logic of detecting artPoints when id[at]<=low[to]
    works everywhere except at the root node because the root node is 
    always the beginning of a loop, or the beginning of a line.
  The root node case can be solved by counting outlinks from the root 
    during the DFS. If the number of outlinks from the root node is 
    greater than one, then the root node is an artPoint.
  The original approach kept track of the previous node during the DFS
    and counted outlinks from the root node when the previous node was
    the root node. This approach simply counts outlinks when the present 
    node is the root node, eliminating the need to keep track of the 
    previous node.

  The nodes in the graph are assumed to be numbered from 0 to n-1, and 
    the nodes should be defined in DFS order. The DFS always begins at 
    node 0, or the lowest unvisited node when disjoint graphs are present. 
    The graph is defined in terms of edges, with edges being defined 
    from each node to nodes in increasing order. To be in DFS order, 
    the first edge listed for each node should be to the next higher 
    node. Only one entry should be made for each edge, even though the 
    graph is expected to be undirected. The software makes entries in 
    the graph for both directions of each edge. The graph is transformed 
    into a directed graph by removing the reverse edge each time a 
    transition is made in the DFS. Defining the nodes and edges in 
    DFS order makes the results easier to understand because the results 
    are listed in node order. Nodes and edges can be defined in any order, 
    and the identified articulation points in the topology of the graph 
    will be correct, but the results will be difficult to understand because 
    the results are listed in node order. For an example of the confusion 
    which occurs when nodes are randomly defined throughout the graph, 
    see the results for test graph 13. The Articulation Points are 
    correctly identified, but it is tedious to follow the progression
    of the algorithm.
""" 

import networkx as nx
import matplotlib.pyplot as plt

def pause(msg=''):
    msg = msg+'cr to continue\n'
    tmp = input(msg)

# test graph 0
edgesLoopLineLoop = [
  (0,1),
  (0,2),
  (1,2),
  (2,3),
  (2,5),
  (3,4),
  (5,6),
  (5,8),
  (6,7),
  (7,8)
]

# test graph 1
edgesLoopToLoopWithSelfLinkAndIsolatedNode = [
    (0,1),
    (0,2),
    (1,2),
    (1,3),
    (2,3),
    (3,4),
    (4,5),
    (4,6),
    (5,6),
    (5,7),
    (6,7),
    (7,7)    # link to self
    #(8,)    # isolated node
]

# test graph 2
edgesLoopToLoopWithSelfLinkAndSpur = [
    (0,1),
    (0,2),
    (1,2),
    (1,3),
    (2,3),
    (3,4),
    (4,5),
    (4,6),
    (5,6),
    (5,7),
    (6,7),
    (7,7),    # link to self
    (7,8)     # spur
]

# test graph 3
# loop within a loop starting from 0
edgesLoopWithinLoop = [
  (0,1),
  (0,4),
  (0,5),
  (1,2),
  (1,5),
  (2,3),
  (3,4)
]
    
# test graph 4
# External loop on a loop with one loop starting from 0
#   and the other starting from 1
edgesLoopWithExternalLoop = [
  (0,1),
  (0,4),
  (1,2),
  (1,6),
  (2,3),
  (2,6),
  (3,4),
  (3,5),
  (6,7)
  #(8,)  #isolated node
]

# test graph 5
edgesRootSpur = [
  (0,1),
  (1,2),
  (1,3),
  (2,3),
  (3,4)
]

# test graph 6
edgesLoop = [
  (0,1),
  (0,3),
  (1,2),
  (2,3),
  (3,4)
]

# test graph 7
edgesLine = [
  (0,1),
  (1,2),
  (2,3)
]

# test graph 8
edgesSunBurst = [
  (0,1),
  (0,2),
  (0,3),
  (0,4)
]

# test graph 9
edgesBowTie = [
  (0,1),
  (0,2),
  (0,3),
  (0,4),
  (1,2),
  (3,4)
]

# test graph 10
edgesBowTie2 = [
  (0,1),
  (0,2),
  (1,2),
  (2,3),
  (2,4),
  (3,4)
]

# test graph 11
edgesBowTie3 = [
  (0,2),
  (0,3),
  (1,3),
  (1,4),
  (2,3),
  (3,4)
]

# test graph 12
edgesLoopsOnLoops = [
  (0,1),
  (0,5),
  (0,6),
  (1,2),
  (2,3),
  (2,6),
  (3,4),
  (4,5),
  (4,8),
  (6,7),
  (7,8)
]

# test graph 13
# node order not in dfs order
edgesScrambled= [  
  (0,4),
  (0,6),
  (1,5),
  (1,9),
  (2,7),
  (2,6),
  (2,8),
  (2,4),
  (3,9),
  (5,9)
]

# XXX
def gen_graphOBE(gnum):
    # Generate undirected graph as a dict from list of edges
    # Enter forward and reverse links together.
    g = {}  # graph adjacency list as a dict
    
    # clear graph
    g.clear()

    # add nodes
    for i in range(numNodes[gnum]):
        g[i] = []

    # add edges
    # will get error if node not in graph
    edges = eds[gnum]
    for i in range(len(edges)):
        fr = edges[i][0]
        to = edges[i][1]
        g[fr].append(to)
        # check for self link
        if to == fr:
            # don't enter self link twice
            continue
        g[to].append(fr)
    return g

def gen_graph(gnum):
    # Generate undirected graph as a dict from list of edges
    # Enter reverse links fter forward links.
    g = {}  # graph adjacency list as a dict
    
    # clear graph
    g.clear()

    # add nodes
    for i in range(numNodes[gnum]):
        g[i] = []

    # add edges
    # will get error if node not in graph
    edges = eds[gnum]
    for i in range(len(edges)):
        fr = edges[i][0]
        to = edges[i][1]
        g[fr].append(to)
    for i in range(len(edges)):
        fr = edges[i][1]
        to = edges[i][0]
        # check for self link
        if to == fr:
            # don't enter self link twice
            continue
        g[fr].append(to)
    return g


# XXX
def dfsArt(root,at, id, outEdgeCount):
    print("\nvisiting node ", at)
    visited[at] = True
    id += 1        # Note: Java program starts with 0 and does incr after assignment
    print("Incrementing id and setting low and ids to id = ", id)
    low[at] = id
    ids[at] = id
    
    for to in g[at]:
        if visited[to] == False:
            print("Next visit will be to node ", to)
  
            # inc outEdgeCount if at root
            if at == root:
                outEdgeCount += 1
   
            if convertToDigraph == "y":
                # remove reverse link from graph
                g[to].remove(at)
                print("removed link from ", to, " to ", at)
                print("graph is now")
                print(g)

            id, outEdgeCount = dfsArt(root, to, id, outEdgeCount)

            print("\nDuring call back, at, to, ids[at], low[to] = ", at, to, ids[at], low[to])
            if low[at] > low[to]:
                print("setting low of node to ", low[to])
            else:
                print("low of node is ", low[at])
            low[at] = min(low[at], low[to])
            
            if ids[at] < low[to]:
                print("less than case")
                print("Setting ArtPoint ")
                isArt[at] = True
            if ids[at] == low[to]:
                print("equal case")
                print("Occurs when call back reaches the beginning of a loop")
                print("Setting ArtPoint ")
                isArt[at] = True
        else:
            print("Link to visited node, at, to, ids[at], low[to] = ", at, to, ids[at], low[to])
            if low[at] > ids[to]:
                print("setting low to ", ids[to])
            else:
                print("low of node is ", low[at])
            low[at] = min(low[at],ids[to])
    return id, outEdgeCount 
    
def findArt(g):
    id = -1  # Assigns numbers from 0 to n-1 to nodes during the dfs
             #   and keeps track of the numbers in ids
    n = len(g)  # number of nodes in g
    for i in range(n):
        if visited[i] == False:
            root = i
            at = i
            outEdgeCount = 0 # Reset outEdgeCount
            id, outEdgeCount = dfsArt(root, at, id, outEdgeCount)

            # Override artPoint decision for root node based on outEdgeCount
            if outEdgeCount > 1:
                print("Setting ArtPoint to True for root node ", i, " because outEdgeCount = ", outEdgeCount)
                isArt[i] = True
            else:
                isArt[i] = False
                print("Setting Art Point to False for root node ", i, " because outEdgeCount = ", outEdgeCount)

titles = [
  "LoopLineLoop",                    # 0
  "LoopToLoopWithSelfLinkAndIsolatedNode",   # 1
  "LoopToLoopWithSelfLinkAndSpur",   # 2
  "LoopWithinLoop",                  # 3
  "LoopWithExternalLoop",            # 4
  "RootSpur",                        # 5
  "Loop",                            # 6
  "Line",                            # 7
  "SunBurst",                        # 8
  "BowTie",                          # 9
  "BowTie2",                         # 10
  "BowTie3",                         # 11
  "LoopsOnLoops",                    # 12
  "Scrambled"                        # 13
]

numNodes = [
  # Some numbers are > len(edges) to create isolated nodes
  9,  # test graph 0
  9,  # test graph 1
  9,  # test graph 2
  6,  # test graph 3
  9,  # test graph 4
  5,  # test graph 5
  5,  # test graph 6
  4,  # test graph 7
  5,  # test graph 8
  5,  # test graph 9
  5,  # test graph 10
  5,  # test graph 11
  9,  # test graph 12
  10  # test graph 13
]

eds = [
  # edges are upper diagonal of adjacency matrix
  edgesLoopLineLoop,                      # 0
  edgesLoopToLoopWithSelfLinkAndIsolatedNode,   # 1
  edgesLoopToLoopWithSelfLinkAndSpur,   # 2
  edgesLoopWithinLoop,                  # 3
  edgesLoopWithExternalLoop,            # 4
  edgesRootSpur,                        # 5
  edgesLoop,                            # 6
  edgesLine,                            # 7
  edgesSunBurst,                        # 8
  edgesBowTie,                          # 9
  edgesBowTie2,                         # 10
  edgesBowTie3,                         # 11
  edgesLoopsOnLoops,                    # 12
  edgesScrambled                        # 13
]

# ***************************************************************
# main 
# ***************************************************************

# XXX

print("\n\nThe graph is normally converted to a directed graph during the depth first search.")
convertToDigraph = input("Enter y to convert to a directed graph, n to retain both links: ")
convertToDigraph = convertToDigraph.replace(" ","")

while True:
    if convertToDigraph == "y": 
        print("Converting to Digraph")
        break
    if convertToDigraph == "n": 
        print("Retaining both links in an undirected graph to see what happens.")
        break
    convertToDigraph = input("\n\nEnter y to convert to a directed graph, n to retain both links: ")
    convertToDigraph = convertToDigraph.replace(" ","")

numGraphs = len(numNodes)
for gnum in range(numGraphs):
# for gnum in range(1,2):     # LoopToLoopWithSelfLinkAndIsolatedNode
# for gnum in range(5,6):     # Root Spur
# for gnum in range(6,7):     # Loop
# for gnum in range(7,8):     # Line
# for gnum in range(9,10):    # BowTie
# for gnum in range(13,14):    # Scrambled

    g = gen_graph(gnum)
    print("graph number ", gnum, " is ")
    print(g)
    # pause()
    
    # For each array, the array index is the node number in the graph, 
    #  assuming that the nodes are numbered from 0 to n-1.
    # ids are the sequential numbers assigned to each node during a DFS
    # ids provides the order in which the nodes were visited during a DFS
    ids = []        # sequential numbers assigned during a DFS
    low = []        # lowlink values for the nodes
    visited = []    # visited indication for all nodes
    isArt = []      # articulation point indication for all nodes
    outEdgeCount = 0
    
    # init storage
    n = len(g)   # number of nodes in graph
    for i in range(n):
        ids.append(-1)
        low.append(-1)
        visited.append(False)
        isArt.append(False)
    
    findArt(g)
    
    print("\nArticulation Point Search Done")
    print("ids is ")
    print(ids)
    print("low is ")
    print(low)
    print("isArt is ")
    print(isArt)
    
    for i in range(len(isArt)):
        if isArt[i]:
            print("artPoint at node ", i)  #  i is node number in graph
    
    
    # YYY
    # Generate networkX graph for plot
    G = nx.Graph()
    G.add_nodes_from(range(numNodes[gnum]))
    edges = eds[gnum]
    G.add_edges_from(edges) 
    
    fig = plt.figure(figsize=(5,5))
    text = "Simplified Alg:" + titles[gnum]
    fig.suptitle(text)
    ax = fig.add_subplot(1,1,1)
    text = "ArtPoints: "
    numArtPts = 0
    for i in range(len(isArt)):
        if isArt[i]:
            if numArtPts == 0:
                text += str(i)
            else:
                text += "," + str(i)
            numArtPts += 1
    if numArtPts == 0:
        text += "None"
    ax.set_title(text)
    
    nx.draw_networkx(G, node_color='cyan')
    # nx.draw(G, with_labels=True, font_weight='bold', node_color='cyan')
    text = "figs/" + titles[gnum] + ".png"
    # plt.savefig(text)
    text = "figs/" + titles[gnum] + ".jpg"
    # plt.savefig(text)

    print("i     G[i]")
    for i in G:
        print(i, G[i])

    plt.show()
    
    
    
print("Done")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
