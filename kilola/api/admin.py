from django.contrib import admin
from .models import Crop, Farm, Batch, Farmer, Buyer, BatchReservation


class CropAdmin(admin.ModelAdmin):
    pass


class FarmAdmin(admin.ModelAdmin):
    pass


class FarmerAdmin(admin.ModelAdmin):
    pass


class BatchAdmin(admin.ModelAdmin):
    pass


class BuyerAdmin(admin.ModelAdmin):
    pass


class BatchReservationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Crop, CropAdmin)
admin.site.register(Farm, FarmAdmin)
admin.site.register(Batch, BatchAdmin)
admin.site.register(Farmer, FarmerAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(BatchReservation, BatchReservationAdmin)