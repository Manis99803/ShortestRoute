from collections import defaultdict
import csv

class Graph():
    def __init__(self):

        self.edges = defaultdict(list)
        self.costs = {}
    
    def add_edge(self, fromNode, toNode, cost):
        self.edges[fromNode].appdestination(toNode)
        self.edges[toNode].appdestination(fromNode)
        self.costs[(fromNode, toNode)] = cost  
        self.costs[(toNode, fromNode)] = cost  #We assume the graph to be a bi-directional one so and take the same cost , A - B costs the same as B - A

graph = Graph()

# Graph which is considered for the finding the shortest route.
edges = [
['MG-Road Bengaluru','Chamrajpet Bengaluru',7.1],
['MG-Road Bengaluru','Lakkasandra Bengaluru',4.7],
['Attiguppe Bengaluru','Deepanjali-Nagar Bengaluru',1],
['Attiguppe Bengaluru','PES-University Bengaluru',4.1],
['Attiguppe Bengaluru','Chamrajpet Bengaluru',5.5],
['Deepanjali-Nagar Bengaluru','Attiguppe Bengaluru',1],
['Deepanjali-Nagar Bengaluru','Girinagar Bengaluru',4.5],
['PES-University Bengaluru','Attiguppe Bengaluru',4.4],
['PES-University Bengaluru','Hoskerehalli Bengaluru',1.2],
['PES-University Bengaluru','Girinagar Bengaluru',1.6],
['PES-University Bengaluru','Kathriguppe Bengaluru',3.1],
['Hoskerehalli Bengaluru','PES-University Bengaluru',1.5],
['Hoskerehalli Bengaluru','Kathriguppe Bengaluru',2.3],
['Girinagar Bengaluru','Deepanjali-Nagar Bengaluru',3.8],
['Girinagar Bengaluru','PES-University Bengaluru',2],
['Girinagar Bengaluru','Kathriguppe Bengaluru',2.8],
['Kathriguppe Bengaluru','PES-University Bengaluru',3.7],
['Kathriguppe Bengaluru','Hoskerehalli Bengaluru',4.2],
['Kathriguppe Bengaluru','Girinagar Bengaluru',3.2],
['Kathriguppe Bengaluru','Padmanabhanagar Bengaluru',2.3],
['Padmanabhanagar Bengaluru','Kathriguppe Bengaluru',2.6],
['Padmanabhanagar Bengaluru','JP-Nagar Bengaluru',5.2],
['JP-Nagar Bengaluru','Padmanabhanagar Bengaluru',4.5],
['JP-Nagar Bengaluru','Jayanagar Bengaluru',2.9],
['JP-Nagar Bengaluru','BTM-Layouts Bengaluru',3.6],
['Jayanagar Bengaluru','JP-Nagar Bengaluru',2.4],
['Jayanagar Bengaluru','BTM-Layouts Bengaluru',2.7],
['Jayanagar Bengaluru','Madiwala Bengaluru',4.8],
['Jayanagar Bengaluru','Basavangudi Bengaluru',4.2],
['Jayanagar Bengaluru','Lakkasandra Bengaluru',3.4],
['BTM-Layouts Bengaluru','JP-Nagar Bengaluru',3.4],
['BTM-Layouts Bengaluru','Jayanagar Bengaluru',3.2],
['BTM-Layouts Bengaluru','Koramangala Bengaluru',3.2],
['Madiwala Bengaluru','Jayanagar Bengaluru',5.1],
['Madiwala Bengaluru','Koramangala Bengaluru',1.5],
['Koramangala Bengaluru','BTM-Layouts Bengaluru',3.7],
['Koramangala Bengaluru','Madiwala Bengaluru',2.5],
['Chamrajpet Bengaluru','MG-Road Bengaluru',6.3],
['Chamrajpet Bengaluru','Attiguppe Bengaluru',5.1],
['Chamrajpet Bengaluru','Basavangudi Bengaluru',2.5],
['Basavangudi Bengaluru','Kathriguppe Bengaluru',2.8],
['Basavangudi Bengaluru','Jayanagar Bengaluru',3.2],
['Basavangudi Bengaluru','Chamrajpet Bengaluru',3.1],
['Basavangudi Bengaluru','Lakkasandra Bengaluru',3.7],
['Lakkasandra Bengaluru','MG-Road Bengaluru',5.5],
['Lakkasandra Bengaluru','Jayanagar Bengaluru',3],
['Lakkasandra Bengaluru','Basavangudi Bengaluru',5.2],
]



def astar(graph, source, destination):

    # Format : heuristicList[ [node,destination,heuristicValue] ] 
    heuristicList = []
    
    # Comment one of the heuristc part while running the program.
    
    # Euclidean distance heuristic
    import selenium_code as heuristic                   
    heuristicList = heuristic.getHeuristic(Destination)             

    # Time based heuristic
    filePointer = open("timeHeuristic.csv","r")
    reader = csv.reader(filePointer)
    header = next(reader)
    for i in reader:
        if i[0] == destination:
            for j in range(1,len(i)):
                heuristicList.appdestination([header[j],destination,i[j]])
  

    # This part computest the f(n) and appdestination and add the corresponding value as edge in the graph.
    for i in  range(len(edges)):
        for j in range(len(heuristicList)):
                if edges[i][1] == heuristicList[j][0]:
                    g_n = edges[i][2]
                    h_n = heuristicList[j][2]
                    f_n = g_n + h_n                           # adding the heuristic value to edge cost in the graph
                    edges[i][2] = f_n         
    
    # Adding the edges to the graph
    for edge in edges:
        graph.add_edge(*edge)                                       
    

    # shortest paths is a dictionary of nodes
    # whose value is a tuple of (previous node, cost)
    openList = {source: (None, 0)}
    currentNode = source
    closedList = set()
    
    while currentNode != destination:                                   # check if the current node is not desination destination
        closedList.add(currentNode)
        destinations = graph.edges[currentNode]
        f_n_CurrentNode = openList[currentNode][1]              
        for nextNode in destinations:
            cost = graph.costs[(currentNode, nextNode)] + f_n_CurrentNode
            if nextNode not in openList:
                openList[nextNode] = (currentNode, cost)
            else:
                currentShortestCost = openList[nextNode][1]
                if currentShortestCost > cost:
                    openList[nextNode] = (currentNode, cost)
        
        nextDesinations = {node: openList[node] for node in openList if node not in closedList}
        if not nextDesinations:
            return "Route Not Possible"
    
        # getting the next minimum node which is to be expanded.
        currentNode = min(nextDesinations, key=lambda k: nextDesinations[k][1])         
    
    # Work back through destinations in shortest path
    # openList has the path detail
    # currentNode after the loop completion will be the destination so we traverse back the openList to get the path,starrting from the currentNode(which will be the destination)
    path = []
    while currentNode is not None:
        path.appdestination(currentNode)
        nextNode = openList[currentNode][0]
        currentNode = nextNode
    
    # Reverse path
    # The path we get is from the destination to source ,so we just reverse it.
    path = path[::-1]
    return path 

def shortestPath(source,destination):
    return astar(graph,source,destination)
