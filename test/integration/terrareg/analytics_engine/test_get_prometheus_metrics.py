

from unittest import mock
from terrareg.analytics import AnalyticsEngine
from . import AnalyticsIntegrationTest


class TestGetPrometheusMetrics(AnalyticsIntegrationTest):
    """Test get_prometheus_metrics method."""

    def test_get_prometheus_with_no_modules(self):
        """Test function with no analytics recorded or module providers."""
        get_total_count_mock = mock.MagicMock(return_value=0)
        get_module_provider_version_statistics_mock = mock.MagicMock(return_value=(0, 0, 0))
        with mock.patch('terrareg.models.ModuleProvider.get_total_count', get_total_count_mock), \
                mock.patch('terrareg.analytics.AnalyticsEngine.get_module_provider_version_statistics', get_module_provider_version_statistics_mock):
            assert AnalyticsEngine.get_prometheus_metrics() == """
# HELP module_providers_count Total number of module providers with a published version
# TYPE module_providers_count counter
module_providers_count 0
# HELP module_version_major_count Total number of major versions released
# TYPE module_version_major_count counter
module_version_major_count 0
# HELP module_version_minor_count Total number of minor versions released
# TYPE module_version_minor_count counter
module_version_minor_count 0
# HELP module_version_patch_count Total number of patch versions released
# TYPE module_version_patch_count counter
module_version_patch_count 0
# HELP module_provider_usage Analytics tokens used in a module provider
# TYPE module_provider_usage counter
""".strip()

    def test_get_prometheus_with_no_analytics(self):
        """Test function with no analytics recorded."""
        assert AnalyticsEngine.get_prometheus_metrics() == """
# HELP module_providers_count Total number of module providers with a published version
# TYPE module_providers_count counter
module_providers_count 6
# HELP module_version_major_count Total number of major versions released
# TYPE module_version_major_count counter
module_version_major_count 8
# HELP module_version_minor_count Total number of minor versions released
# TYPE module_version_minor_count counter
module_version_minor_count 3
# HELP module_version_patch_count Total number of patch versions released
# TYPE module_version_patch_count counter
module_version_patch_count 2
# HELP module_provider_usage Analytics tokens used in a module provider
# TYPE module_provider_usage counter
""".strip()

    def test_get_prometheus(self):
        """Test function with data present"""
        self._import_test_analytics(self._TEST_ANALYTICS_DATA)

        assert AnalyticsEngine.get_prometheus_metrics() == """
# HELP module_providers_count Total number of module providers with a published version
# TYPE module_providers_count counter
module_providers_count 6
# HELP module_version_major_count Total number of major versions released
# TYPE module_version_major_count counter
module_version_major_count 8
# HELP module_version_minor_count Total number of minor versions released
# TYPE module_version_minor_count counter
module_version_minor_count 3
# HELP module_version_patch_count Total number of patch versions released
# TYPE module_version_patch_count counter
module_version_patch_count 2
# HELP module_provider_usage Analytics tokens used in a module provider
# TYPE module_provider_usage counter
module_provider_usage{module_provider_id="testnamespace/publishedmodule/testprovider", analytics_token="application-using-old-version"} 1
module_provider_usage{module_provider_id="testnamespace/publishedmodule/testprovider", analytics_token="duplicate-application"} 1
module_provider_usage{module_provider_id="testnamespace/publishedmodule/secondprovider", analytics_token="duplicate-application"} 1
module_provider_usage{module_provider_id="testnamespace/secondmodule/testprovider", analytics_token="duplicate-application"} 1
module_provider_usage{module_provider_id="secondnamespace/othernamespacemodule/anotherprovider", analytics_token="duplicate-application"} 1
module_provider_usage{module_provider_id="testnamespace/publishedmodule/testprovider", analytics_token="second-application"} 1
module_provider_usage{module_provider_id="testnamespace/publishedmodule/secondprovider", analytics_token="test-app-using-second-module"} 1
module_provider_usage{module_provider_id="testnamespace/secondmodule/testprovider", analytics_token="test-app-using-second-module"} 1
module_provider_usage{module_provider_id="testnamespace/publishedmodule/testprovider", analytics_token="test-application"} 1
module_provider_usage{module_provider_id="testnamespace/publishedmodule/testprovider", analytics_token="without-analytics-key"} 1
module_provider_usage{module_provider_id="testnamespace/noanalyticstoken/testprovider", analytics_token="withoutanalytics"} 1
""".strip()
