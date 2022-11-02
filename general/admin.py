from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from import_export import resources
from import_export.admin import ExportActionMixin
from . models import Contact, SiteDetail, Suscriber

class SiteDetailAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General', {
            'fields': (
                'name', 'email', 'phone', 'address', 'timestamp'
            ),
        }),
        ('Social', {
            'fields': (
                'twitter', 'facebook', 'linkedin', 'instagram', 'youtube'
            ),
        })
    )

    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        tzname = request.session.get('django_timezone')
        print(tzname)
        if self.model.objects.all().count() == 1:
            obj = self.model.objects.all()[0]
            return HttpResponseRedirect(reverse("admin:%s_%s_change" %(self.model._meta.app_label, self.model._meta.model_name), args=(obj.id,)))
        return super(SiteDetailAdmin, self).changelist_view(request=request, extra_context=extra_context)

class SuscriberResource(resources.ModelResource):
    class Meta:
        model = Suscriber
        fields = ['email']
    
    def after_export(self, queryset, data, *args, **kwargs):
        queryset.update(exported=True)
        return queryset

class SuscriberAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['email', 'exported', 'timestamp']
    list_filter = ['email', 'exported', 'timestamp']
    resource_class = SuscriberResource

    fieldsets = (
        ('General', {
            'fields': (
                'email', 'exported', 'timestamp'
            ),
        }),
    )

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'timestamp']
    list_filter = ['name', 'email', 'subject', 'timestamp']

    fieldsets = (
        ('General', {
            'fields': (
                'name', 'email', 'subject', 'message', 'timestamp'
            ),
        }),
    )


admin.site.register(SiteDetail, SiteDetailAdmin)
admin.site.register(Suscriber, SuscriberAdmin)
admin.site.register(Contact, ContactAdmin)
