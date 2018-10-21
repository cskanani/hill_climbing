'''
run code as follows:
python3 hill_climbing.py file_name_where_input_is_stored

Input file format:
start_state_comma_saperated
goal_state_comma_saperated

'''
import queue,random,sys,time,random
expn = [] #list to store explored nodes
mvs = [] #list to store moves from root to goal
nsml = 10 #number of side moves limit, for paltue situations
nsm = 0 #for counting no of side moves
rrl = 100 #random restart limit
rr = 0 #for counting no of random restarts
nexp = 0 #number of nodes explored
nvis = 0 #number of nodes expanded
htyp = '' #hueristics type m = Manhatan, d = Displaced tiles, o = Over-estimated, any other for Zero hueristics
fn = sys.argv[1] 
time_e = 0 #for measuring time

with open(fn,'r') as fno:
    sarr = [int(x) for x in fno.readline()[:-1].split(',')]
    goal = [int(x) for x in fno.readline()[:-1].split(',')]

#function for moving tile
def mv_u(p):
    arr=p.arr.copy()
    zi = arr.index(0)
    if(zi in [0,1,2]):
        return None
    else:
        arr[zi],arr[zi-3] =  arr[zi-3],arr[zi]
        return Node(p,arr,'u')
        
def mv_d(p):
    arr=p.arr.copy()
    zi = arr.index(0)
    if(zi in [6,7,8]):
        return None
    else:
        arr[zi],arr[zi+3] =  arr[zi+3],arr[zi]
        return Node(p,arr,'d')
        
def mv_l(p):
    arr=p.arr.copy()
    zi = arr.index(0)
    if(zi in [0,3,6]):
        return None
    else:
        arr[zi],arr[zi-1] =  arr[zi-1],arr[zi]
        return Node(p,arr,'l')
        
def mv_r(p):
    arr=p.arr.copy()
    zi = arr.index(0)
    if(zi in [2,5,8]):
        return None
    else:
        arr[zi],arr[zi+1] =  arr[zi+1],arr[zi]
        return Node(p,arr,'r')

#function for generating child-nodes
def gen_c(parent):
    global nexp,nsm,nsml
    mu = mv_u(parent)
    md = mv_d(parent)
    ml = mv_l(parent)
    mr = mv_r(parent)
    cn = None
    tl = []
    if (mu != None and mu.arr != parent.arr):
        expn.append(mu);nexp+=1
        tl.append(mu)
    if (md != None and md.arr != parent.arr):
        expn.append(md);nexp+=1
        tl.append(md)
    if (ml != None and ml.arr != parent.arr):
        expn.append(ml);nexp+=1
        tl.append(ml)
    if (mr != None and mr.arr != parent.arr):
        expn.append(mr);nexp+=1
        tl.append(mr)
    if(max(tl).h < parent.h):
        return max(tl)
    elif(max(tl).h == parent.h and nsm < nsml):
        print('taken a side move')
        nsm += 1
        return gen_c(max(tl))
    else:
        return None
    
#function for calculating different type of hueristics
def find_h(arr):
    h = 0
    if(htyp == 'm'):
        for i in range(1,9):
            pos = arr.index(i)
            x = pos//3
            y = pos%3
            posg = goal.index(i)
            xg = posg//3
            yg = posg%3
            h += abs(xg-x) + abs(yg-y)
    elif(htyp == 'm0'):
        for i in range(0,9):
            pos = arr.index(i)
            x = pos//3
            y = pos%3
            posg = goal.index(i)
            xg = posg//3
            yg = posg%3
            h += abs(xg-x) + abs(yg-y)
    elif(htyp == 'd'):
        for i in range(1,9):
            if(arr[i-1] != i): 
                h += 1
    elif(htyp == 'd0'):
        for i in range(0,9):
            if(arr[i-1] != i): 
                h += 1
    elif(htyp == 's'):
        for i in range(1,9):
            pos = arr.index(i)
            x = pos//3
            y = pos%3
            posg = goal.index(i)
            xg = posg//3
            yg = posg%3
            h += abs(xg-x) + abs(yg-y)
        for i in range(1,9):
            if(arr[i-1] != i): 
                h += 1
    elif(htyp == 's0'):
        for i in range(0,9):
            pos = arr.index(i)
            x = pos//3
            y = pos%3
            posg = goal.index(i)
            xg = posg//3
            yg = posg%3
            h += abs(xg-x) + abs(yg-y)
        for i in range(0,9):
            if(arr[i-1] != i): 
                h += 1
    else:
        print('Please try again with a valid hueristic type')
    return h

#class for creating node objects
class Node:
    def __init__(self,parent,arr,mv):
        self.parent = parent
        self.mv = mv
        self.h = find_h(arr)
        self.arr = arr
        
    def __lt__(self, other):
        return self.h < other.h
    def __eq__(self,other):
        if(other == None):
            return 0
        elif(self.arr == other.arr):
            return 1
        else:
            return 0
     
#function to run a_star algo
def run_as(m,p):
    global htyp, nmvs, nvis, rr, rrl,nsm
    rr = 0
    nexp = 0
    htyp = m
    mvs[:] = []
    
    while(True):
        nvis += 1
        if(p.arr == goal):
            while(p.parent != None):
                mvs.insert(0,p.mv)
                p = p.parent
            break
        nsm = 0
        nn = gen_c(p)
        if(nn != None):
            p = nn
        else:
            if(rr < rrl):
                rr += 1
                p = expn[random.randint(0,len(expn)-1)]
            else:
                print('unable to solve')
                break

#function for printing results data
def p_data(m):
    print('\n')
    if(htyp == 'm'):
        print('Data with Manhatan hueristics : ')
    elif(htyp == 'm0'):
        print('Data with Manhatan hueristics(0) : ')
    elif(htyp == 'd'):
        print('Data with displaced tiles hueristics : ')
    elif(htyp == 'd0'):
        print('Data with displaced tiles hueristics(0) : ')
    elif(htyp == 's'):
        print('Data with displaced tiles hueristics + Manhatan hueristics : ')
    elif(htyp == 's0'):
        print('Data with displaced tiles hueristics(0) + Manhatan hueristics(0) : ')
    else:
        print('Unable to show output! Please try again with a valid hueristic type')
    print('Number of nodes explored :',nexp)
    print('Number of nodes expanded :',nvis)
    print('Length of path :',len(mvs))
    print('Path to goal :',mvs)
    print('Time taken for execution :',time_e,'seconds')

run_l = ['m','m0','d','d0','s','s0'] #list of hueristics to run on m = Manhatan, d = Displaced tiles, o = Over-estimated, any other for Zero hueristics
s = Node(None,sarr,'') #start node
for zx in run_l:
    start = time.time()
    run_as(zx,s)
    time_e = time.time()-start
    p_data(zx)
