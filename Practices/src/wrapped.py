class Wrapme(object):
    def __init__(self, obj):
        self.__data = obj
        
    def get(self):
        return self.__data
    
    def __repr__(self):
        return 'self.__data'
    
    def __str__(self):
        return str(self.__data)
    
    def __getattr__(self, attr):
        return getattr(self.__data, attr)
    

WrappedComplex = Wrapme(3.5+4.2j)
print WrappedComplex

print WrappedComplex.real

print WrappedComplex.imag

print WrappedComplex.conjugate()
        
print WrappedComplex.get()

wrappedList = Wrapme([123, 'foo', 45.67])
wrappedList.append('bar')
wrappedList.append(123)
print wrappedList

print wrappedList.count(123)

print wrappedList.pop()

print wrappedList

realList = wrappedList.get()
print realList[3]