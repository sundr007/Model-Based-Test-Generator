from copy import deepcopy as copy

class CPP:
	def __init__(self,N):
		self.N=N
		if self.N <= 0:
			print('Graph is empty')
			exit()
		self.delta=[0]*N
		self.defined=[[False]*N for _ in range(N)]
		self.label=[[[]]*N for _ in range(N)]
		self.c=[[0]*N for _ in range(N)]
		self.f=[[0]*N for _ in range(N)]
		self.arcs=[[0]*N for _ in range(N)]
		self.cheapestLabel=[['']*N for _ in range(N)]
		self.path=[[0]*N for _ in range(N)]
		self.basicCost=0	
		self.neg=list()
		self.pos=list()
		self.NONE=-1
	
	def solve(self):
		print('CPP - least cost paths')
		self.leastCostPaths()
		print('CPP - check valid')
		if not self.checkValid():
			return False
		print('CPP - Find unbalanced')
		self.findUnbalanced()
		print('CPP - Find feasible')
		self.findFeasible()
		print('CPP - Improvements')
		passes = 100
		while self.improvements() and passes>0:
			passes = passes - 1
		return True
	
	def addArc(self, lab, u, v, cost):
		if not self.defined[u][v]:
			self.label[u][v] = list()
		self.label[u][v].append(lab)
		self.basicCost += cost
		if not self.defined[u][v] or self.c[u][v] > cost :
			self.c[u][v] = cost
			self.cheapestLabel[u][v] = lab
			self.defined[u][v]=True
			self.path[u][v] = v
		self.arcs[u][v] += 1
		self.delta[u]+=1
		self.delta[v]-=1
	
	def leastCostPaths(self):
		for k in range(self.N):
			for i in range(self.N):
				if self.defined[i][k]:
					for j in range(self.N):
						if self.defined[k][j] and (not self.defined[i][j]or self.c[i][j] > self.c[i][k]+self.c[k][j]):
							self.path[i][j] = self.path[i][k]
							self.c[i][j] = self.c[i][k]+self.c[k][j]
							self.defined[i][j] = True
							if i == j and self.c[i][j] < 0: 
								return # stop on negative cycle

	def checkValid(self):
		for i in range(self.N):
			for j in range(self.N):
				if not self.defined[i][j]:
					print("Graph is not strongly connected")
					return False
			if( self.c[i][j] < 0):
				print("Graph has a negative cycle")
		return True
	
	def findUnbalanced(self):
		nn = 0 # number of vertices of negative delta
		np = 0 # number of vertices of positive delta
		for i in range(self.N):
			if self.delta[i] < 0:
				nn+=1
			elif self.delta[i] > 0:
				np+=1
		self.neg = [0]*nn
		self.pos = [0]*np
		nn = 0
		np = 0
		for i in range(self.N): # initialise sets
			if self.delta[i] < 0: 
				self.neg[nn] = i
				nn+=1
			elif self.delta[i] > 0: 
				self.pos[np] = i
				np+=1

	def findFeasible(self):
# delete next line to be faster, but non-reentrant
		delta = copy(self.delta)
			
		for u in range(len(self.neg)):
			i = self.neg[u]
			for v in range(len(self.pos)):
				j = self.pos[v]
				self.f[i][j] = -delta[i] if -delta[i] < delta[j] else delta[j];
				delta[i] += self.f[i][j]
				delta[j] -= self.f[i][j];	
				
	def improvements(self):
		residual = CPP(self.N)
		for u in range(len(self.neg)):	
			i = self.neg[u]
			for v in range(len(self.pos)):
				j = self.pos[v]
				residual.addArc('a', i, j, self.c[i][j])
				if self.f[i][j] != 0:
					residual.addArc('a', j, i, -self.c[i][j])

		residual.leastCostPaths(); # find a negative cycle
		for i in range(self.N):
			if residual.c[i][i] < 0: # cancel the cycle (if any)
				k = 0
				kunset = True
				u = i 
				while True: # find k to cancel
					v = residual.path[u][i]
					if (residual.c[u][v] < 0 and (kunset or k > self.f[v][u])):
						k = self.f[v][u]
						kunset = False
					u = v
					if u == i:
						break
				u = i 
				while True: # cancel k along the cycle
					v = residual.path[u][i]
					if residual.c[u][v] < 0:
						self.f[v][u] -= k
					else: 
						self.f[u][v] += k
					u = v
					if u == i:
						break
				return True; # have another go
		return False; # no improvements found

	def cost(self):
		return self.basicCost+self.phi()

	def phi(self):
		phi = 0
		for i in range(self.N):
			for j in range(self.N):
				phi += self.c[i][j]*self.f[i][j]
		return phi
				
	
				
	def findPath(self, start, f): # find a path between unbalanced vertices
		for i in range(self.N):
			if f[start][i]>0:
				return i
		return self.NONE
		
	def printCPT(self, startVertex):
		v = startVertex
# delete next 2 lines to be faster, but non-reentrant
		arcs = copy(self.arcs)
		f	 = copy(self.f)
		Procedure = list()
		while True:
			u = v
			v = self.findPath(u, f)
			if v != self.NONE:
				f[u][v]-=1 # remove path
				while True: # break down path into its arcs
					if u == v:
						break
					p = self.path[u][v]
					# print("Take arc "+str(self.cheapestLabel[u][p])+" from "+str(u)+" to "+str(p))
					Procedure.append((u,p,self.cheapestLabel[u][p]))
					u = p
			else:
				bridgeVertex = self.path[u][startVertex]
				if arcs[u][bridgeVertex] == 0:
					break # finished if bridge already used
				v = bridgeVertex
				for i in range(self.N): # find an unused arc, using bridge last
					if( i != bridgeVertex and arcs[u][i] > 0):
						v = i
						break
				arcs[u][v]-=1 # decrement count of parallel arcs
				# print("Take arc "+str(self.label[u][v][arcs[u][v]])+" from "+str(u)+" to "+str(v)) # use each arc label in turn
				Procedure.append((u,v,self.label[u][v][arcs[u][v]]))
		return Procedure

# ============================================
# Main Program
# ============================================

# G = CPP(4)
# G.addArc("a",0,1,1)
# G.addArc("b",0,2,1)
# G.addArc("c",1,2,1)
# G.addArc("d",1,3,1)
# G.addArc("e",2,3,1)
# G.addArc("f",3,0,1)
# G.solve()

# G.printCPT(0)
# print('cost = %s'%G.cost())