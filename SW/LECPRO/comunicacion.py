#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 17:25:38 2017

@author: henry
"""

# simple inquiry example
# bluetooth low energy scan
from bluepy import btle
 
print "Connecting..."
dev = btle.Peripheral()
dev.connect("d4:36:39:de:43:96") 
print "Services..."
for svc in dev.services:
     print str(svc)