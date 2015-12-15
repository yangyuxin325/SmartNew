class FooClass(object):
    """my very first class : FooClass"""
    
    version = 0.1
    
    def __init__(self, nm = 'John Doe'):
        """ constructor"""
        self.name = nm
        print "Created a class instance for", nm
        
    def showname(self):
        """display instance attribute and class name"""
        print 'Your name is',self.name
        print 'My name is',self.__class__.__name__
        
    def shower(self):
        """display class(static) attribute"""
        print self.version
    
    def addMe2Me(self,x):
        """apply + operation to argument"""
        return x + x
    
foo1 = FooClass()

foo1.shower()

print foo1.addMe2Me(5)
 
print foo1.addMe2Me('xyz')       

foo2 = FooClass('Jane Smith')

foo2.showname()

print('Enter five number')
v = []
i = 0
s = 0
while i < 5:
    a = input('n%d = ' % (i+1))
    v.extend([int(a)])
    s = s + v[i]
    i += 1
print (v)
print('sum = %d' % s)
