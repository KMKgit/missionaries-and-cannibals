from pyDatalog import pyDatalog
import sys, random

dx = [0, -2, -1, 0, -1]
dy = [-2, 0, -1, -1, 0]
globalNodeNum=0
pyDatalog.create_terms('X, Y, Z, P, P2, C, C2')
pyDatalog.create_terms('link, path_with_cost, shortest_path')

class State():
    def __init__(self, missionaryIn, cannibalIn, missionaryOut, cannibalOut, boat, nodeNum):
        self.missionaryIn = missionaryIn
        self.cannibalIn = cannibalIn
        self.missionaryOut = missionaryOut
        self.cannibalOut = cannibalOut
        self.boat = boat
        self.parent = None
        self.nodeNum = nodeNum
        
    def check(self):        
        if self.missionaryIn >= 0 and self.cannibalIn >= 0 and self.missionaryOut >= 0 and self.cannibalOut >= 0 and (self.missionaryIn == 0 or self.missionaryIn >= self.cannibalIn) and (self.missionaryOut == 0 or self.missionaryOut >= self.cannibalOut): return True
        else: return False

    def is_goal(self):
        if self.missionaryIn == 0 and self.cannibalIn == 0: return True
        else: return False
            
    def __eq__(self, other):
        return self.missionaryIn == other.missionaryIn and self.cannibalIn == other.cannibalIn and self.boat == other.boat and self.missionaryOut == other.missionaryOut and self.cannibalOut == other.cannibalOut

    def __hash__(self):
        return hash((self.missionaryIn, self.cannibalIn, self.missionaryOut, self.cannibalOut, self.boat))
        
def find(cur_state):
    global globalNodeNum
    child = []
    sign = 1
    if cur_state.boat == False:
        sign = -1

    for i in range(5):
        mi = cur_state.missionaryIn + dx[i] * sign
        ci = cur_state.cannibalIn + dy[i] * sign
        mo = cur_state.missionaryOut - dx[i] * sign
        co = cur_state.cannibalOut - dy[i] * sign        
        globalNodeNum += 1
        new_state = State(mi, ci, mo, co, not cur_state.boat, globalNodeNum)
        if(new_state.check()):
            new_state.parent = cur_state
            child.append(new_state)
    return child

def bfs(mi, ci):
    if(ci>mi):
        exit("Fault, There are more cannibals than missionaries.")

    init_state = State(mi, ci, 0, 0, True, 0)
    if(init_state).is_goal():
        return init_state
    queue = list()
    visited = set()
    queue.append(init_state)
    while queue:
        state = queue.pop(0)
        if state.is_goal():
            return state
        visited.add(state)
        children = find(state)        
        for child in children:
            if (child not in visited) and (child not in queue):
                queue.append(child)
                +link(state.nodeNum, child.nodeNum)          
    return None

def print_(s):
    path = []    
    path.append(s)
    p = s.parent
    while p:
        path.append(p)
        p = p.parent
    
    for state in path[::-1]:
        print (str(state.nodeNum) + "\t\t" + str(state.missionaryIn) + "\t\t" + str(state.cannibalIn) + "\t\t" + str(state.missionaryOut) + "\t\t" + str(state.cannibalOut) + "\t\t" + str(state.boat))

def main():
    ret = bfs(int(sys.argv[1]), int(sys.argv[2]))
    if(ret is None): exit("no solution")

    (path_with_cost(X,Y,P,C)) <= (path_with_cost(X,Z,P2,C2)) & link(Z,Y) & (X!=Y) & (X._not_in(P2)) & (Y._not_in(P2)) & (P==P2+[Z]) & (C==C2+1) 
    (path_with_cost(X,Y,P,C)) <= link(X,Y) & (P==[]) & (C==0)
    (shortest_path[X,Y]==min_(P, order_by=C)) <= (path_with_cost(X,Y,P,C))
    shortest_all_path = (shortest_path[0,Y]==P).data

    print ("==========================")
    print ("shortest path(length: " + str(len(shortest_all_path[0][1])+1) + ")")
    print ("(End node number, (Node path from left to right)")
    print (shortest_all_path[0])
    print ("==========================")
    print ("details table")
    print ("node number\tmissionaryIn\tcannibalIn\tmissionaryOut\tcannibalOut\tboat\t")
    print_(ret)

if __name__ == "__main__":
    main()