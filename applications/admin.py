from django.contrib import admin
from .models import (Application, Applicant, PrimaryParent,
                    SecondaryParent, Address, SchoolYear)
# Register your models here.

admin.site.register(Application)
admin.site.register(SchoolYear)
admin.site.register(Applicant)
admin.site.register(Address)
admin.site.register(PrimaryParent)
admin.site.register(SecondaryParent)
