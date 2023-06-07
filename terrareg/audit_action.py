
from enum import Enum


class AuditAction(Enum):
    """Types of audit events"""

    NAMESPACE_CREATE = "namespace_create"

    MODULE_PROVIDER_CREATE = "module_provider_create"
    MODULE_PROVIDER_DELETE = "module_provider_delete"

    MODULE_PROVIDER_UPDATE_GIT_TAG_FORMAT = "module_provider_update_git_tag_format"
    MODULE_PROVIDER_UPDATE_GIT_PROVIDER = "module_provider_update_git_provider"
    MODULE_PROVIDER_UPDATE_GIT_PATH = "module_provider_update_git_path"
    MODULE_PROVIDER_UPDATE_GIT_CUSTOM_BASE_URL = "module_provider_update_git_custom_base_url"
    MODULE_PROVIDER_UPDATE_GIT_CUSTOM_CLONE_URL = "module_provider_update_git_custom_clone_url"
    MODULE_PROVIDER_UPDATE_GIT_CUSTOM_BROWSE_URL = "module_provider_update_git_custom_browse_url"
    MODULE_PROVIDER_UPDATE_VERIFIED = "module_provider_update_verified"

    MODULE_VERSION_INDEX = "module_version_index"
    MODULE_VERSION_PUBLISH = "module_version_publish"
    MODULE_VERSION_DELETE = "module_version_delete"

    USER_GROUP_CREATE = "user_group_create"
    USER_GROUP_DELETE = "user_group_delete"
    USER_GROUP_NAMESPACE_PERMISSION_ADD = "user_group_namespace_permission_add"
    USER_GROUP_NAMESPACE_PERMISSION_MODIFY = "user_group_namespace_permission_modify"
    USER_GROUP_NAMESPACE_PERMISSION_DELETE = "user_group_namespace_permission_delete"

    USER_LOGIN = "user_login"