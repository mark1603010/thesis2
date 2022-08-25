from django.contrib import admin
from home.models import *
# Register your models here.
from django.conf import settings
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
from django_summernote.admin import SummernoteModelAdmin

admin.site.site_header = "MUSEO Tu' Agusan"
admin.site.site_title = "MUSEO Tu' Agusan Portal"
admin.site.index_title = "MUSEO Tu' Agusan Portal"

admin.site.register(Category)


#user
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username',)
    list_display = ('username', 'email', 'first_name', 'last_name', 'gender', 'address')
admin.site.register(User, UserAdmin)

# class DestinationAdmin(admin.ModelAdmin):
#     search_fields = ('title','address')
#     list_display = ('title','num_likes','num_comments')
#     list_filter = ('category',)
#
#     # fieldsets = (
#     #     (None, {
#     #         'fields': ('title', 'lat', 'long',)
#     #     }),
#     # )
#
#     formfield_overrides = {
#         map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
#     }

class DestinationAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    search_fields = ('title', 'address')
    list_display = ('title', 'num_likes', 'num_comments')
    list_filter = ('category',)

    # fieldsets = (
    #     (None, {
    #         'fields': ('title', 'lat', 'long',)
    #     }),
    # )

    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }

admin.site.register(Destination, DestinationAdmin)


#amenities
class AmenityAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'date_created')
admin.site.register(Amenity, AmenityAdmin)

#destination amenities
class DestinationAmenitiesAdmin(admin.ModelAdmin):
    search_fields = ('destination',)
    list_display = ('destination', 'amenity', 'date_created')
    list_filter = ('destination',)
admin.site.register(DestinationAmenities, DestinationAmenitiesAdmin)


#photo
class PhotoAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'photo', 'date_uploaded')
admin.site.register(Photo, PhotoAdmin)


# destination photos
class DestinationPhotosAdmin(admin.ModelAdmin):
    search_fields = ('destination',)
    list_display = ('destination', 'photo', 'date_created')
    list_filter = ('destination',)
admin.site.register(DestinationPhotos, DestinationPhotosAdmin)


#featured
class FeaturedAdmin(admin.ModelAdmin):
    search_fields = ('destination',)
    list_display = ('destination', 'date_created',)
admin.site.register(Featured, FeaturedAdmin)


#Tags
class TagAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'description', 'date_created')
admin.site.register(Tag, TagAdmin)

#Destination Tags
class DestinationTagsAdmin(admin.ModelAdmin):
    search_fields = ('destination',)
    list_display = ('destination', 'tag', 'date_tag')
    list_filter = ('destination',)
admin.site.register(DestinationTags, DestinationTagsAdmin)


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('commenter', 'message')
    list_display = ('commenter', 'message', 'date_created')
    list_filter = ('commenter',)

admin.site.register(Comment, CommentAdmin)

class ReportCommentAdmin(admin.ModelAdmin):
    search_fields = ('comment', 'reason')
    list_display = ('comment', 'reason', 'report_by', 'date_created', 'destination')
    list_filter = ('date_created', )

admin.site.register(ReportComment, ReportCommentAdmin)

admin.site.register(Reaction)
