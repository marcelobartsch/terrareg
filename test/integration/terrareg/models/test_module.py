
import pytest

from terrareg.models import Module, Namespace
import terrareg.errors
from test.integration.terrareg import TerraregIntegrationTest

class TestModule(TerraregIntegrationTest):

    @pytest.mark.parametrize('module_name', [
        'invalid@atsymbol',
        'invalid"doublequote',
        "invalid'singlequote",
        '-startwithdash',
        'endwithdash-',
        '_startwithunderscore',
        'endwithunscore_',
        'a:colon',
        'or;semicolon',
        'who?knows',
        '-a',
        'a-',
        'a_',
        '_a',
        '__',
        '--',
        '_',
        '-',
    ])
    def test_invalid_module_names(self, module_name):
        """Test invalid module names"""
        namespace = Namespace(name='test')
        with pytest.raises(terrareg.errors.InvalidModuleNameError):
            Module(namespace=namespace, name=module_name)

    @pytest.mark.parametrize('module_name', [
        'normalname',
        'name2withnumber',
        '2startendiwthnumber2',
        'contains4number',
        'with-dash',
        'with_underscore',
        'withAcapital',
        'StartwithCaptital',
        'endwithcapitaL',
        # Two letters
        'tl',
        # Two numbers
        '11',
        # Two characters with dash/unserscore
        'a-z',
        'a_z',
    ])
    def test_valid_module_names(self, module_name):
        """Test valid module names"""
        namespace = Namespace(name='test')
        Module(namespace=namespace, name=module_name)
