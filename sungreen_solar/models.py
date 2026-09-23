from django.db import models


# =========================================================
# PAGE MODEL
# =========================================================

class Page(models.Model):

    title = models.CharField(
        max_length=200
    )

    content = models.TextField()

    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================================================
# SERVICE MODEL
# =========================================================

class Service(models.Model):

    name = models.CharField(
        max_length=200
    )

    description = models.TextField()

    def __str__(self):
        return self.name


# =========================================================
# SLIDER MODEL
# =========================================================

class Slider(models.Model):

    title = models.CharField(
        max_length=200
    )

    subtitle = models.CharField(
        max_length=300,
        blank=True
    )

    image = models.ImageField(
        upload_to="slider/"
    )

    button_text = models.CharField(
        max_length=100,
        default="Learn More"
    )

    button_link = models.CharField(
        max_length=200,
        default="#"
    )

    status = models.BooleanField(
        default=True
    )

    created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================================================
# CONTACT MESSAGE MODEL
# =========================================================

class ContactMessage(models.Model):

    SERVICE_CHOICES = [

        (
            "residential-solar",
            "Residential Solar"
        ),

        (
            "commercial-solar",
            "Commercial Solar"
        ),

        (
            "solar-maintenance",
            "Solar Maintenance"
        ),

        (
            "solar-battery",
            "Solar Battery Storage"
        ),

        (
            "solar-support",
            "Solar Support"
        ),

        (
            "other",
            "Other Enquiry"
        ),

    ]

    # -----------------------------------------------------
    # CUSTOMER INFORMATION
    # -----------------------------------------------------

    name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30
    )


    # -----------------------------------------------------
    # ENQUIRY INFORMATION
    # -----------------------------------------------------

    subject = models.CharField(
        max_length=255,
        blank=True
    )

    service = models.CharField(
        max_length=100,
        choices=SERVICE_CHOICES,
        blank=True
    )

    message = models.TextField()


    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    is_read = models.BooleanField(
        default=False
    )


    # -----------------------------------------------------
    # DATE / TIME
    # -----------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

    class Meta:

        ordering = [
            "-created_at"
        ]

        verbose_name = "Contact Message"

        verbose_name_plural = "Contact Messages"


    # -----------------------------------------------------
    # STRING REPRESENTATION
    # -----------------------------------------------------

    def __str__(self):

        return f"{self.name} - {self.email}"


from django.db import models
from django.utils import timezone


# =========================================================
# SOLAR PRODUCT
# =========================================================

# =========================================================
# SOLAR PRODUCT
# =========================================================

class SolarProduct(models.Model):

    category = models.CharField(
        max_length=100,
    )

    name1 = models.CharField(
        max_length=200
    )

    name2 = models.CharField(
        max_length=200,
        blank=True
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):
        return self.name1


# =========================================================
# SOLAR PRODUCT IMAGES
# =========================================================

class SolarProductImage(models.Model):

    product = models.ForeignKey(
        SolarProduct,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="solar_products/images/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.product.name1


# =========================================================
# SOLAR PRODUCT PDF / BROCHURES
# =========================================================

class SolarProductPDF(models.Model):

    product = models.ForeignKey(
        SolarProduct,
        on_delete=models.CASCADE,
        related_name="pdfs"
    )

    title = models.CharField(
        max_length=255,
        default="Product Brochure"
    )

    pdf = models.FileField(
        upload_to="solar_products/pdfs/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.product.name1} - {self.title}"

# =====================================================
# SOLAR INVERTER
# =====================================================

from django.db import models


class SolarInverter(models.Model):

    category = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    name1 = models.CharField(
        max_length=200
    )

    name2 = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name1


class SolarInverterImage(models.Model):

    inverter = models.ForeignKey(
        SolarInverter,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="solar_inverters/images/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.inverter.name1


class SolarInverterPDF(models.Model):

    inverter = models.ForeignKey(
        SolarInverter,
        on_delete=models.CASCADE,
        related_name="pdfs"
    )

    # PDF TITLE
    title = models.CharField(
        max_length=255,
        default="PDF Document"
    )

    # PDF FILE
    pdf = models.FileField(
        upload_to="solar_inverters/pdfs/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


from django.db import models
from django.utils import timezone




from django.db import models


class BatteryStorage(models.Model):

    category = models.CharField(
        max_length=200,
        blank=False
    )

    name1 = models.CharField(
        max_length=255,
        blank=False
    )

    name2 = models.CharField(
        max_length=255,
        blank=True
    )

    description = models.TextField(
        blank=False
    )

    # Optional old/main image field
    image = models.ImageField(
        upload_to="battery_storage/",
        blank=True,
        null=True
    )

    # Optional old/main PDF field
    pdf = models.FileField(
        upload_to="battery_storage/pdfs/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name1


class BatteryStorageImage(models.Model):

    product = models.ForeignKey(
        BatteryStorage,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="battery_storage/images/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.product.name1


class BatteryStoragePDF(models.Model):

    product = models.ForeignKey(
        BatteryStorage,
        on_delete=models.CASCADE,
        related_name="pdfs"
    )

    pdf = models.FileField(
        upload_to="battery_storage/pdfs/"
    )

    title = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title or self.pdf.name



from django.db import models


class Review(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField(blank=True, null=True)

    rating = models.PositiveIntegerField(
        choices=[
            (1, "1 Star"),
            (2, "2 Stars"),
            (3, "3 Stars"),
            (4, "4 Stars"),
            (5, "5 Stars"),
        ]
    )

    review = models.TextField()

    status = models.BooleanField(
        default=False,
        help_text="Only approved reviews will appear on the website."
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.name} - {self.rating} Stars"
    
    
    
    
from django.db import models


class MountingKit(models.Model):

    name1 = models.CharField(
        max_length=255,
        verbose_name="Product Name"
    )

    name2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Product Subtitle"
    )

    category = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="mounting_kits/",
        blank=True,
        null=True
    )

    pdf = models.FileField(
        upload_to="mounting_kits/pdfs/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name1


class MountingKitImage(models.Model):

    product = models.ForeignKey(
        MountingKit,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="mounting_kits/images/"
    )

    def __str__(self):
        return self.product.name1


class MountingKitPDF(models.Model):

    product = models.ForeignKey(
        MountingKit,
        on_delete=models.CASCADE,
        related_name="pdfs"
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    pdf = models.FileField(
        upload_to="mounting_kits/pdfs/"
    )

    def __str__(self):
        return self.title or self.product.name1




# =========================================================
# EV CHARGER
# =========================================================

class EVCharger(models.Model):

    name1 = models.CharField(
        max_length=255,
        verbose_name="Product Name"
    )

    name2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Product Subtitle"
    )

    category = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to="ev_chargers/",
        blank=True,
        null=True
    )

    pdf = models.FileField(
        upload_to="ev_chargers/pdfs/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name1


# =========================================================
# EV CHARGER IMAGES
# =========================================================

class EVChargerImage(models.Model):

    product = models.ForeignKey(
        EVCharger,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(
        upload_to="ev_chargers/images/"
    )

    def __str__(self):
        return self.product.name1


# =========================================================
# EV CHARGER PDFs
# =========================================================

class EVChargerPDF(models.Model):

    product = models.ForeignKey(
        EVCharger,
        on_delete=models.CASCADE,
        related_name="pdfs"
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    pdf = models.FileField(
        upload_to="ev_chargers/pdfs/"
    )

    def __str__(self):
        return self.title or self.product.name1
