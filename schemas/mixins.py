from django.contrib.auth.mixins import AccessMixin


class SchemaAccessMixin(AccessMixin):
    """Verify that the current user have access to schema."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user == self.get_object().user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
