
from terrareg.server.error_catching_resource import ErrorCatchingResource


class ApiTerraregModuleVersionVariableTemplate(ErrorCatchingResource):
    """Provide variable template for module version."""

    def _get(self, namespace, name, provider, version):
        """Return variable template."""
        _, _, _, module_version, error = self.get_module_version_by_name(
            namespace, name, provider, version)
        if error:
            return error
        return module_version.variable_template