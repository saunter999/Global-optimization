#!/usr/bin/env python
from scipy import *
from pylab import *
from numpy import inf,random
from numpy import linalg as LA



class PSO:
        #-----------PSO parameters and objects---------#
	def __init__(self,pN,dim,max_iter):
	    self.w=1.0
	    self.wdamp=0.99
	    self.c1=2.0
	    self.c2=2.0
	    self.pN=pN
	    self.lb=-12.
	    self.ub=12.
	    self.dim=dim
	    self.max_iter=max_iter
	    self.X=zeros((self.pN,self.dim))     ## particle's positions and velocity 
	    self.V=zeros((self.pN,self.dim))
	    self.pbest=zeros((self.pN,self.dim)) ##particle's personal best position and the swarm's global best position 
	    self.gbest=zeros(self.dim)
	    self.p_fit=zeros(self.pN)            ## particle's personal best fit and the swarm's global best fit
	    self.g_fit=inf

	def print_info(self):
	    print "w=",self.w
	    print "pN=",self.pN
	    print "dim=",self.dim
	    print "max_iter=",self.max_iter
	    print "lb=",self.lb
	    print "ub=",self.ub

        #-----------target function---------#
	def function(self,X): ##X is local
#	    return X*sin(X)+X*cos(2*X)  
#	    return cos(14.5 * X - 0.3) + (X + 0.2) * X
#	    return X**2-4*X+3  
 	    return (X**2-5*X)*sin(X) 
#	    return LA.norm(X)**2
#	    return (X[0]**2+X[1]-11)**2+(X[0]+X[1]**2-7)**2

        #-----------PSO objects initialization---------#
	def init_Population(self):
	    for i in range(self.pN):
	        self.X[i]=self.lb*ones(self.dim)+(self.ub-self.lb)*random.rand(self.dim)
#		print self.X[i]
		self.V[i]=random.rand(self.dim)
		self.pbest[i]=self.X[i]
		tmp=self.function(self.X[i])
		self.p_fit[i]=tmp
		if tmp<self.g_fit:
		   self.g_fit=tmp
		   self.gbest=self.X[i]
#	    print 'g_fit=',self.g_fit,self.gbest
	    

        #-------------PSO iteration-------------#
	def iterator(self):
	     gbestls=[]
	     fitness=[]
	     for i in range(self.max_iter):
	         self.w=self.w*self.wdamp
	 	 fitness.append(self.g_fit)
		 gbestls.append(self.gbest)
		 for j in range(self.pN):
		     tmp=self.function(self.X[j])
#		     if j==0:
#		         print i,j,'x=',self.X[j],'y=',tmp
		     if tmp<self.p_fit[j]:  ##updating personal best
		        self.pbest[j]=self.X[j]
			self.p_fit[j]=tmp
 		        if tmp<self.g_fit:  ##updating global best
 			   self.gbest=self.X[j]
 			   self.g_fit=tmp
		     self.V[j]=self.w*self.V[j]+self.c1*random.rand(self.dim)*(self.pbest[j]-self.X[j])+self.c2*random.rand(self.dim)*(self.gbest-self.X[j])
		     ##velocity normalization##
		     vnom=LA.norm(self.V[j])
#		     if j==0:
#		       print 'vnorm',vnom
		     if vnom>1.0:
		     	 self.V[j]/=vnom
		     self.X[j]+=self.V[j]
		     ##boundary regularization
		     for k in range(self.dim):
		         if self.X[j][k]<self.lb: self.X[j][k]=self.lb
		         if self.X[j][k]>self.ub: self.X[j][k]=self.ub
	     return array(fitness),array(gbestls)


    


if __name__=="__main__":
	my_pso=PSO(pN=20,dim=1,max_iter=100)
	my_pso.print_info()
	my_pso.init_Population()
	fitness,gbestls=my_pso.iterator()
	
	print "global minimum x=",gbestls[-1]
	print "global minimum y=",fitness[-1]
 	#print fitness

	figure(1)
	title('Global_best y vs iteration')
	plot(range(my_pso.max_iter),fitness,'o-')
	for i in range(my_pso.dim):
	    figure(i+2)
	    title('Global_best x_'+str(i)+' vs iteration')
	    plot(range(my_pso.max_iter),gbestls[:,i],'o-')
		
	figure(0)
	xs=linspace(my_pso.lb,my_pso.ub,200)
	ys=[my_pso.function(x) for x in xs]
	plot(xs,ys)
	if my_pso.dim==1:
    	   axvline(x=gbestls[-1],c='r')
	   savefig('PSO_globalmin.png')
	show()
