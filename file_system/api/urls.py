from django.urls import path, include, re_path
from file_system.api import views as api_view

urlpatterns = [
    path("<path:path>/", api_view.root_dir_child, name="root-to-child"),
    path("remove/<path:path>", api_view.remove_file_or_dir, name="remove-file-or-dir"),
    path("create/<path:path>", api_view.create_dir, name="create-dir"),
    path("rename", api_view.rename_dir, name="rename-dir"),
    path("create-wordlist", api_view.createWordlist, name="create-wordlist"),
]
