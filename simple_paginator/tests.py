from django.utils import unittest
from django.http import HttpRequest
from django import test
from django.test.client import RequestFactory
from __init__ import *
from models import MockModel

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

class TestPaginate(test.TestCase):
    fixtures = ["testdata.json"]

    def setUp(self):
        self.columns = (
            ("Field1", "integer_field"),
            ("Field2", "testmethod"),
        )
        self.factory = RequestFactory()
        self.data = MockModel.objects.all()

    def test_sort_by_column(self):
        request = self.factory.get('/some/view?pfx_or=1&pfx_pa=1')
        items, order, base_url = paginate(request, 'pfx', self.data,
                columns=self.columns, per_page=5)
        self.assertEqual([i.id for i in items.object_list], [2,5,6,1,4])

    def test_sort_by_method(self):
        request = self.factory.get('/some/view?pfx_or=-2&pfx_pa=1')
        items, order, base_url = paginate(request, 'pfx', self.data,
                columns=self.columns, per_page=5)
        self.assertEqual([i.id for i in items.object_list], [5,7,3,2,4])

    def test_sort_by_index(self):
        data = [
            [1, 2, 23, 4, 5],
            [1, 2, 43, 4, 5],
            [1, 2, 31, 4, 5],
            [1, 2, 345, 4, 5]
        ]
        request = self.factory.get('/some/view?pfx_or=3&pfx_pa=2')
        items, order, base_url = paginate(request, 'pfx', data,
                columns=self.columns, per_page=2)
        self.assertEqual(items.object_list,
            [[1, 2, 43, 4, 5], [1, 2, 345, 4, 5]])


if __name__ == '__main__':
    unittest.main()
