def psychologist():
    print 'Please tell me your problems'
    while True:
        answer = (yield)
        if answer is not None:
            if answer.endswith('?'):
                print("Don't ask yourself"
                     "too much question")
            elif 'good' in answer:
                print "A that's good, go on"
            elif 'bad' in answer:
                print "Don't be so negative"
                
free = psychologist()
free.next()

free.send('I feel bad')
free.send("Why I shouldn't ?")
free.send("ok then i should find what is good for me")

def my_generator():
    try:
        yield 'something'
    except ValueError:
        yield 'dealing with the exception'
    finally:
        print "ok let's clean"

gen =  my_generator()
print gen.next()

print gen.throw(ValueError('mean mean mean'))
gen.close()
print gen.next()