'''
Created on 20/04/2015

@author: david
'''

class DataSmoothWindow(object):
    
    def __init__(self, size):
                
        self._data = [0]*size
        self._writeIndex = 0
        self._readIndex = 0
        self._size = size
        self._count = 0
        self._sum = 0
        
    
    def push(self, value):
        
        if self._count == self._size:
            
            self.pop()
        
        self._data[self._writeIndex] = value
        self._writeIndex = (self._writeIndex+1) % self._size        
    
        self._count += 1
        self._sum += value
        
    
    def pop(self):
        
        if self._count != 0:
            value = self._data[self._readIndex]
            self._readIndex = (self._readIndex + 1) % self._size                
        
            self._count = self._count-1
            self._sum = self._sum - value
        else:
            value = 0
        
        return value
     
    
    def count(self):
        
        return self._count
    
    
    def getSize(self):
        
        return self._size
    
    def sum(self):
        
        return self._sum
        
    def average(self):
        
        return self._sum / self._count
    
