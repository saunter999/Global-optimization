#!/usr/bin/env python
from scipy import *
from pylab import *
from numpy import random

class Simulanneal:
	def __init__(self,dim,T0,nT,max_iter):
	    """
	    Nontrivial factors affecting the performance:
	    1)Starting temperature:T0,which shouldn't be too small and T should to be comparable to the typical difference in function values between local minima.
	    2)step for each proposing move: step
	    3)decreasing rate of T: rate
	    """
	    self.dim=dim
	    self.T0=T0
	    self.nT=nT
	    self.max_iter=int(max_iter)
	    self.ub=12.
	    self.lb=-12.
	    self.step=(self.ub-self.lb)*0.2
#	    self.step=5.0
	    self.X=self.lb*ones(self.dim)+(self.ub-self.lb)*random.rand(self.dim)
#	    self.rate=0.90
#	    self.Tls=[self.T0*self.rate**i for i in range(nT) ]
            ##Nonlinear mesh for temperature--cooling procedure
	    xs=linspace(1e-3,self.T0,self.nT)
	    self.Tls=[tanh(x)*self.T0 for x in xs]
	    self.Tls.reverse()

	   
	def print_info(self):
	    print "nT=",self.nT
	    print "dim=",self.dim
	    print "max_iter=",self.max_iter
	    print "lb=",self.lb
	    print "ub=",self.ub
	    print "step=",self.step


	def function(self,X):
# 	    return X*sin(X)+X*cos(2*X) 
#	    return cos(14.5 * X - 0.3) + (X + 0.2) * X
#	    return X**2-4*X+3  
	    return (X**2-5*X)*sin(X) 
#	    return LA.norm(X)**2
#	    return (X[0]**2+X[1]-11)**2+(X[0]+X[1]**2-7)**2

	def iterator(self):
 	    print "Tlow=",self.Tls[-1],"Thigh=",self.Tls[0]
 	    Xls=[]
 	    for T in (self.Tls):
 	       print 'T=',T
	       for i in range(self.max_iter):
		   tmp=self.X
		   fX=self.function(tmp)
		   rdm=-1.0*ones(self.dim)+2.0*random.rand(self.dim)
		   Xprm=tmp+self.step*rdm
		   fXprm=self.function(Xprm)
		   if fXprm<fX:
		      self.X=Xprm
		   else:
		      p=exp(-(fXprm-fX)/T)
		      r=random.rand()
		      if p>r: self.X=Xprm
		   if self.X>self.ub: self.X=self.ub
		   if self.X<self.lb: self.X=self.lb
#		   print i,self.X
		   Xls.append(self.X)
 	    return Xls
		   

if __name__=="__main__":
	my_SA=Simulanneal(dim=1,T0=2.5,nT=20,max_iter=5e3)
	my_SA.print_info()
	Xls=my_SA.iterator()
#	print 'X value in the last 20 iterations'
#	print Xls[-20:-1]
	print "global minimum x=",Xls[-1]
	print "global minimum y=",my_SA.function(Xls[-1])
	figure(1)
	title("X vs iteration")
	plot(range(my_SA.nT*my_SA.max_iter),Xls,'o-',markersize=1)
#	xscale('log')

	figure(0)
	xs=linspace(my_SA.lb,my_SA.ub,200)
	ys=[my_SA.function(x) for x in xs]
	plot(xs,ys)
	if my_SA.dim==1:
    	   axvline(x=Xls[-1],c='r')
	   savefig('SA_globalmin.png')
	
	show()
