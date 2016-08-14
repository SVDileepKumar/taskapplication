from django.contrib import admin
from tasks.models import *

# Register your models here.

# @admin.register(TasksModel,site=index)
# class MyAdmin(admin.ModelAdmin):
#     pass
admin.site.register(Project)
admin.site.register(TasksModel)
admin.site.register(TaskList)
admin.site.register(MileStone)
admin.site.register(UserModel)
admin.site.register(TasklistUserModel)
admin.site.register(CommentsModel)
