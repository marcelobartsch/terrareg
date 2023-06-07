
import pytest

from terrareg.models import Module, ModuleProvider, Namespace
from test.integration.terrareg import TerraregIntegrationTest

class TestProviderLogo(TerraregIntegrationTest):

    @pytest.mark.parametrize('provider_name,expect_exists', [
        ('aws', True),
        ('gcp', True),
        ('null', True),
        ('datadog', True),
        ('doesnotexist', False),
    ])
    def test_logo_exists(self, provider_name, expect_exists):
        """Test exists method of logo provider"""
        namespace = Namespace(name='real_providers')
        module = Module(namespace=namespace, name='test-module')
        module_provider = ModuleProvider(module=module, name=provider_name)
        logo = module_provider.get_logo()
        assert logo.exists == expect_exists

    @pytest.mark.parametrize('provider_name,expected_tos', [
        ('aws', 'Amazon Web Services, AWS, the Powered by AWS logo are trademarks of Amazon.com, Inc. or its affiliates.'),
        ('gcp', 'Google Cloud and the Google Cloud logo are trademarks of Google LLC.'),
        ('null', ' '),
        ('datadog', 'All \'Datadog\' modules are designed to work with Datadog. Modules are in no way affiliated with nor endorsed by Datadog Inc.'),
        ('consul', 'All \'Consul\' modules are designed to work with HashiCorp Consul. Terrareg and modules hosted within it are in no way affiliated with, nor endorsed by, HashiCorp. HashiCorp, HashiCorp Consul and the HashiCorp Consul logo are trademarks of HashiCorp.'),
        ('nomad', 'All \'Nomad\' modules are designed to work with HashiCorp Nomad. Terrareg and modules hosted within it are in no way affiliated with, nor endorsed by, HashiCorp. HashiCorp, HashiCorp Nomad and the HashiCorp Nomad logo are trademarks of HashiCorp.'),
        ('vagrant', 'All \'Vagrant\' modules are designed to work with HashiCorp Vagrant. Terrareg and modules hosted within it are in no way affiliated with, nor endorsed by, HashiCorp. HashiCorp, HashiCorp Vagrant and the HashiCorp Vagrant logo are trademarks of HashiCorp.'),
        ('vault', 'All \'Vault\' modules are designed to work with HashiCorp Vault. Terrareg and modules hosted within it are in no way affiliated with, nor endorsed by, HashiCorp. HashiCorp, HashiCorp Vault and the HashiCorp Vault logo are trademarks of HashiCorp.'),
        ('doesnotexist', None),
    ])
    def test_logo_tos(self, provider_name, expected_tos):
        """Test tos property of ProviderLogo"""
        namespace = Namespace(name='real_providers')
        module = Module(namespace=namespace, name='test-module')
        module_provider = ModuleProvider(module=module, name=provider_name)
        logo = module_provider.get_logo()
        assert logo.tos == expected_tos

    @pytest.mark.parametrize('provider_name,expected_alt', [
        ('aws', 'Powered by AWS Cloud Computing'),
        ('gcp', 'Google Cloud'),
        ('null', 'Null Provider'),
        ('datadog', 'Works with Datadog'),
        ('consul', 'Hashicorp Consul'),
        ('nomad', 'Hashicorp Nomad'),
        ('vagrant', 'Hashicorp Vagrant'),
        ('vault', 'Hashicorp Vault'),
        ('doesnotexist', None),
    ])
    def test_logo_alt(self, provider_name, expected_alt):
        """Test alt property of ProviderLogo"""
        namespace = Namespace(name='real_providers')
        module = Module(namespace=namespace, name='test-module')
        module_provider = ModuleProvider(module=module, name=provider_name)
        logo = module_provider.get_logo()
        assert logo.alt == expected_alt

    @pytest.mark.parametrize('provider_name,expected_link', [
        ('aws', 'https://aws.amazon.com/'),
        ('gcp', 'https://cloud.google.com/'),
        ('null', '#'),
        ('datadog', 'https://www.datadoghq.com/'),
        ('doesnotexist', None),
        ('consul', '#'),
        ('nomad', '#'),
        ('vagrant', '#'),
        ('vault', '#'),
    ])
    def test_logo_link(self, provider_name, expected_link):
        """Test link property of ProviderLogo"""
        namespace = Namespace(name='real_providers')
        module = Module(namespace=namespace, name='test-module')
        module_provider = ModuleProvider(module=module, name=provider_name)
        logo = module_provider.get_logo()
        assert logo.link == expected_link

    @pytest.mark.parametrize('provider_name,expected_source', [
        ('aws', '/static/images/PB_AWS_logo_RGB_stacked.547f032d90171cdea4dd90c258f47373c5573db5.png'),
        ('gcp', '/static/images/gcp.png'),
        ('null', '/static/images/null.png'),
        ('datadog', '/static/images/dd_logo_v_rgb.png'),
        ('doesnotexist', None),
        ('consul', '/static/images/consul.png'),
        ('nomad', '/static/images/nomad.png'),
        ('vagrant', '/static/images/vagrant.png'),
        ('vault', '/static/images/vault.png'),
    ])
    def test_logo_source(self, provider_name, expected_source):
        """Test source property of ProviderLogo"""
        namespace = Namespace(name='real_providers')
        module = Module(namespace=namespace, name='test-module')
        module_provider = ModuleProvider(module=module, name=provider_name)
        logo = module_provider.get_logo()
        assert logo.source == expected_source
