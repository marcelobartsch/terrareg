
from flask_restful import reqparse

from terrareg.server.error_catching_resource import ErrorCatchingResource
import terrareg.models
import terrareg.module_search


class ApiModuleDetails(ErrorCatchingResource):
    def _get(self, namespace, name):
        """Return latest version for each module provider."""

        parser = reqparse.RequestParser()
        parser.add_argument(
            'offset', type=int, location='args',
            default=0, help='Pagination offset')
        parser.add_argument(
            'limit', type=int, location='args',
            default=10, help='Pagination limit'
        )
        args = parser.parse_args()

        namespace, _ = terrareg.models.Namespace.extract_analytics_token(namespace)

        search_results = terrareg.module_search.ModuleSearch.search_module_providers(
            offset=args.offset,
            limit=args.limit,
            namespaces=[namespace],
            modules=[name]
        )

        if not search_results.module_providers:
            return self._get_404_response()

        return {
            "meta": search_results.meta,
            "modules": [
                module_provider.get_latest_version().get_api_outline()
                for module_provider in search_results.module_providers
            ]
        }

