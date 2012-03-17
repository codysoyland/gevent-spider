from gevent.monkey import patch_all; patch_all()

def web():
    from .web import serve
    print 'Serving on port 8088...'
    serve()
