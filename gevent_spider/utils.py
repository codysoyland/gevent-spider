import time

class timer(object):
    """
    Context manager for timing operations.
    """
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self,ty,val,tb):
        self.end = time.time()
    def result(self):
        return self.end - self.start
