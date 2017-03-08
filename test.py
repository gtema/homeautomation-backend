import unittest

"""General entry point for the tests
"""
if __name__ == '__main__':
    from tests.test_api_base import *
    from tests.test_basic import *
    from tests.test_stock_api import *
    from tests.test_models import *

    unittest.main()
