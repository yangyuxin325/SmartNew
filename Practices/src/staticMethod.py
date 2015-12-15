# class TestStaticMethod:
#     def foo():
#         print 'calling static method foo()'
#          
#     foo = staticmethod(foo)
#         
#         
# class TestClassMethod:
#     def foo(cls):
#         print 'calling class method foo()'
#         print 'foo() is part of class: ',cls.__name__
#          
#     foo = classmethod(foo)

class TestStaticMethod:
    @staticmethod
    def foo():
        print 'calling static method foo()'
         
    
class TestClassMethod:
    @classmethod
    def foo(cls):
        print 'calling class method foo()'
        print 'foo() is part of class: ',cls.__name__
        
        
tsm = TestStaticMethod()
TestStaticMethod.foo()

tcm = TestClassMethod()
TestClassMethod.foo()
tcm.foo()
