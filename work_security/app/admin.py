from django.contrib import admin

from app.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Gallery)
admin.site.register(Instruction)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TestToUser)
