class AnyIter(object):
    def __init__(self, data, safe=False):
        self.safe = safe
        self.iter = iter(data)
        
    def __iter__(self):
        return self
    
    def next(self, howmany=1):
        retval = []
        for eachItem in range(howmany):
            try:
                retval.append(self.iter.next())
            except StopIteration:
                if self.safe:
                    break
                else:
                    raise
        return retval
    
a = AnyIter(range(10),True)
i = iter(a)
for j in range(1,5):
    print j, " : ", i.next(j)
    
print range(10)
    
