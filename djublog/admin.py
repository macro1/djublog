from django.contrib import admin
from djublog import models


class PostInline(admin.StackedInline):
    model = models.Post


class RemoteFeedAdmin(admin.ModelAdmin):
    inlines = (PostInline,)

    def save_model(self, request, obj, form, change):
        obj.update_feed()
        obj.save()


admin.site.register(models.RemoteFeed, RemoteFeedAdmin)
