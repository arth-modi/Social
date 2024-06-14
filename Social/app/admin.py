from django.contrib import admin
from .models import *
from django.contrib import messages
from django.utils.translation import ngettext
from .forms import SocialAdminForm
from import_export.admin import ImportExportActionModelAdmin
from .pagination import myPagination
from import_export.fields import Field
from import_export import resources

class PostResource(resources.ModelResource):
    user = Field(attribute="user__username",column_name='user')
    tags = Field(attribute="tags",column_name='tagss')

    class Meta:
        model = Post
        fields = ["id", "user", "title","tagss",'image','posted_at']
        
class PostInline(admin.StackedInline):
    model = Post
    per_page =5
# Register your models here.
# admin.site.register(Post)
@admin.register(Post)
class Postadmin(ImportExportActionModelAdmin):
    form= SocialAdminForm
    resource_class=PostResource
    list_display=['id', 'title', 'image','posted_at', 'user', 'tags']
    empty_value_display="--"
    save_as=True
    save_as_continue=False
    # fields=[('id', 'title'), 'posted_at', 'user']
    search_fields=['title', 'user__email']
    search_help_text="Search using title or email."
    list_filter=['user',]
    list_display_links = ["title"]
    list_select_related=['user']
    list_per_page=5
    actions=["update_tags"]
    # readonly_fields = ["image"]
    autocomplete_fields = ["user"]
    date_hierarchy='posted_at'
    def get_ordering(self, request):
        # if request.user.is_superuser:
        #     return ["title", "id"]
        # else:
        #     return ["id"]
        return ["id"]
    @admin.action(description="Tag as Update")
    def update_tags(self, request, queryset):
        queryset.update(tags="update")

# admin.site.disable_action("delete_selected")

# admin.site.register(Comment)
@admin.register(Comment)
class Commentadmin(admin.ModelAdmin):
    list_display=['id', 'text', 'post', 'user']
    save_as=True
    save_as_continue=False
    # fields=[('id', 'title'), 'posted_at', 'user']
    search_fields=['text', 'user__email']
    search_help_text="Search using text or email."
    list_filter=['user','post']
    list_display_links = ["text"]
    list_select_related=['user']
    list_per_page=5
    ordering=["id"]
    
# admin.site.register(Like)
@admin.register(Like)
class Likeadmin(admin.ModelAdmin):
    list_display=['id', 'post', 'user']
    save_as=True
    save_as_continue=False
    # fields=[('id', 'title'), 'posted_at', 'user']
    search_fields=['post', 'user']
    search_help_text="Search using post or user."
    list_filter=['user','post']
    list_display_links = ["id"]
    list_select_related=['user']
    list_per_page=5
# admin.site.register(CustomUser)
@admin.register(CustomUser)
class Useradmin(admin.ModelAdmin):
    list_display=["full_name", 'username', 'mobile', 'email','post_count']
    list_display_links = ["username"]
    inlines = [
        PostInline,
    ]
    # fields = [('first_name', 'last_name'), 'username', ]
    exclude = ["password", 'last_login']
    empty_value_display="----"
    search_fields=['username']
    list_filter=['username',]
    actions=["superuser_change"]
    date_hierarchy='date_joined'
    ordering=["first_name", "last_name"]
    @admin.display(description="Name", ordering="")
    def full_name(self, obj):
        if (obj.first_name and obj.last_name):
            return f"{obj.first_name} {obj.last_name}"
        elif obj.first_name:
            return f"{obj.first_name}"
        elif obj.last_name:
            return f"{obj.last_name}"
        else:
            return "----"
    
    @admin.display(description="No. of Posts", ordering="")
    def post_count(self, obj):
        return obj.user_related.count()
    
    @admin.action(description="Give Superuser permissions")
    def superuser_change(self, request, queryset):
        updated = queryset.update(is_superuser=True)
        self.message_user(
            request,
            ngettext(
                "%d user successfully given superuser status.",
                "%d users successfully given superuser status.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )
