from django.contrib import admin

from .models import Playlist

@admin.register(Playlist)
class PlaylistAdmint(admin.ModelAdmin):

    save_on_top = True

    date_hierarchy = 'created'

    list_display = [
        '__str__',
        'task_id',
        'mixdown_file',
        'created',
        'status',
    ]

    list_filter = [
        'status',
        'created',
    ]

