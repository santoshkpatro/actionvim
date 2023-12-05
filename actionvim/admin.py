from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from actionvim.forms import UserChangeForm, UserCreationForm
from actionvim.models import User, Project, Permission, Section, Task, TaskMember


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["username", "email", "first_name", "role"]
    list_filter = ["role"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name"]}),
        ("Permissions", {"fields": ["role"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "email", "first_name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


class PermissionAdmin(admin.TabularInline):
    model = Permission
    extra = 0


class SectionInlineAdmin(admin.StackedInline):
    model = Section
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["public_id", "task_count", "is_public", "created_at"]
    inlines = [PermissionAdmin, SectionInlineAdmin]


class TaskInlineAdmin(admin.StackedInline):
    model = Task
    extra = 0


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ["project", "title", "position", "created_at"]
    inlines = [TaskInlineAdmin]


class TaskMemberInline(admin.StackedInline):
    model = TaskMember
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["public_id", "project", "title", "created_at"]
    inlines = [TaskMemberInline]


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
