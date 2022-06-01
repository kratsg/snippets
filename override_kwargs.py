import contextlib
import sys

@contextlib.contextmanager
def override(**new_kwargs):
    def _wrapper(frame, event, arg):
        #print(f"Entering: {frame.f_code.co_name}")
        #print(f"{frame.f_locals}")
        if event not in ['call']: return
        current_kwargs = frame.f_locals
        common_keys = current_kwargs.keys() & new_kwargs.keys()
        frame.f_locals.update({**current_kwargs, **dict(zip(common_keys, map(new_kwargs.get, common_keys)))})

    sys.settrace(_wrapper)
    yield
    sys.settrace(None)

def foo(a=1, b=2):
    print(f'foo: a={a}, b={b}')

class Bar:
    def __init__(self, name='Bar', a=1, b=2):
        self.name = name
        print(f'{self.name}.init: a={a}, b={b}')

    def baz(self, a=1, b=2):
        print(f'{self.name}().baz: a={a}, b={b}')

print('Outside context, expect a=1, b=2')
foo()
bar = Bar()
bar.baz()

print('Outside context, expect a=3, b=4')
foo(3,4)
bar.baz(3,4)

with override(a=8, b=9):
    print('Inside context, expect a=8, b=9')
    foo()
    bar.baz()
    bar2 = Bar('Bar2')
    bar2.baz()
    print('Inside context, expect a=8, b=9 (still, even passing in a=3, b=4)')
    foo(3,4)
    bar.baz(3,4)
    bar2.baz(3,4)

print('Outside context again, expect a=1, b=2')
foo()
bar.baz()
bar2.baz()

print('Outside context, expect a=3, b=4')
foo(3,4)
bar.baz(3,4)
bar2.baz(3,4)
