
from flask_restful import reqparse, inputs

from terrareg.server.error_catching_resource import ErrorCatchingResource
import terrareg.models


class ApiTerraregGraphData(ErrorCatchingResource):
    """Interface to obtain module verison graph data."""

    def _get(self, namespace, name, provider, version, example_path=None, submodule_path=None):
        """Return graph data for module version."""
        parser = reqparse.RequestParser()
        parser.add_argument(
            "full_resource_names", type=inputs.boolean,
            default=False,
            help="Show resource labels as full path",
            location="args"
        )
        parser.add_argument(
            "full_module_names", type=inputs.boolean,
            default=False, help="Show module labels as full path",
            location="args"
        )
        args = parser.parse_args()

        _, _, module_provider, error = self.get_module_provider_by_names(namespace, name, provider)
        if error:
            return error

        module_version = terrareg.models.ModuleVersion.get(module_provider=module_provider, version=version)

        if module_version is None:
            return self._get_404_response()

        # If example or submodule is provided, obtain the object
        # and obtain module details object.
        if example_path:
            example = terrareg.models.Example.get(module_version=module_version, module_path=example_path)
            if not example:
                return self._get_404_response()
            module_details = example.module_details
        elif submodule_path:
            submodule = terrareg.models.Submodule.get(module_version=module_version, module_path=submodule_path)
            if not submodule:
                return self._get_404_response()
            module_details = submodule.module_details
        else:
            # Otherwise, use module version module details object
            module_details = module_version.module_details

        return module_details.get_graph_json(
            full_module_names=args.full_module_names,
            full_resource_names=args.full_resource_names)
