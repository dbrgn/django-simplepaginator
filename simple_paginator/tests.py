from django.utils import unittest
from django.http import HttpRequest
from __init__ import *

class TestBaseUrl(unittest.TestCase):
    def setUp(self):
        self.request = HttpRequest()
        self.request.META['PATH_INFO'] = '/'

    def test1(self):
        self.request.META['QUERY_STRING'] = ''
        p = SimplePaginator(self.request, 'pfx', [])
        b = p.get_base_url()
        self.assertEqual(b['pa'], '/?')
        self.assertEqual(b['or'], '/?')

    def test2(self):
        self.request.META['QUERY_STRING'] = 'foo=bar'
        p = SimplePaginator(self.request, 'pfx', [])
        b = p.get_base_url()
        self.assertEqual(b['pa'], '/?foo=bar&')
        self.assertEqual(b['or'], '/?foo=bar&')

    def test3(self):
        self.request.META['QUERY_STRING'] = 'pfx_pa=3'
        p = SimplePaginator(self.request, 'pfx', [])
        b = p.get_base_url()
        self.assertEqual(b['pa'], '/?')
        self.assertEqual(b['or'], '/?pfx_pa=3&')

    def test4(self):
        self.request.META['QUERY_STRING'] = 'foo=bar&pfx_pa=3'
        p = SimplePaginator(self.request, 'pfx', [])
        b = p.get_base_url()
        self.assertEqual(b['pa'], '/?foo=bar&')
        self.assertEqual(b['or'], '/?foo=bar&pfx_pa=3&')

    def test5(self):
        self.request.META['QUERY_STRING'] = 'pfx_or=4'
        p = SimplePaginator(self.request, 'pfx', [])
        b = p.get_base_url()
        self.assertEqual(b['pa'], '/?pfx_or=4&')
        self.assertEqual(b['or'], '/?')

    def test6(self):
        self.request.META['QUERY_STRING'] = 'foo=bar&pfx_or=4'
        p = SimplePaginator(self.request, 'pfx', [])
        b = p.get_base_url()
        self.assertEqual(b['pa'], '/?foo=bar&pfx_or=4&')
        self.assertEqual(b['or'], '/?foo=bar&')

    def test7(self):
        self.request.META['QUERY_STRING'] = 'pfx_pa=3&pfx_or=4'
        p = SimplePaginator(self.request, 'pfx', [])
        b = p.get_base_url()
        self.assertEqual(b['pa'], '/?pfx_or=4&')
        self.assertEqual(b['or'], '/?pfx_pa=3&')

    def test8(self):
        self.request.META['QUERY_STRING'] = 'foo=bar&pfx_pa=3&pfx_or=4'
        p = SimplePaginator(self.request, 'pfx', [])
        b = p.get_base_url()
        self.assertEqual(b['pa'], '/?foo=bar&pfx_or=4&')
        self.assertEqual(b['or'], '/?foo=bar&pfx_pa=3&')
            

if __name__ == '__main__':
    unittest.main()
