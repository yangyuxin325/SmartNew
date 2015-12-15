class P1(object):
    def foo(self):
        print 'called P1-foo()'
        
class P2:
    def foo(self):
        print 'called P2-foo()'
        
    def bar(self):
        print 'called P2-bar()'
        
class C1(P1, P2):
    pass

class C2(P1, P2):
    def bar(self):
        print 'called C2-bar()'
        
class GC(C1, C2):
    pass

gc = GC()

gc.foo()

gc.bar()

C2.bar(gc)

class B(object):
    pass

class C(object):
    def __init__(self):
        print 'the default constructor'
        
class D(B, C):
    pass

d = D()