# coding=utf-8
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from urllib import urlencode
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs


class SimplePaginator(object):
    """A simple wrapper around the Django paginator."""

    def __init__(self, request, prefix, data, columns=None, per_page=20, orphans=1):
        """Initialize a Paginator and set some properties. Return a tuple
        containing items and ordering key.

        Keyword arguments:
        request -- The request object
        prefix -- The prefix for the controls' css-class
        data -- Elements to paginate
        columns -- A tuple of tuples containing column name and key (default None)
        per_page -- How many elements to display per page (default 20)
        orphans -- Whether to move orphans to the previous page (default 1)

        """
        self.request = request
        self.prefix = prefix
        self.data = data
        self.columns = columns
        self.per_page = per_page
        self.orphans = orphans

    def get_base_url(self):
        '''Get query string from request, remove all necessary parts and return
        two variants - one for the page suffix, one for the order suffix.

        '''
        # Get querystring and path, initialize variables
        qsd = parse_qs(self.request.META['QUERY_STRING'])
        path = self.request.META['PATH_INFO']
        qs_pa = qs_or = ''
        qs = baseurl = {}

        # Remove arguments that mighmight overwritten
        if qsd:
            if self.prefix + '_pa' in qsd:
                qs_pa = qsd.pop(self.prefix + '_pa')[0]
            if self.prefix + '_or' in qsd:
                qs_or = qsd.pop(self.prefix + '_or')[0]

        # Get querystring for both suffix variants
        qs_base = [(k, qsd[k][0]) for k in qsd]
        if qs_or:
            qs['pa'] = urlencode(qs_base + [(self.prefix + '_or', qs_or)])
        if qs_pa:
            qs['or'] = urlencode(qs_base + [(self.prefix + '_pa', qs_pa)])

        # Build base url
        if 'pa' in qs:
            baseurl['pa'] = '%s?%s&' % (path, qs['pa'])
        if 'or' in qs:
            baseurl['or'] = '%s?%s&' % (path, qs['or'])
        if qsd:
            if not 'pa' in baseurl:
                baseurl['pa'] = '%s?%s&' % (path, urlencode(qs_base))
            if not 'or' in baseurl:
                baseurl['or'] = '%s?%s&' % (path, urlencode(qs_base))
        else:
            if not 'pa' in baseurl:
                baseurl['pa'] = path + '?'
            if not 'or' in baseurl:
                baseurl['or'] = path + '?'

        return baseurl

    def paginate(self):
        # Make sure page number is an int. If not, deliver first page.
        try:
            page = int(self.request.GET.get('%s_pa' % self.prefix, 1))
        except ValueError:
            page = 1

        # Get sorting key
        try:
            order = int(self.request.GET.get('%s_or' % self.prefix, 0))
        except ValueError:
            order = 0

        # Sort data
        # First, check if data supports order_by (e.g. a queryset)
        # TODO default ordering feature
        if hasattr(self.data, 'order_by') and self.columns and order:
            order_str = '%s' if order > 0 else '-%s'
            order_key = order_str % self.columns[abs(order) - 1][1]
            self.data = self.data.order_by(order_key)

        # If data doesn't support order_by, sort by index
        elif order:
            sortfunc = lambda x: x[abs(order) - 1] * cmp(order, 0)
            self.data = sorted(self.data, sortfunc)

        # Initialize paginator
        self.paginator = Paginator(self.data, self.per_page, self.orphans)

        # Get pagination items for current page. If page request is out of
        # range, deliver last page of results.
        try:
            items = self.paginator.page(page)
        except (EmptyPage, InvalidPage):
            items = self.paginator.page(self.paginator.num_pages)

        # Get base url
        baseurl = self.get_base_url()

        return items, order, baseurl


def paginate(*args, **kwargs):
    """Shortcut function to avoid having to instantiate the SimplePaginator
    Class."""
    p = SimplePaginator(*args, **kwargs)
    return p.paginate()
