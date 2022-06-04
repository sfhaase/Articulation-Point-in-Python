# Articulation-Point-in-Python
My goal is to generate a Python program to identify Articulation Points in an undirected graph.
	I recently became interested in graph theory because of internet claims about the advantages of graph databases. I have also been involved with processing survey data from the local community using Python and Pandas. So I’ve been wondering about using Python to process graphs, which has led me to watching youtube presentations about graph theory. One of the more interesting youtube videos I have encountered is William Fiset's graph theory presentation in freeCodeCamp.org, titled “Algorithms Course – Graph Theory Tutorial from a Google Engineer”. He has obviously spent a great amount of effort and the results are really fascinating. I have seen shortest path algorithms and minimal spanning trees before, but the section on bridges and articulation points really peaked my interest, especially because it could easily be useful for looking at graph databases. His source code is implemented in Java, which I have never liked, so I decided to try implementing his pseudo code in Python. I understand what bridges and articulation points are supposed to be, but I had trouble understanding exactly what lowlink values were.  The video and the associated pdf from github indicate that the lowlink value of a node is the “smallest [lowest] id reachable from that node using forward and backward edges”. When I look at an undirected graph, it seems to me that I can reach any node I wish using forward and backward edges. My work with Python has led me to believe that the lowlink value of a node is really the lowest node reached after that node during a Depth First Search (DFS). The fact that the lowlink value of a node depends on doing a DFS puts a big constraint on the lowest node which can be reached.  If an edge is found to an already visited node during a DFS, then a loop has been found and the lowlink value of the nodes in the loop will be reduced. Otherwise, the lowlink value will remain the same as the id of the node. 

        The first issue I encountered while implementing the pseudocode was that he mentioned in the video that he transformed the graph into a directed graph. I did not understand how I was supposed to transform an undirected graph into a directed graph. The problem was that I could not see an easy way to decide whether to remove the forward link or the backward link because I could easily create a node which could not be reached during a DFS, sort of like an intersection with only oneway roads going away from the intersection. I couldn’t just remove links to lower nodes because one may be needed to detect a loop. I started by naming the nodes of a graph in an order which looked like a DFS and entered the edges from each node to nodes with larger id’s. I generated a graph as a Python dictionary and entered the edges as both forward and backward links. After some experimenting, I decided that the appropriate way to transform the graph into a directed graph was to remove the reverse link when a link was used during the DFS. 
        William Fiset kept track of the parent node during each transition of the DFS, incrementing an outEdgeCount for the root node whenever the parent was the root node. I found that keeping track of the parent node during the DFS was unnecessary. The outEdgeCount can easily be maintained by simply incrementing the count when a transition is made from the root node. The only other change I needed to make for implementing the algorithm in Python was that the id and the outEdgeCount needed to be included as parameters because Python insisted on integers in a function being local to the function. The resulting pseudocode and a python implementation are included in this repository. The python implementation includes several test cases to demonstrate that the algorithm works. 


