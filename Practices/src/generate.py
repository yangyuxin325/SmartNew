# import tokenize
# 
# reader = open('connect.py').next
# tokens = tokenize.generate_tokens(reader)
# print tokens.next()
# print tokens.next()
# print tokens.next()

# def power(values):
#     for value in values:
#         print 'powering %s' % value
#         yield value
#         
# def adder(values):
#     for value in values:
#         print 'adding to %s' % value
#         if value % 2 == 0:
#             yield value + 3
#         else:
#             yield value + 2
#             
# elements = [1, 4, 7, 9, 12, 19]
# res = adder(power(elements))
# print res.next()

# def psychologist():
#     print 'Please tell me your problems'
#     while True:
#         answer = (yield)
#         if answer is not None:
#             if answer.endswith('?'):
#                 print ("Don't ask yourself "
#                 "to much questions")
#             elif 'good' in answer:
#                 print "A that's good, go on"
#             elif 'bad' in answer:
#                 print "Don't be so negative"
# 
# free = psychologist()
# print free.next()
# free.send("Why I shouldn't?")

def my_generator():
    try:
        yield 'someting'
    except ValueError:
        yield 'dealing with the exception'
    finally:
        print "ok let's clean"
        
gen = my_generator()
print gen.next()
print gen.throw(ValueError('mean mean mean'))
gen.close()