#!/usr/bin/python
from collections import namedtuple
import time
import sys

class Edge:
    def __init__(self, origin=None, destination=None, corig=None, cdest=0, weight=0):
        self.origin = origin        # write appropriate value
        self.destination = destination
        self.codeOrig = corig
        self.codeDest = cdest
        self.weight = weight        # write appropriate value

    def __hash__(self):
        # The hash of the edge is computed based on origin and destination
        return hash((self.origin, self.destination))

    def __repr__(self):
        return "edge: {0} {1} {2}".format(self.origin, self.destination, self.weight)
        
    ## write rest of code that you need for this class
 
class Airport:
    def __init__ (self, iden=None, name=None, pageRank=0):
        self.code = iden
        self.name = name
        self.routesIn = []
        self.routeHash = dict()
        self.outweight = 0 
        self.pageRank = pageRank

    def __repr__(self):
        return f"{self.code} \t {self.pageRank}"
        #{self.pageIndex}

    #self.routeHash[(origin, destination)] = edge

edgeList = []           # list of Edge
edgeHash = dict()       # hash of edge to ease the match
airportList = []        # list of Airport
airportHash = dict()    # hash key IATA code -> Airport

def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r", encoding="utf-8")
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print(f"There were {cont} Airports with IATA code")


def readRoutes(fd):
    print("Reading Routes file from routes.txt")
    routesTxt = open("routes.txt", "r", encoding="utf-8")
    for line in routesTxt.readlines():
        r = Edge()
        try:
            temp = line.split(',')
            if (len(temp[2]) != 3 or len(temp[4]) != 3):
                raise Exception('not an IATA code of origin or destination')
            r.origin = temp[3][:]
            r.destination = temp[5][:]
            r.codeOrig = temp[2][:]
            r.codeDest = temp[4][:]
        except Exception as inst:
            pass
        else:
            key = hash((r.origin, r.destination))
           
            if key in edgeHash:
                edgeHash[key].weight += 1
            else:
                r.weight = 1
                edgeHash[key] = r
            edgeList.append(r)
            if r.codeOrig in airportHash.keys() and r.codeDest in airportHash.keys():
                airportHash[r.codeOrig].outweight += 1
                airportHash[r.codeDest].routesIn.append(r)
                if key in airportHash[r.codeDest].routeHash:
                    airportHash[r.codeDest].routeHash[key] = edgeHash[key]
                else:
                    airportHash[r.codeDest].routeHash[key] = r
    routesTxt.close()

def computePageRanks():
    n = len(airportHash)  
    P = [1 / n] * n      
    L = 0.85     #dumping factor         
    teleportation = (1 - L) / n  
    maxIterations = 400   
    epsilon = 1e-8        

    # Map airport codes to indices for PageRank calculation
    codeToIndex = {code: idx for idx, code in enumerate(airportHash)}
    indexToCode = {idx: code for code, idx in codeToIndex.items()}

    it = 0
    while it < maxIterations:
        Q = [0] * n  
        for code, airport in airportHash.items():
            i = codeToIndex[code]             
            rankSum = 0
            for key, edge in airport.routeHash.items():
                j = codeToIndex[edge.codeOrig]  
                outWeight = airportHash[edge.codeOrig].outweight  
                if outWeight > 0:
                    rankSum += P[j] * edge.weight / outWeight

            Q[i] = teleportation + L * rankSum

        totalSum = sum(Q)
        if totalSum > 0:
            Q = [value / totalSum for value in Q]
        
        maxDiff = sum(abs(Q[i] - P[i]) for i in range(n))
        P = Q  
        it += 1
        
        # Convergence check
        if maxDiff < epsilon:
            break

    for code, airport in airportHash.items():
        airport.pageRank = P[codeToIndex[code]]

    return it  

def outputPageRanks():
    sortedAirports = sorted(airportHash.values(), key=lambda a: a.pageRank, reverse=True)
    s = 0
    for airport in sortedAirports:
        s += airport.pageRank
        print(airport)
    print(s)

def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    #print(airportList)
    #print(edgeHash)
    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2-time1)

if __name__ == "__main__":
    sys.exit(main())
