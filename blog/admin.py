from django.contrib import admin
from .models import Post

admin.site.register(Post)

# Generating admin sites for your staff or clients to add, change, and delete content 
# is tedious work that doesn’t require much creativity. For that reason, Django entirely 
# automates creation of admin interfaces for models.