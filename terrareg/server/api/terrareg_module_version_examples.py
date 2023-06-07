
from terrareg.server.error_catching_resource import ErrorCatchingResource


class ApiTerraregModuleVersionExamples(ErrorCatchingResource):
    """Interface to obtain list of examples in module version."""

    def _get(self, namespace, name, provider, version):
        """Return list of examples."""
        _, _, _, module_version, error = self.get_module_version_by_name(namespace, name, provider, version)
        if error:
            return error

        return [
            {
                'path': example.path,
                'href': example.get_view_url()
            }
            for example in module_version.get_examples()
        ]
