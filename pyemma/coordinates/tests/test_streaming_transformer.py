import unittest
import numpy as np
from pyerna.coordinates import source
from pyerna.coordinates.data._base.transformer import StreamingTransformer


class MyTransformer(StreamingTransformer):
    def _transform_array(self, array):
        return array * 2

    def describe(self, *args, **kwargs):
        return ()

    def dimension(self):
        return 1


class TestStreamingTransformer(unittest.TestCase):
    def test_get_output(self):
        data = np.ones(10)
        t = MyTransformer()
        t.data_producer = source(data)
        out = t.get_output()
        np.testing.assert_equal(out[0].squeeze(), data*2)
