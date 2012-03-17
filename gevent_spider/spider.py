from gevent.threadpool import ThreadPool
from gevent.pool import Pool
from lxml.html import fromstring
from urlparse import urlsplit, urljoin
import requests
from .utils import timer

def spider(client, url, domain_whitelist=None, pool=None, threadpool=None, tested=None):
    client.send_status('Spidering {url}...'.format(url=url))

    domain_whitelist = domain_whitelist or (urlsplit(url).netloc,)
    threadpool = threadpool or ThreadPool(4) # for lxml - 4 workers
    pool = pool or Pool() # maximum number of concurrent HTTP requests
    tested = tested or set([url])

    with timer() as timed:
        response = requests.get(url)

    result = dict(
        status_code = response.status_code,
        length = len(response.text),
        headers = response.headers,
        url = url,
        duration = timed.result(),
    )
    client.send_result(result)

    html = threadpool.apply(fromstring, [response.text])
    for link in html.cssselect('a'):
        href = link.attrib.get('href').split('#')[0].strip()
        if not href:
            continue
        url = urljoin(response.url, href)
        parts = urlsplit(url)
        if parts.netloc not in domain_whitelist:
            continue
        if url in tested:
            continue
        tested.add(url)
        pool.spawn(spider, client, url, domain_whitelist, pool, threadpool, tested)
    return pool
