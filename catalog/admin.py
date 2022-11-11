from django.contrib import admin
from . import models

# Register your models here.
# admin.site.register(models.Book)
# admin.site.register(models.Author)
admin.site.register(models.Genre)
admin.site.register(models.Language)
# admin.site.register(models.BookInstance)

class BooksInstanceInline(admin.TabularInline):
    model = models.BookInstance

class BookInline(admin.TabularInline):
    model = models.Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name',  ('date_of_birth', 'date_of_death')]

    inlines = [BookInline]

admin.site.register(models.Author, AuthorAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    list_filter = ('language','author')

    inlines = [BooksInstanceInline]
    # pass

admin.site.register(models.Book, BookAdmin)

class BookInstanceAdmin(admin.ModelAdmin):
    # list_display = ('book', 'status', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint','id')
        }),
        ('Availability', {
            'fields': ('status','due_back', 'borrower')
        }),
    )
    # pass

admin.site.register(models.BookInstance, BookInstanceAdmin)