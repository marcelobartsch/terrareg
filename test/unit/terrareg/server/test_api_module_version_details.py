
from test.unit.terrareg import (
    mock_models,
    setup_test_data, TerraregUnitTest
)
from test import client
import terrareg.models


class TestApiModuleVersionDetails(TerraregUnitTest):
    """Test ApiModuleVersionDetails resource."""

    @setup_test_data()
    def test_existing_module_version(self, client, mock_models):
        res = client.get('/v1/modules/moduledetails/fullypopulated/testprovider/1.5.0')

        assert res.json == {
            'id': 'moduledetails/fullypopulated/testprovider/1.5.0',
            'namespace': 'moduledetails',
            'name': 'fullypopulated',
            'provider': 'testprovider',
            'verified': False,
            'trusted': False,
            'versions': ['1.2.0', '1.6.1-beta', '1.5.0'],
            'owner': 'This is the owner of the module',
            'version': '1.5.0',
            'description': 'This is a test module version for tests.',
            'source': 'https://link-to.com/source-code-here',
            'published_at': '2022-01-05T22:53:12',
            'downloads': 0,
            'internal': False,
            'root': {
                'path': '',
                'readme': '# This is an exaple README!',
                'empty': False,
                'inputs': [
                    {'name': 'name_of_application', 'type': 'string', 'description': 'Enter the application name', 'default': None, 'required': True},
                    {'name': 'string_with_default_value', 'type': 'string', 'description': 'Override the default string', 'default': 'this is the default', 'required': False},
                    {'name': 'example_boolean_input', 'type': 'bool', 'description': 'Override the truthful boolean', 'default': True, 'required': False},
                    {'name': 'example_list_input', 'type': 'list', 'description': 'Override the stringy list', 'default': ['value 1', 'value 2'], 'required': False}
                ],
                'outputs': [
                    {'name': 'generated_name', 'description': 'Name with randomness'},
                    {'name': 'no_desc_output', 'description': None}
                ],
                'dependencies': [
                    {
                        'name': 'hashicorp-registry-module',
                        'source': 'matthewjohn/test-module/null',
                        'version': '1.5.0'
                    },
                    {
                        'name': 'local-registry-module',
                        'source': 'my-registry.example.com/matthewjohn/test-module/null',
                        'version': '2.1.3'
                    }
                ],
                'provider_dependencies': [
                    {'name': 'random', 'namespace': 'hashicorp', 'source': '', 'version': '>= 5.2.1, < 6.0.0'},
                    {'name': 'unsafe', 'namespace': 'someothercompany', 'source': '', 'version': '2.0.0'}
                ],
                'resources': [
                    {'type': 'string', 'name': 'random_suffix', 'provider': 'random', 'source': 'hashicorp/random', 'mode': 'managed', 'version': 'latest', 'description': None}
                ]
            },
            'submodules': [],
            'providers': ['testprovider']
        }

        assert res.status_code == 200

    @setup_test_data()
    def test_unverified_module_version(self, client, mock_models):
        res = client.get('/v1/modules/testnamespace/unverifiedmodule/testprovider/1.2.3')

        assert res.json == {
            'id': 'testnamespace/unverifiedmodule/testprovider/1.2.3', 'owner': 'Mock Owner',
            'namespace': 'testnamespace', 'name': 'unverifiedmodule',
            'version': '1.2.3', 'provider': 'testprovider',
            'description': 'Mock description',
            'source': None,
            'published_at': '2020-01-01T23:18:12',
            'downloads': 0, 'verified': False, 'trusted': False, 'internal': False,
            'root': {
                'path': '', 'readme': 'Mock module README file',
                'empty': False, 'inputs': [], 'outputs': [], 'dependencies': [],
                'provider_dependencies': [], 'resources': []
            },
            'submodules': [], 'providers': ['testprovider'], 'versions': ['1.2.3']
        }

        assert res.status_code == 200

    @setup_test_data()
    def test_internal_module_version(self, client, mock_models):
        res = client.get('/v1/modules/testnamespace/internalmodule/testprovider/5.2.0')

        assert res.json == {
            'id': 'testnamespace/internalmodule/testprovider/5.2.0', 'owner': 'Mock Owner',
            'namespace': 'testnamespace', 'name': 'internalmodule',
            'version': '5.2.0', 'provider': 'testprovider',
            'description': 'Mock description',
            'source': None,
            'published_at': '2020-01-01T23:18:12',
            'downloads': 0, 'verified': False, 'trusted': False, 'internal': True,
            'root': {
                'path': '', 'readme': 'Mock module README file',
                'empty': False, 'inputs': [], 'outputs': [], 'dependencies': [],
                'provider_dependencies': [], 'resources': []
            },
            'submodules': [], 'providers': ['testprovider'], 'versions': ['5.2.0']
        }

        assert res.status_code == 200

    @setup_test_data()
    def test_non_existent_module_version(self, client, mock_models):
        """Test endpoint with non-existent module"""

        res = client.get('/v1/modules/namespacename/modulename/providername/0.1.2')

        assert res.json == {'errors': ['Not Found']}
        assert res.status_code == 404

    @setup_test_data()
    def test_analytics_token(self, client, mock_models):
        """Test endpoint with analytics token"""

        res = client.get('/v1/modules/test_token-name__testnamespace/testmodulename/testprovider/2.4.1')

        test_namespace = terrareg.models.Namespace(name='testnamespace')
        test_module = terrareg.models.Module(namespace=test_namespace, name='testmodulename')
        test_module_provider = terrareg.models.ModuleProvider(module=test_module, name='testprovider')
        test_module_version = terrareg.models.ModuleVersion(module_provider=test_module_provider, version='2.4.1')

        assert res.json == test_module_version.get_api_details()
        assert res.status_code == 200
