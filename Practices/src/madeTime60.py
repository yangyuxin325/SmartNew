class Time60(object):
    def __init__(self, hr, mt):
        self.hr = hr
        self.mt = mt
        
    def __str__(self):
        return '%d:%d' % (self.hr, self.mt)
    
    def __add__(self, other):
        return self.__class__(self.hr + other.hr, self.mt + other.mt)
    
    __repr__ = __str__
    
    def __iadd__(self, other):
        self.hr += other.hr
        self.mt += other.mt
        return self
    
    
mon = Time60(10,30)
tue = Time60(11,15)

print mon, tue

print mon + tue
    
print id(mon)
# print mon + tue
mon += tue

# print mon.__iadd__(tue)

print id(mon)

print mon

    
    