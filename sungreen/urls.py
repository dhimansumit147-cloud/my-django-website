"""
URL configuration for sungreen project.
"""

from django.contrib import admin
from django.urls import path
from sungreen_solar import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    # =====================================================
    # CUSTOM ADMIN CONTACT
    # =====================================================

    path(
        "admin/contact/",
        views.admin_contacts,
        name="admin-contact"
    ),

    path(
        "admin/contact/<int:pk>/",
        views.admin_contact_detail,
        name="admin-contact-detail"
    ),

    path(
        "admin/contact/<int:pk>/delete/",
        views.admin_contact_delete,
        name="admin-contact-delete"
    ),


    # =====================================================
    # USER MANAGEMENT
    # IMPORTANT:
    # These URLs MUST come before Django admin/
    # =====================================================

    # ALL USERS
    path(
        "admin/users/",
        views.all_users,
        name="all-users"
    ),

    # ADD USER
    path(
        "admin/users/add/",
        views.add_user,
        name="add-user"
    ),

    # USER DETAILS
    path(
        "admin/users/<int:user_id>/",
        views.user_details,
        name="user-details"
    ),

    # EDIT USER
    path(
        "admin/users/<int:user_id>/edit/",
        views.edit_user,
        name="edit-user"
    ),

    # DELETE USER
    path(
        "admin/users/<int:user_id>/delete/",
        views.delete_user,
        name="delete-user"
    ),


    # =====================================================
    # CUSTOM ADMIN FORGOT PASSWORD
    # =====================================================

    path(
        "admin/forgot-password/",
        views.admin_forgot_password,
        name="admin_forgot_password"
    ),

    path(
        "admin-verify-otp/",
        views.admin_verify_otp,
        name="admin_verify_otp"
    ),

    path(
        "admin-new-password/",
        views.admin_new_password,
        name="admin_new_password"
    ),

    path(
        "admin-resend-otp/",
        views.admin_resend_otp,
        name="admin_resend_otp"
    ),


    # =====================================================
    # WEBSITE
    # =====================================================

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "residential-solar/",
        views.residential_solar,
        name="residential_solar"
    ),

    path(
        "commercial-solar/",
        views.commercial_solar,
        name="commercial_solar"
    ),

    path(
        "hybrid-solar-system/",
        views.hybrid_solar_system,
        name="hybrid_solar_system"
    ),

    path(
        "solar-maintenance/",
        views.solar_maintenance,
        name="solar_maintenance"
    ),


    # =====================================================
    # CONTACT
    # =====================================================

    path(
        "contact/",
        views.contact,
        name="contact"
    ),


    # =====================================================
    # ADMIN LOGIN
    # =====================================================

    path(
        "admin-login/",
        views.admin_login,
        name="admin-login"
    ),

    path(
        "admin-panel/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "logout/",
        views.admin_logout,
        name="logout"
    ),


    # =====================================================
    # ADMIN SLIDER
    # =====================================================

    path(
        "admin-slider/",
        views.admin_slider,
        name="admin-slider"
    ),

    path(
        "add-slider/",
        views.add_slider,
        name="add-slider"
    ),

    path(
        "edit-slider/<int:id>/",
        views.edit_slider,
        name="edit-slider"
    ),

    path(
        "delete-slider/<int:id>/",
        views.delete_slider,
        name="delete-slider"
    ),


    # =====================================================
    # SOLAR PANELS ADMIN
    # =====================================================

    # ADD SOLAR PRODUCT
    path(
        "solar-panels/add/",
        views.add_solar_product,
        name="add_solar_product"
    ),

    # MANAGE SOLAR PRODUCTS
    path(
        "solar-panels/",
        views.solar_panels,
        name="solar_panels"
    ),

    # EDIT SOLAR PRODUCT
    path(
        "solar-panels/edit/<int:id>/",
        views.edit_solar_product,
        name="edit_solar_product"
    ),

    # DELETE SOLAR PRODUCT
    path(
        "solar-panels/delete/<int:id>/",
        views.delete_solar_product,
        name="delete_solar_product"
    ),

    # DELETE SOLAR PRODUCT IMAGE
    path(
        "solar-panels/image/delete/<int:image_id>/",
        views.delete_solar_product_image,
        name="delete_solar_product_image"
    ),

    # DELETE SOLAR PRODUCT PDF
    path(
        "solar-panels/pdf/delete/<int:id>/",
        views.delete_solar_product_pdf,
        name="delete_solar_product_pdf"
    ),


    # =====================================================
    # SOLAR MODULES PUBLIC PAGE
    # =====================================================

    path(
        "solar-modules/",
        views.solar_modules,
        name="solar_modules"
    ),


    # =====================================================
    # SOLAR INVERTER ADMIN
    # =====================================================

    # ADD SOLAR INVERTER
    path(
        "admin-inverter/add/",
        views.add_solar_inverter,
        name="add_solar_inverter"
    ),

    # MANAGE SOLAR INVERTERS
    path(
        "admin-inverter/",
        views.solar_inverters,
        name="solar_inverters"
    ),

    # EDIT SOLAR INVERTER
    path(
        "admin-inverter/edit/<int:id>/",
        views.edit_solar_inverter,
        name="edit_solar_inverter"
    ),

    # DELETE SOLAR INVERTER
    path(
        "admin-inverter/delete/<int:id>/",
        views.delete_solar_inverter,
        name="delete_solar_inverter"
    ),


    # =====================================================
    # SOLAR INVERTERS PUBLIC PAGE
    # =====================================================

    path(
        "solar-inverters/",
        views.solar_inverters_page,
        name="solar_inverters_page"
    ),

    path(
        "solar-inverters/<int:id>/",
        views.solar_inverter_detail,
        name="solar_inverter_detail"
    ),


    # =====================================================
    # BATTERY STORAGE ADMIN
    # =====================================================

    # ADD BATTERY STORAGE
    path(
        "admin-battery-storage/add/",
        views.add_battery_storage,
        name="add_battery_storage"
    ),

    # MANAGE BATTERY STORAGE
    path(
        "admin-battery-storage/",
        views.battery_storage,
        name="battery_storage"
    ),

    # EDIT BATTERY STORAGE
    path(
        "admin-battery-storage/edit/<int:product_id>/",
        views.edit_battery_storage,
        name="edit_battery_storage"
    ),

    # DELETE BATTERY STORAGE
    path(
        "admin-battery-storage/delete/<int:product_id>/",
        views.delete_battery_storage,
        name="delete_battery_storage"
    ),


    # =====================================================
    # PUBLIC BATTERY STORAGE
    # =====================================================

    path(
        "battery-storage/",
        views.public_battery_storage,
        name="public_battery_storage"
    ),


    # =====================================================
    # CUSTOMER REVIEWS
    # =====================================================

    # SUBMIT REVIEW
    path(
        "submit-review/",
        views.submit_review,
        name="submit_review"
    ),

    # MANAGE REVIEWS
    path(
        "admin-reviews/",
        views.admin_reviews,
        name="admin-reviews"
    ),

    # APPROVE REVIEW
    path(
        "admin-reviews/approve/<int:review_id>/",
        views.approve_review,
        name="approve-review"
    ),

    # REJECT REVIEW
    path(
        "admin-reviews/reject/<int:review_id>/",
        views.reject_review,
        name="reject-review"
    ),

    # DELETE REVIEW
    path(
        "admin-reviews/delete/<int:review_id>/",
        views.delete_review,
        name="delete-review"
    ),


    # =====================================================
    # PUBLIC - MOUNTING KITS
    # =====================================================

    path(
        "mounting-kits/",
        views.public_mounting_kits,
        name="public_mounting_kits"
    ),

    path(
        "mounting-kits/<int:id>/",
        views.mounting_kit_detail,
        name="mounting_kit_detail"
    ),


    # =====================================================
    # ADMIN - MOUNTING KITS
    # IMPORTANT:
    # THESE MUST COME BEFORE Django admin/
    # =====================================================

    # MANAGE MOUNTING KITS
    path(
        "admin/mounting-kits/",
        views.mounting_kits,
        name="mounting_kits"
    ),

    # ADD MOUNTING KIT
    path(
        "admin/mounting-kits/add/",
        views.add_mounting_kit,
        name="add_mounting_kit"
    ),

    # EDIT MOUNTING KIT
    path(
        "admin/mounting-kits/edit/<int:product_id>/",
        views.edit_mounting_kit,
        name="edit_mounting_kit"
    ),

    # DELETE MOUNTING KIT
    path(
        "admin/mounting-kits/delete/<int:product_id>/",
        views.delete_mounting_kit,
        name="delete_mounting_kit"
    ),

    # DELETE MOUNTING KIT IMAGE
    path(
        "admin/mounting-kits/image/delete/<int:image_id>/",
        views.delete_mounting_kit_image,
        name="delete_mounting_kit_image"
    ),

    # DELETE MOUNTING KIT PDF
    path(
        "admin/mounting-kits/pdf/delete/<int:pdf_id>/",
        views.delete_mounting_kit_pdf,
        name="delete_mounting_kit_pdf"
    ),


    # =====================================================
    # PUBLIC - EV CHARGERS
    # =====================================================

    path(
        "ev-chargers/",
        views.public_ev_chargers,
        name="public_ev_chargers"
    ),

    path(
        "ev-chargers/<int:id>/",
        views.ev_charger_detail,
        name="ev_charger_detail"
    ),


    # =====================================================
    # ADMIN - EV CHARGERS
    # IMPORTANT:
    # THESE MUST COME BEFORE Django admin/
    # =====================================================

    # MANAGE EV CHARGERS
    path(
        "admin/ev-chargers/",
        views.ev_chargers,
        name="ev_chargers"
    ),

    # ADD EV CHARGER
    path(
        "admin/ev-chargers/add/",
        views.add_ev_charger,
        name="add_ev_charger"
    ),

    # EDIT EV CHARGER
    path(
        "admin/ev-chargers/edit/<int:product_id>/",
        views.edit_ev_charger,
        name="edit_ev_charger"
    ),

    # DELETE EV CHARGER
    path(
        "admin/ev-chargers/delete/<int:product_id>/",
        views.delete_ev_charger,
        name="delete_ev_charger"
    ),

    # DELETE EV CHARGER IMAGE
    path(
        "admin/ev-chargers/image/delete/<int:image_id>/",
        views.delete_ev_charger_image,
        name="delete_ev_charger_image"
    ),

    # DELETE EV CHARGER PDF
    path(
        "admin/ev-chargers/pdf/delete/<int:pdf_id>/",
        views.delete_ev_charger_pdf,
        name="delete_ev_charger_pdf"
    ),


    # =====================================================
    # DJANGO ADMIN
    # IMPORTANT:
    # MUST BE LAST AMONG admin/ URLS
    # =====================================================

    path(
        "admin/",
        admin.site.urls
    ),

]


# =========================================================
# MEDIA FILES
# =========================================================

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
