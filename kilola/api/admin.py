from django.contrib import admin
from .models import Crop, Farm, Batch, BuyerProfile, BatchReservation


class CropAdmin(admin.ModelAdmin):
    pass


class FarmAdmin(admin.ModelAdmin):
    pass


class BatchAdmin(admin.ModelAdmin):
    pass


class BuyerProfileAdmin(admin.ModelAdmin):
    pass


class BatchReservationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Crop, CropAdmin)
admin.site.register(Farm, FarmAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(BuyerProfile, BuyerProfileAdmin)
admin.site.register(BatchReservation, BatchReservationAdmin)
