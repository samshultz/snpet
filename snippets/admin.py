from django.contrib import admin
from .models import Language, Category, Snippet


class LanguageAdmin(admin.ModelAdmin):
    list_display = 'name', 'language_mode', 'total_users'

    def total_users(self, obj):
        return obj.users.count()
    total_users.short_description = "Total Users"

admin.site.register(Language, LanguageAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name', 'slug'
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


class SnippetAdmin(admin.ModelAdmin):
    list_display = 'title', 'language', 'author', 'total_upvotes', 'total_downvotes', "total_bookmarks"
    radio_fields = {'language': admin.HORIZONTAL}
    list_filter = 'title', 'language', 'category', 'author', 'created'
    search_fields = 'title', 'language', 'category', 'author'
    ordering = 'title', 'created', 'language'
    save_on_top = True
    filter_horizontal = ['upvotes', 'downvotes', 'bookmarks']

    def total_upvotes(self, obj):
        return obj.upvotes.count()
    total_upvotes.short_description = "Upvotes"

    def total_downvotes(self, obj):
        return obj.downvotes.count()
    total_downvotes.short_description = "Downvotes"

    def total_bookmarks(self, obj):
        return obj.bookmarks.count()
    total_bookmarks.short_description = "Bookmarks"


    


admin.site.register(Snippet, SnippetAdmin)