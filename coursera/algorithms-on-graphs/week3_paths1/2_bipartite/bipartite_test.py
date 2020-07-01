import unittest
from bipartite import bipartite
import signal
import sys
from functools import wraps
class TimedOut(BaseException):
    pass

def timeout(seconds):
    """Decorator that makes a function time out.
    Because test suites that hang are no fun.  Especially on buildbots.
    Currently only implemented for Unix.
    """
    def decorator(fn):
        if hasattr(signal, 'alarm'):
            # yay, unix!
            @wraps(fn)
            def wrapper(*args, **kw):
                this_frame = sys._getframe()
                def raiseTimeOut(signal, frame):
                    # the if statement here is meant to prevent an exception in the
                    # finally: clause before clean up can take place
                    if frame is not this_frame:
                        raise TimedOut('timed out after %s seconds' % seconds)
                prev_handler = signal.signal(signal.SIGALRM, raiseTimeOut)
                try:
                    signal.alarm(seconds)
                    return fn(*args, **kw)
                finally:
                    signal.alarm(0)
                    signal.signal(signal.SIGALRM, prev_handler)
            return wrapper
        else:
            # XXX um, could someone please implement this for Windows and other
            # strange platforms?
            return fn
    return decorator

class MyTestCase(unittest.TestCase):
    def test1(self):
        result = bipartite([[3], [4, 3], [3], [1, 2, 0], [1]])
        self.assertEqual(1, result)
    def test2(self):
        result = bipartite([[1, 3, 2], [0, 2], [1, 0], [0]])
        self.assertEqual(0, result)
    def test3(self):
        result = bipartite([[], [], [], []])
        self.assertEqual(1, result)
    def test4(self):
        result = bipartite([[1], [0], [3], [2]])
        self.assertEqual(1, result)
    @timeout(20)
    def test5(self):
        long_list = [ [] for _ in range(100000) ]
        result = bipartite(long_list)
        self.assertEqual(1, result)

if __name__ == '__main__':
    unittest.main()
