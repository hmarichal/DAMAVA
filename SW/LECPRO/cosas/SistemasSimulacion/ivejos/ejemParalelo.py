# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 20:36:10 2018

@author: henry
"""
from multiprocessing import Process

def func1(p,s):
  print 'func1: starting'
  for i in xrange(10000000): pass
  print 'func1: finishing'
  print p
  print s
  while(True):
      a = p
def func2(p,s):
  print 'func2: starting'
  for i in xrange(10000000): pass
  print 'func2: finishing'
  print p
  print s
  while(True):
      a = p

if __name__ == '__main__':
  p1 = Process(target=func1,args=('hola',1))
  p1.start()
  p2 = Process(target=func2,args=('hola2',2))
  p2.start()
#  p1.join()
#  p2.join()