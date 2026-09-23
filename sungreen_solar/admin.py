from django.contrib import admin

from .models import (
    BatteryStorage,
    BatteryStorageImage,
    BatteryStoragePDF,
)


# =========================================================
# BATTERY STORAGE IMAGE INLINE
# =========================================================

class BatteryStorageImageInline(admin.TabularInline):

    model = BatteryStorageImage

    extra = 1


# =========================================================
# BATTERY STORAGE PDF INLINE
# =========================================================

class BatteryStoragePDFInline(admin.TabularInline):

    model = BatteryStoragePDF

    extra = 1


# =========================================================
# BATTERY STORAGE ADMIN
# =========================================================

@admin.register(BatteryStorage)
class BatteryStorageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "category",
        "name1",
        "name2",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "category",
        "name1",
        "name2",
        "description",
    )

    list_filter = (
        "category",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = (
        BatteryStorageImageInline,
        BatteryStoragePDFInline,
    )


# =========================================================
# BATTERY STORAGE IMAGE ADMIN
# =========================================================

@admin.register(BatteryStorageImage)
class BatteryStorageImageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "image",
        "created_at",
    )

    search_fields = (
        "product__name1",
        "product__category",
    )

    ordering = (
        "-created_at",
    )


# =========================================================
# BATTERY STORAGE PDF ADMIN
# =========================================================

@admin.register(BatteryStoragePDF)
class BatteryStoragePDFAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "title",
        "pdf",
        "created_at",
    )

    search_fields = (
        "product__name1",
        "product__category",
        "title",
    )

    ordering = (
        "-created_at",
    )
