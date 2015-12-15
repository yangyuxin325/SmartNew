def upper_attr(future_class_name, future_class_parents,future_class_attr):
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startwith('__'))
    uppercase_attr = dict((name.upper(),value) for name,value in attrs)
    return type(future_class_name, future_class_parents, uppercase_attr)

__metaclass__ = upper_attr

class Foo(object):
    bar = 'bip'
    
print hasattr(Foo, 'bar')
print hasattr(Foo, 'BAR')
 
# f = Foo()
# print f.BAR