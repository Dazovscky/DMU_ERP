from import_export import resources
from .models import *

class CommentResource(resources.ModelResource):
    class Meta:
        model = AttendanceTotalHours