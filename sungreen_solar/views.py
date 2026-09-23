from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.html import escape

from .models import (
    Page,
    Service,
    Slider,
    ContactMessage,
    SolarProduct,
    SolarInverter,
    SolarInverterImage,
    SolarInverterPDF,
    BatteryStorage,
)



from django.shortcuts import render

from .models import Slider, Review


def home(request):

    sliders = Slider.objects.filter(
        status=True
    ).order_by("-created")

    reviews = Review.objects.filter(
        status=True
    ).order_by("-created")

    return render(
        request,
        "home.html",
        {
            "sliders": sliders,
            "reviews": reviews,
        }
    )


def submit_review(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        rating = request.POST.get("rating")
        review_text = request.POST.get("review", "").strip()
        if not name or not rating or not review_text:
            return redirect("home")

        Review.objects.create(
            name=name,
            email=email if email else None,
            rating=int(rating),
            review=review_text,
            status=False
        )

        return redirect("home")

    return redirect("home")

# =========================================================
# ADMIN LOGIN
# =========================================================

def admin_login(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect("dashboard")

        return render(
            request,
            "admin/login.html",
            {
                "error": "Invalid Username or Password"
            }
        )

    return render(
        request,
        "admin/login.html"
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from .models import (
    SolarProduct,
    SolarInverter,
    BatteryStorage,
    ContactMessage,
    MountingKit,
    EVCharger,
)


@login_required(login_url="/admin-login/")
def dashboard(request):

    # =========================================================
    # PRODUCT COUNTS
    # =========================================================

    total_solar_modules = SolarProduct.objects.count()

    total_solar_inverters = SolarInverter.objects.count()

    total_battery_storage = BatteryStorage.objects.count()

    total_mounting_kits = MountingKit.objects.count()

    total_ev_chargers = EVCharger.objects.count()

    # =========================================================
    # CONTACT COUNTS
    # =========================================================

    total_contacts = ContactMessage.objects.count()

    unread_contacts = ContactMessage.objects.filter(
        is_read=False
    ).count()

    read_contacts = ContactMessage.objects.filter(
        is_read=True
    ).count()

    # =========================================================
    # USER COUNT
    # =========================================================

    total_users = User.objects.count()

    # =========================================================
    # DASHBOARD
    # =========================================================

    return render(
        request,
        "admin/dashboard.html",
        {
            "total_solar_modules": total_solar_modules,
            "total_solar_inverters": total_solar_inverters,
            "total_battery_storage": total_battery_storage,

            "total_mounting_kits": total_mounting_kits,
            "total_ev_chargers": total_ev_chargers,

            "total_contacts": total_contacts,
            "total_users": total_users,

            "unread_contacts": unread_contacts,
            "read_contacts": read_contacts,
        }
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@login_required(login_url="/admin-login/")
def admin_logout(request):

    logout(request)

    return redirect("admin-login")


# =========================================================
# ADMIN SLIDER LIST
# =========================================================

@login_required(login_url="/admin-login/")
def admin_slider(request):

    sliders = Slider.objects.all().order_by(
        "-created"
    )

    return render(
        request,
        "admin/admin_slider.html",
        {
            "sliders": sliders
        }
    )


# =========================================================
# ADD SLIDER
# =========================================================

@login_required(login_url="/admin-login/")
def add_slider(request):

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        subtitle = request.POST.get(
            "subtitle",
            ""
        ).strip()

        image = request.FILES.get(
            "image"
        )

        button_text = request.POST.get(
            "button_text",
            "Learn More"
        ).strip()

        button_link = request.POST.get(
            "button_link",
            "#"
        ).strip()

        if not title:

            messages.error(
                request,
                "Slider title is required."
            )

            return redirect("add-slider")

        if not image:

            messages.error(
                request,
                "Please select a slider image."
            )

            return redirect("add-slider")

        Slider.objects.create(
            title=title,
            subtitle=subtitle,
            image=image,
            button_text=button_text,
            button_link=button_link
        )

        messages.success(
            request,
            "Slider added successfully."
        )

        return redirect(
            "admin-slider"
        )

    return render(
        request,
        "admin/add_slider.html"
    )


# =========================================================
# EDIT SLIDER
# =========================================================

@login_required(login_url="/admin-login/")
def edit_slider(request, id):

    slider = get_object_or_404(
        Slider,
        id=id
    )

    if request.method == "POST":

        slider.title = request.POST.get(
            "title",
            ""
        ).strip()

        slider.subtitle = request.POST.get(
            "subtitle",
            ""
        ).strip()

        slider.button_text = request.POST.get(
            "button_text",
            "Learn More"
        ).strip()

        slider.button_link = request.POST.get(
            "button_link",
            "#"
        ).strip()

        image = request.FILES.get("image")

        if image:
            slider.image = image

        slider.status = bool(
            request.POST.get("status")
        )

        slider.save()

        messages.success(
            request,
            "Slider updated successfully."
        )

        return redirect(
            "admin-slider"
        )

    return render(
        request,
        "admin/edit_slider.html",
        {
            "slider": slider
        }
    )


# =========================================================
# DELETE SLIDER
# =========================================================

@login_required(login_url="/admin-login/")
def delete_slider(request, id):

    slider = get_object_or_404(
        Slider,
        id=id
    )

    if request.method == "POST":

        slider.delete()

        messages.success(
            request,
            "Slider deleted successfully."
        )

        return redirect("admin-slider")

    return redirect("admin-slider")


# =========================================================
# ABOUT
# =========================================================

def about(request):

    return render(
        request,
        "about.html"
    )


# =========================================================
# RESIDENTIAL SOLAR
# =========================================================

def residential_solar(request):

    return render(
        request,
        "residential-solar.html"
    )


# =========================================================
# COMMERCIAL SOLAR
# =========================================================

def commercial_solar(request):

    return render(
        request,
        "commercial-solar.html"
    )


# =========================================================
# HYBRID SOLAR SYSTEM
# =========================================================

def hybrid_solar_system(request):

    return render(
        request,
        "hybrid-solar-system.html"
    )


# =========================================================
# SOLAR MAINTENANCE
# =========================================================

def solar_maintenance(request):

    return render(
        request,
        "solar-maintenance.html"
    )


# =========================================================
# CONTACT PAGE
# =========================================================

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils.html import escape

from .models import ContactMessage


def contact(request):

    # =====================================================
    # GET REQUEST
    # =====================================================
    # Normal page open / refresh par koi new message nahi banega.
    # =====================================================

    if request.method != "POST":
        return render(
            request,
            "contact.html"
        )

    # =====================================================
    # GET FORM DATA
    # =====================================================

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    subject = request.POST.get("subject", "").strip()
    service = request.POST.get("service", "").strip()
    message_text = request.POST.get("message", "").strip()

    # =====================================================
    # VALIDATION
    # =====================================================

    if not name:
        messages.error(
            request,
            "Please enter your name.",
            extra_tags="contact-toast"
        )
        return redirect("contact")

    if not email:
        messages.error(
            request,
            "Please enter your email address.",
            extra_tags="contact-toast"
        )
        return redirect("contact")

    if not phone:
        messages.error(
            request,
            "Please enter your phone number.",
            extra_tags="contact-toast"
        )
        return redirect("contact")

    if not message_text:
        messages.error(
            request,
            "Please enter your message.",
            extra_tags="contact-toast"
        )
        return redirect("contact")

    # =====================================================
    # SAVE ENQUIRY
    # =====================================================

    try:

        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            service=service,
            message=message_text
        )

    except Exception as e:

        print("CONTACT SAVE ERROR:", e)

        messages.error(
            request,
            "We could not save your enquiry. Please try again.",
            extra_tags="contact-toast"
        )

        return redirect("contact")

    # =====================================================
    # SERVICE DISPLAY
    # =====================================================

    if contact_message.service:
        service_name = contact_message.get_service_display()
    else:
        service_name = "Not selected"

    # =====================================================
    # SAFE HTML VALUES
    # =====================================================

    safe_name = escape(contact_message.name)
    safe_email = escape(contact_message.email)
    safe_phone = escape(contact_message.phone)

    safe_subject = escape(
        contact_message.subject or "Not provided"
    )

    safe_service = escape(service_name)

    safe_message = escape(
        contact_message.message
    ).replace(
        "\n",
        "<br>"
    )

    safe_created_at = escape(
        str(contact_message.created_at)
    )

    # =====================================================
    # EMAIL SUBJECT
    # =====================================================

    admin_subject = (
        f"New Sungreen Solar Enquiry - "
        f"{contact_message.name}"
    )

    # =====================================================
    # PLAIN TEXT EMAIL
    # =====================================================

    plain_message = f"""
New Sungreen Solar Contact Enquiry

Name:
{contact_message.name}

Email:
{contact_message.email}

Phone:
{contact_message.phone}

Subject:
{contact_message.subject or "Not provided"}

Service:
{service_name}

Message:
{contact_message.message}

Submitted:
{contact_message.created_at}

----------------------------------

Sungreen Solar

Website Contact Enquiry Notification

Please respond to the customer at your earliest convenience.
"""

    # =====================================================
    # HTML EMAIL
    # =====================================================

    html_message = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>
Sungreen Solar - New Contact Enquiry
</title>

</head>

<body
style="
margin:0;
padding:0;
background:#eef3f0;
font-family:Arial,Helvetica,sans-serif;
color:#17231e;
"
>

<table
width="100%"
cellpadding="0"
cellspacing="0"
border="0"
style="
width:100%;
background:#eef3f0;
padding:30px 15px;
"
>

<tr>

<td align="center">

<table
width="100%"
cellpadding="0"
cellspacing="0"
border="0"
style="
width:100%;
max-width:620px;
background:#ffffff;
border-radius:18px;
overflow:hidden;
border:1px solid #dce6e0;
"
>

<!-- HEADER -->

<tr>

<td
style="
background:#0b2b1e;
padding:34px;
"
>

<div
style="
display:inline-block;
padding:6px 12px;
background:#173e2d;
border:1px solid #2a6047;
border-radius:30px;
color:#b8ed38;
font-size:9px;
font-weight:bold;
letter-spacing:2px;
"
>

SUNGREEN SOLAR

</div>

<h1
style="
margin:18px 0 7px 0;
color:#ffffff;
font-size:27px;
line-height:1.25;
"
>

New Contact Enquiry

</h1>

<p
style="
margin:0;
color:#c7d8d0;
font-size:13px;
line-height:1.6;
"
>

A new customer enquiry has been received
through your website.

</p>

</td>

</tr>


<!-- ATTENTION -->

<tr>

<td
style="
padding:18px 22px;
"
>

<div
style="
padding:11px 14px;
background:#f4f9e9;
border:1px solid #d9e9b7;
border-radius:10px;
color:#54721f;
font-size:11px;
font-weight:600;
"
>

✓ New enquiry requires your attention

</div>

</td>

</tr>


<!-- CONTENT -->

<tr>

<td
style="
padding:10px 30px 30px 30px;
"
>

<h2
style="
color:#14241d;
font-size:16px;
"
>

Customer Information

</h2>

<table
width="100%"
cellpadding="0"
cellspacing="0"
border="0"
style="
border:1px solid #dce5e0;
border-radius:12px;
overflow:hidden;
"
>

<tr>

<td
style="
padding:14px;
background:#f7f9f8;
color:#748079;
font-size:9px;
font-weight:bold;
"
>
NAME
</td>

<td
style="
padding:14px;
color:#25352e;
font-size:12px;
font-weight:600;
"
>
{safe_name}
</td>

</tr>


<tr>

<td
style="
padding:14px;
background:#f7f9f8;
color:#748079;
font-size:9px;
font-weight:bold;
"
>
EMAIL
</td>

<td
style="
padding:14px;
color:#518421;
font-size:12px;
font-weight:600;
"
>
{safe_email}
</td>

</tr>


<tr>

<td
style="
padding:14px;
background:#f7f9f8;
color:#748079;
font-size:9px;
font-weight:bold;
"
>
PHONE
</td>

<td
style="
padding:14px;
color:#25352e;
font-size:12px;
font-weight:600;
"
>
{safe_phone}
</td>

</tr>


<tr>

<td
style="
padding:14px;
background:#f7f9f8;
color:#748079;
font-size:9px;
font-weight:bold;
"
>
SERVICE
</td>

<td
style="
padding:14px;
color:#57821d;
font-size:12px;
font-weight:700;
"
>
{safe_service}
</td>

</tr>


<tr>

<td
style="
padding:14px;
background:#f7f9f8;
color:#748079;
font-size:9px;
font-weight:bold;
"
>
SUBJECT
</td>

<td
style="
padding:14px;
color:#25352e;
font-size:12px;
"
>
{safe_subject}
</td>

</tr>

</table>


<h2
style="
margin-top:30px;
color:#14241d;
font-size:16px;
"
>

Customer Message

</h2>


<div
style="
padding:18px 16px;
background:#f6f9f7;
border-left:3px solid #a9e635;
border-radius:10px;
color:#52605a;
font-size:12px;
line-height:1.8;
"
>

{safe_message}

</div>


<div
style="
margin-top:20px;
padding:16px;
background:#f6f9f7;
border-radius:10px;
"
>

<div
style="
color:#7b8781;
font-size:8px;
font-weight:bold;
letter-spacing:1px;
"
>

SUBMITTED

</div>

<div
style="
margin-top:5px;
color:#26362f;
font-size:10px;
font-weight:600;
"
>

{safe_created_at}

</div>

</div>

</td>

</tr>


<!-- FOOTER -->

<tr>

<td
style="
padding:25px 30px;
background:#061a13;
text-align:center;
"
>

<div
style="
color:#a9e635;
font-size:11px;
font-weight:800;
letter-spacing:1.5px;
"
>

SUNGREEN SOLAR

</div>

<div
style="
margin-top:7px;
color:#91a39a;
font-size:9px;
"
>

Website Contact Enquiry Notification

</div>

</td>

</tr>

</table>


<div
style="
max-width:620px;
margin:14px auto 0 auto;
text-align:center;
color:#8b9791;
font-size:9px;
"
>

This is an automated notification from the Sungreen Solar website.

</div>

</td>

</tr>

</table>

</body>

</html>
"""

    # =====================================================
    # SEND EMAIL
    # =====================================================

    email_sent = False

    try:

        email_message = EmailMultiAlternatives(
            subject=admin_subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[
                settings.CONTACT_ADMIN_EMAIL
            ],
            reply_to=[
                contact_message.email
            ]
        )

        email_message.attach_alternative(
            html_message,
            "text/html"
        )

        email_message.send(
            fail_silently=False
        )

        email_sent = True

    except Exception as e:

        print("EMAIL ERROR:", e)

    # =====================================================
    # SUCCESS / WARNING
    # =====================================================

    if email_sent:

        messages.success(
            request,
            "Your enquiry has been submitted successfully! "
            "Our team will contact you shortly.",
            extra_tags="contact-toast"
        )

    else:

        messages.warning(
            request,
            "Your enquiry was saved successfully, "
            "but the email notification could not be sent.",
            extra_tags="contact-toast"
        )

    # =====================================================
    # POST → REDIRECT → GET
    # =====================================================

    return redirect("contact")


# =========================================================
# ADMIN CONTACT LIST
# =========================================================

@login_required(login_url="/admin-login/")
def admin_contacts(request):

    contacts = ContactMessage.objects.all().order_by(
        "-created_at"
    )

    total_count = contacts.count()

    read_count = contacts.filter(
        is_read=True
    ).count()

    unread_count = contacts.filter(
        is_read=False
    ).count()

    return render(
        request,
        "admin/admin_contact.html",
        {
            "contacts": contacts,
            "total_count": total_count,
            "read_count": read_count,
            "unread_count": unread_count,
        }
    )


# =========================================================
# ADMIN CONTACT DETAIL
# =========================================================

@login_required(login_url="/admin-login/")
def admin_contact_detail(request, pk):

    contact = get_object_or_404(
        ContactMessage,
        pk=pk
    )

    if not contact.is_read:

        contact.is_read = True

        contact.save(
            update_fields=[
                "is_read"
            ]
        )

    return render(
        request,
        "admin/admin_contact_detail.html",
        {
            "contact": contact,
            "enquiry": contact,
        }
    )


# =========================================================
# DELETE CONTACT
# =========================================================

@login_required(login_url="/admin-login/")
def admin_contact_delete(request, pk):

    contact = get_object_or_404(
        ContactMessage,
        pk=pk
    )

    if request.method == "POST":

        contact.delete()

        messages.success(
            request,
            "Contact enquiry deleted successfully."
        )

    return redirect(
        "admin-contact"
    )


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import (
    SolarProduct,
    SolarProductImage,
    SolarProductPDF,
)



# =========================================================
# IMPORTS
# =========================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import (
    SolarProduct,
    SolarProductImage,
    SolarProductPDF,
)


# =========================================================
# SOLAR MODULE - PUBLIC
# =========================================================

def solar_modules(request):

    products = SolarProduct.objects.prefetch_related(
        "images",
        "pdfs"
    ).all().order_by("-id")

    return render(
        request,
        "solar_module.html",
        {
            "products": products
        }
    )


# =========================================================
# SOLAR MODULE - MANAGE
# =========================================================

@login_required(login_url="/admin-login/")
def solar_panels(request):

    products = SolarProduct.objects.prefetch_related(
        "images",
        "pdfs"
    ).all().order_by("-id")

    return render(
        request,
        "admin/solar_panels.html",
        {
            "products": products
        }
    )


# =========================================================
# ADD SOLAR PRODUCT
# =========================================================

@login_required(login_url="/admin-login/")
def add_solar_product(request):

    if request.method == "POST":

        # -------------------------------------------------
        # PRODUCT INFORMATION
        # -------------------------------------------------

        category = request.POST.get(
            "category",
            ""
        ).strip()

        name1 = request.POST.get(
            "name1",
            ""
        ).strip()

        name2 = request.POST.get(
            "name2",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not category:
            messages.error(
                request,
                "Solar product category is required."
            )

            return redirect(
                "add_solar_product"
            )

        if not name1:
            messages.error(
                request,
                "Solar product name is required."
            )

            return redirect(
                "add_solar_product"
            )

        if not description:
            messages.error(
                request,
                "Product description is required."
            )

            return redirect(
                "add_solar_product"
            )

        # -------------------------------------------------
        # CREATE MAIN PRODUCT
        # -------------------------------------------------

        product = SolarProduct.objects.create(
            category=category,
            name1=name1,
            name2=name2,
            description=description
        )

        # -------------------------------------------------
        # MULTIPLE IMAGES
        # -------------------------------------------------

        images = request.FILES.getlist(
            "images"
        )

        for image in images:

            if image:

                SolarProductImage.objects.create(
                    product=product,
                    image=image
                )

        # -------------------------------------------------
        # MULTIPLE PDFs
        # -------------------------------------------------

        pdfs = request.FILES.getlist(
            "pdfs"
        )

        pdf_titles = request.POST.getlist(
            "pdf_titles"
        )

        for index, pdf in enumerate(pdfs):

            if not pdf:
                continue

            # PDF title
            if index < len(pdf_titles):
                title = pdf_titles[index].strip()
            else:
                title = ""

            if not title:
                title = "Product Brochure"

            SolarProductPDF.objects.create(
                product=product,
                title=title,
                pdf=pdf
            )

        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        messages.success(
            request,
            "Solar product added successfully."
        )

        return redirect(
            "solar_panels"
        )

    # -----------------------------------------------------
    # GET REQUEST
    # -----------------------------------------------------

    return render(
        request,
        "admin/add_solar_product.html"
    )


# =========================================================
# EDIT SOLAR PRODUCT
# =========================================================

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    SolarProduct,
    SolarProductImage,
    SolarProductPDF,
)


# =========================================================
# EDIT SOLAR PRODUCT
# =========================================================

@login_required(login_url="/admin-login/")
def edit_solar_product(request, id):

    product = get_object_or_404(
        SolarProduct,
        id=id
    )

    # =====================================================
    # POST - UPDATE PRODUCT
    # =====================================================

    if request.method == "POST":

        # -------------------------------------------------
        # PRODUCT INFORMATION
        # -------------------------------------------------

        category = request.POST.get(
            "category",
            ""
        ).strip()

        name1 = request.POST.get(
            "name1",
            ""
        ).strip()

        name2 = request.POST.get(
            "name2",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not category:

            messages.error(
                request,
                "Solar product category is required."
            )

            return redirect(
                "edit_solar_product",
                id=product.id
            )

        if not name1:

            messages.error(
                request,
                "Solar product name is required."
            )

            return redirect(
                "edit_solar_product",
                id=product.id
            )

        if not description:

            messages.error(
                request,
                "Product description is required."
            )

            return redirect(
                "edit_solar_product",
                id=product.id
            )

        # -------------------------------------------------
        # UPDATE PRODUCT INFORMATION
        # -------------------------------------------------

        product.category = category
        product.name1 = name1
        product.name2 = name2
        product.description = description

        product.save()

        # =================================================
        # ADD NEW IMAGES
        # =================================================

        images = request.FILES.getlist(
            "images"
        )

        for image in images:

            if image:

                SolarProductImage.objects.create(
                    product=product,
                    image=image
                )

        # =================================================
        # ADD NEW PDFs
        # =================================================

        pdfs = request.FILES.getlist(
            "pdfs"
        )

        pdf_titles = request.POST.getlist(
            "pdf_titles"
        )

        for index, pdf in enumerate(pdfs):

            if not pdf:
                continue

            # ---------------------------------------------
            # Get matching PDF title
            # ---------------------------------------------

            if index < len(pdf_titles):

                title = pdf_titles[index].strip()

            else:

                title = ""

            # ---------------------------------------------
            # Default title
            # ---------------------------------------------

            if not title:

                title = "Product Brochure"

            # ---------------------------------------------
            # Create PDF record
            # ---------------------------------------------

            SolarProductPDF.objects.create(
                product=product,
                title=title,
                pdf=pdf
            )

        # =================================================
        # SUCCESS
        # =================================================

        messages.success(
            request,
            "Solar product updated successfully."
        )

        return redirect(
            "solar_panels"
        )

    # =====================================================
    # GET - EDIT PAGE
    # =====================================================

    images = product.images.all()

    pdfs = product.pdfs.all()

    return render(
        request,
        "admin/edit_solar_product.html",
        {
            "product": product,
            "images": images,
            "pdfs": pdfs,
        }
    )


# =========================================================
# DELETE SOLAR PRODUCT IMAGE
# =========================================================

@login_required(login_url="/admin-login/")
def delete_solar_product_image(request, image_id):

    image = get_object_or_404(
        SolarProductImage,
        id=image_id
    )

    # -----------------------------------------------------
    # Save product ID before deleting image
    # -----------------------------------------------------

    product_id = image.product.id

    # -----------------------------------------------------
    # Only allow POST
    # -----------------------------------------------------

    if request.method != "POST":

        messages.error(
            request,
            "Invalid request method."
        )

        return redirect(
            "edit_solar_product",
            id=product_id
        )

    # -----------------------------------------------------
    # Delete actual image file
    # -----------------------------------------------------

    if image.image:

        image.image.delete(
            save=False
        )

    # -----------------------------------------------------
    # Delete database record
    # -----------------------------------------------------

    image.delete()

    # -----------------------------------------------------
    # Success message
    # -----------------------------------------------------

    messages.success(
        request,
        "Product image deleted successfully."
    )

    # -----------------------------------------------------
    # Return to edit page
    # -----------------------------------------------------

    return redirect(
        "edit_solar_product",
        id=product_id
    )


# =========================================================
# DELETE SOLAR PRODUCT PDF
# =========================================================

@login_required(login_url="/admin-login/")
def delete_solar_product_pdf(request, pdf_id):

    pdf = get_object_or_404(
        SolarProductPDF,
        id=pdf_id
    )

    # -----------------------------------------------------
    # Save product ID before deleting PDF
    # -----------------------------------------------------

    product_id = pdf.product.id

    # -----------------------------------------------------
    # Only allow POST
    # -----------------------------------------------------

    if request.method != "POST":

        messages.error(
            request,
            "Invalid request method."
        )

        return redirect(
            "edit_solar_product",
            id=product_id
        )

    # -----------------------------------------------------
    # Delete actual PDF file
    # -----------------------------------------------------

    if pdf.pdf:

        pdf.pdf.delete(
            save=False
        )

    # -----------------------------------------------------
    # Delete database record
    # -----------------------------------------------------

    pdf.delete()

    # -----------------------------------------------------
    # Success message
    # -----------------------------------------------------

    messages.success(
        request,
        "Product PDF deleted successfully."
    )

    # -----------------------------------------------------
    # Return to edit page
    # -----------------------------------------------------

    return redirect(
        "edit_solar_product",
        id=product_id
    )


# =========================================================
# DELETE SOLAR PRODUCT
# =========================================================

@login_required(login_url="/admin-login/")
def delete_solar_product(request, id):

    product = get_object_or_404(
        SolarProduct,
        id=id
    )

    # -----------------------------------------------------
    # Only allow POST
    # -----------------------------------------------------

    if request.method != "POST":

        messages.error(
            request,
            "Invalid request method."
        )

        return redirect(
            "solar_panels"
        )

    # -----------------------------------------------------
    # Delete product
    #
    # If SolarProductImage and SolarProductPDF have
    # ForeignKey(..., on_delete=models.CASCADE), their
    # database records will also be deleted automatically.
    # -----------------------------------------------------

    product.delete()

    # -----------------------------------------------------
    # Success message
    # -----------------------------------------------------

    messages.success(
        request,
        "Solar product deleted successfully."
    )

    # -----------------------------------------------------
    # Return to products page
    # -----------------------------------------------------

    return redirect(
        "solar_panels"
    )




# =========================================================
# SOLAR INVERTERS - MANAGE
# =========================================================
@login_required(login_url="/admin-login/")
def solar_inverters(request):

    # Selected category
    selected_category = request.GET.get(
        "category",
        ""
    ).strip()

    # All categories
    categories = (
        SolarInverter.objects
        .exclude(category__isnull=True)
        .exclude(category__exact="")
        .values_list(
            "category",
            flat=True
        )
        .distinct()
        .order_by("category")
    )

    # All products
    products = (
        SolarInverter.objects
        .prefetch_related(
            "images",
            "pdfs"
        )
        .all()
        .order_by("-id")
    )

    # Category filter
    if selected_category:

        products = products.filter(
            category=selected_category
        )


    return render(
        request,
        "admin/solar_inverters.html",
        {
            "products": products,
            "categories": categories,
            "selected_category": selected_category,
        }
    )



# =========================================================
# ADD SOLAR INVERTER
# =========================================================

@login_required(login_url="/admin-login/")
def add_solar_inverter(request):

    if request.method == "POST":

        category = request.POST.get(
            "category",
            ""
        ).strip()

        name1 = request.POST.get(
            "name1",
            ""
        ).strip()

        name2 = request.POST.get(
            "name2",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        # -------------------------------------------------
        # CREATE INVERTER
        # -------------------------------------------------

        product = SolarInverter.objects.create(
            category=category,
            name1=name1,
            name2=name2,
            description=description
        )

        # -------------------------------------------------
        # MULTIPLE IMAGES
        # -------------------------------------------------

        images = request.FILES.getlist(
            "images"
        )

        for image in images:

            if image:

                SolarInverterImage.objects.create(
                    inverter=product,
                    image=image
                )

        # -------------------------------------------------
        # MULTIPLE PDFS
        # -------------------------------------------------

        pdf_files = request.FILES.getlist(
            "pdfs"
        )

        pdf_titles = request.POST.getlist(
            "pdf_titles"
        )

        for index, pdf in enumerate(
            pdf_files
        ):

            if not pdf:
                continue

            if index < len(pdf_titles):

                title = pdf_titles[index].strip()

            else:

                title = ""

            if not title:

                title = pdf.name.rsplit(
                    ".",
                    1
                )[0]

            SolarInverterPDF.objects.create(
                inverter=product,
                title=title,
                pdf=pdf
            )

        messages.success(
            request,
            "Solar inverter added successfully."
        )

        return redirect(
            "solar_inverters"
        )

    return render(
        request,
        "admin/add_solar_inverter.html"
    )


# =========================================================
# EDIT SOLAR INVERTER
# =========================================================

@login_required(login_url="/admin-login/")
def edit_solar_inverter(request, id):

    product = get_object_or_404(
        SolarInverter,
        id=id
    )

    if request.method == "POST":

        # -------------------------------------------------
        # PRODUCT
        # -------------------------------------------------

        product.category = request.POST.get(
            "category",
            ""
        ).strip()

        product.name1 = request.POST.get(
            "name1",
            ""
        ).strip()

        product.name2 = request.POST.get(
            "name2",
            ""
        ).strip()

        product.description = request.POST.get(
            "description",
            ""
        ).strip()

        product.save()

        # -------------------------------------------------
        # ADD IMAGES
        # -------------------------------------------------

        for image in request.FILES.getlist(
            "images"
        ):

            if image:

                SolarInverterImage.objects.create(
                    inverter=product,
                    image=image
                )

        # -------------------------------------------------
        # ADD PDFS
        # -------------------------------------------------

        pdf_files = request.FILES.getlist(
            "pdfs"
        )

        pdf_titles = request.POST.getlist(
            "pdf_titles"
        )

        for index, pdf in enumerate(
            pdf_files
        ):

            if not pdf:
                continue

            if index < len(pdf_titles):

                title = pdf_titles[index].strip()

            else:

                title = ""

            if not title:

                title = pdf.name.rsplit(
                    ".",
                    1
                )[0]

            SolarInverterPDF.objects.create(
                inverter=product,
                title=title,
                pdf=pdf
            )

        # -------------------------------------------------
        # DELETE IMAGES
        # -------------------------------------------------

        delete_images = request.POST.getlist(
            "delete_images"
        )

        if delete_images:

            SolarInverterImage.objects.filter(
                id__in=delete_images,
                inverter=product
            ).delete()

        # -------------------------------------------------
        # DELETE PDFS
        # -------------------------------------------------

        delete_pdfs = request.POST.getlist(
            "delete_pdfs"
        )

        if delete_pdfs:

            SolarInverterPDF.objects.filter(
                id__in=delete_pdfs,
                inverter=product
            ).delete()

        # -------------------------------------------------
        # UPDATE EXISTING PDF TITLES
        # -------------------------------------------------

        existing_pdf_ids = request.POST.getlist(
            "existing_pdf_ids"
        )

        existing_pdf_titles = request.POST.getlist(
            "existing_pdf_titles"
        )

        for index, pdf_id in enumerate(
            existing_pdf_ids
        ):

            if index >= len(
                existing_pdf_titles
            ):
                continue

            pdf_title = (
                existing_pdf_titles[index]
                .strip()
            )

            pdf_obj = SolarInverterPDF.objects.filter(
                id=pdf_id,
                inverter=product
            ).first()

            if pdf_obj and pdf_title:

                pdf_obj.title = pdf_title

                pdf_obj.save(
                    update_fields=[
                        "title"
                    ]
                )

        messages.success(
            request,
            "Solar inverter updated successfully."
        )

        return redirect(
            "solar_inverters"
        )

    return render(
        request,
        "admin/edit_solar_inverter.html",
        {
            "product": product,
            "images": product.images.all(),
            "pdfs": product.pdfs.all()
        }
    )


# =========================================================
# DELETE SOLAR INVERTER
# =========================================================

@login_required(login_url="/admin-login/")
def delete_solar_inverter(request, id):

    product = get_object_or_404(
        SolarInverter,
        id=id
    )

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Solar inverter deleted successfully."
        )

    return redirect(
        "solar_inverters"
    )


# =========================================================
# PUBLIC SOLAR INVERTERS
# =========================================================

from datetime import timedelta

from django.shortcuts import render
from django.utils import timezone

from .models import SolarInverter


def solar_inverters_page(request):

    products = (
        SolarInverter.objects
        .prefetch_related(
            "images",
            "pdfs"
        )
        .all()
        .order_by("-id")
    )

    # Unique categories
    categories = (
        SolarInverter.objects
        .exclude(category__isnull=True)
        .exclude(category__exact="")
        .values_list("category", flat=True)
        .distinct()
    )

    fifteen_days_ago = (
        timezone.now()
        - timedelta(days=15)
    )

    return render(
        request,
        "solar_inverters.html",
        {
            "products": products,
            "categories": categories,
            "fifteen_days_ago": fifteen_days_ago,
        }
    )


# =========================================================
# SOLAR INVERTER DETAIL
# =========================================================

def solar_inverter_detail(request, id):

    product = get_object_or_404(
        SolarInverter.objects.prefetch_related(
            "images",
            "pdfs"
        ),
        id=id
    )

    return render(
        request,
        "solar_inverter_detail.html",
        {
            "product": product
        }
    )


# =========================================================
# BATTERY STORAGE
# =========================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import (
    BatteryStorage,
    BatteryStorageImage,
    BatteryStoragePDF,
)


# =========================================================
# PUBLIC - BATTERY STORAGE LIST
# =========================================================

def public_battery_storage(request):

    batteries = (
        BatteryStorage.objects
        .prefetch_related("images", "pdfs")
        .order_by("-created_at")
    )

    categories = (
        BatteryStorage.objects
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )

    return render(
        request,
        "battery_storage.html",
        {
            "batteries": batteries,
            "categories": categories,
        }
    )


def battery_storage_detail(request, id):

    battery = get_object_or_404(
        BatteryStorage.objects.prefetch_related(
            "images",
            "pdfs",
        ),
        id=id
    )

    return render(
        request,
        "battery_storage_detail.html",
        {
            "battery": battery,
        }
    )

# =========================================================
# ADMIN - MANAGE BATTERY STORAGE
# =========================================================

# =========================================================
# ADMIN - BATTERY STORAGE LIST
# =========================================================

def battery_storage(request):

    products = (
        BatteryStorage.objects
        .prefetch_related(
            "images",
            "pdfs",
        )
        .order_by("-created_at")
    )

    # -----------------------------------------------------
    # CATEGORY FILTER
    # -----------------------------------------------------

    selected_category = request.GET.get(
        "category",
        ""
    ).strip()

    if selected_category:

        products = products.filter(
            category=selected_category
        )

    # -----------------------------------------------------
    # GET UNIQUE TEXT CATEGORIES
    # -----------------------------------------------------

    categories = (
        BatteryStorage.objects
        .exclude(category="")
        .exclude(category__isnull=True)
        .values_list(
            "category",
            flat=True
        )
        .distinct()
        .order_by("category")
    )

    return render(
        request,
        "admin/battery_storage.html",
        {
            "products": products,
            "categories": categories,
            "selected_category": selected_category,
        }
    )


# =========================================================
# ADMIN - ADD BATTERY STORAGE
# =========================================================

def add_battery_storage(request):

    if request.method == "POST":

        # -------------------------------------------------
        # TEXT FIELDS
        # -------------------------------------------------

        category = request.POST.get(
            "category",
            ""
        ).strip()

        name1 = request.POST.get(
            "name1",
            ""
        ).strip()

        name2 = request.POST.get(
            "name2",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not category:

            messages.error(
                request,
                "Please enter a battery storage category."
            )

            return render(
                request,
                "admin/add_battery_storage.html",
                {
                    "category": category,
                    "name1": name1,
                    "name2": name2,
                    "description": description,
                }
            )

        if not name1:

            messages.error(
                request,
                "Please enter the product name."
            )

            return render(
                request,
                "admin/add_battery_storage.html",
                {
                    "category": category,
                    "name1": name1,
                    "name2": name2,
                    "description": description,
                }
            )

        if not description:

            messages.error(
                request,
                "Please enter the product description."
            )

            return render(
                request,
                "admin/add_battery_storage.html",
                {
                    "category": category,
                    "name1": name1,
                    "name2": name2,
                    "description": description,
                }
            )

        # -------------------------------------------------
        # IMAGES
        # -------------------------------------------------

        images = request.FILES.getlist(
            "images"
        )

        if not images:

            messages.error(
                request,
                "Please upload at least one product image."
            )

            return render(
                request,
                "admin/add_battery_storage.html",
                {
                    "category": category,
                    "name1": name1,
                    "name2": name2,
                    "description": description,
                }
            )

        # -------------------------------------------------
        # CREATE BATTERY PRODUCT
        # -------------------------------------------------

        product = BatteryStorage.objects.create(
            category=category,
            name1=name1,
            name2=name2,
            description=description,
        )

        # -------------------------------------------------
        # SAVE ALL IMAGES
        # -------------------------------------------------

        for image in images:

            if image:

                BatteryStorageImage.objects.create(
                    product=product,
                    image=image,
                )

        # -------------------------------------------------
        # SAVE FIRST IMAGE AS MAIN IMAGE
        # -------------------------------------------------

        if images:

            product.image = images[0]

            product.save(
                update_fields=["image"]
            )

        # -------------------------------------------------
        # PDF FILES
        # -------------------------------------------------

        pdfs = request.FILES.getlist(
            "pdfs"
        )

        pdf_titles = request.POST.getlist(
            "pdf_titles"
        )

        # -------------------------------------------------
        # SAVE PDFs
        # -------------------------------------------------

        for index, pdf in enumerate(pdfs):

            if not pdf:
                continue

            title = ""

            if index < len(pdf_titles):

                title = pdf_titles[index].strip()

            BatteryStoragePDF.objects.create(
                product=product,
                pdf=pdf,
                title=title,
            )

        # -------------------------------------------------
        # SUCCESS MESSAGE
        # -------------------------------------------------

        messages.success(
            request,
            f'"{product.name1}" has been added successfully.'
        )

        return redirect(
            "battery_storage"
        )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    return render(
        request,
        "admin/add_battery_storage.html"
    )


# =========================================================
# ADMIN - EDIT BATTERY STORAGE
# =========================================================

def edit_battery_storage(
    request,
    product_id
):

    product = get_object_or_404(
        BatteryStorage,
        id=product_id
    )

    if request.method == "POST":

        # -------------------------------------------------
        # TEXT FIELDS
        # -------------------------------------------------

        category = request.POST.get(
            "category",
            ""
        ).strip()

        name1 = request.POST.get(
            "name1",
            ""
        ).strip()

        name2 = request.POST.get(
            "name2",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not category:

            messages.error(
                request,
                "Please enter a battery storage category."
            )

            return redirect(
                "edit_battery_storage",
                product_id=product.id
            )

        if not name1:

            messages.error(
                request,
                "Please enter the product name."
            )

            return redirect(
                "edit_battery_storage",
                product_id=product.id
            )

        if not description:

            messages.error(
                request,
                "Please enter the product description."
            )

            return redirect(
                "edit_battery_storage",
                product_id=product.id
            )

        # -------------------------------------------------
        # UPDATE PRODUCT
        # -------------------------------------------------

        product.category = category
        product.name1 = name1
        product.name2 = name2
        product.description = description

        product.save()

        # -------------------------------------------------
        # NEW IMAGES
        # -------------------------------------------------

        images = request.FILES.getlist(
            "images"
        )

        for image in images:

            if image:

                BatteryStorageImage.objects.create(
                    product=product,
                    image=image,
                )

        # -------------------------------------------------
        # UPDATE MAIN IMAGE
        # -------------------------------------------------

        if images:

            product.image = images[0]

            product.save(
                update_fields=["image"]
            )

        # -------------------------------------------------
        # NEW PDFs
        # -------------------------------------------------

        pdfs = request.FILES.getlist(
            "pdfs"
        )

        pdf_titles = request.POST.getlist(
            "pdf_titles"
        )

        for index, pdf in enumerate(pdfs):

            if not pdf:
                continue

            title = ""

            if index < len(pdf_titles):

                title = pdf_titles[index].strip()

            BatteryStoragePDF.objects.create(
                product=product,
                pdf=pdf,
                title=title,
            )

        # -------------------------------------------------
        # SUCCESS MESSAGE
        # -------------------------------------------------

        messages.success(
            request,
            f'"{product.name1}" has been updated successfully.'
        )

        return redirect(
            "battery_storage"
        )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    return render(
        request,
        "admin/edit_battery_storage.html",
        {
            "product": product,
        }
    )


# =========================================================
# ADMIN - DELETE BATTERY STORAGE
# =========================================================

def delete_battery_storage(
    request,
    product_id
):

    product = get_object_or_404(
        BatteryStorage,
        id=product_id
    )

    if request.method == "POST":

        product.delete()

    # -----------------------------------------------------
    # NO SUCCESS MESSAGE HERE
    # -----------------------------------------------------

    return redirect(
        "battery_storage"
    )


# =========================================================
# ADMIN - DELETE BATTERY IMAGE
# =========================================================

def delete_battery_storage_image(
    request,
    image_id
):

    image = get_object_or_404(
        BatteryStorageImage,
        id=image_id
    )

    product_id = image.product.id

    if request.method == "POST":

        image.delete()

    # -----------------------------------------------------
    # NO SUCCESS MESSAGE HERE
    # -----------------------------------------------------

    return redirect(
        "edit_battery_storage",
        product_id=product_id
    )


# =========================================================
# ADMIN - DELETE BATTERY PDF
# =========================================================

def delete_battery_storage_pdf(
    request,
    pdf_id
):

    pdf = get_object_or_404(
        BatteryStoragePDF,
        id=pdf_id
    )

    product_id = pdf.product.id

    if request.method == "POST":

        pdf.delete()

    # -----------------------------------------------------
    # NO SUCCESS MESSAGE HERE
    # -----------------------------------------------------

    return redirect(
        "edit_battery_storage",
        product_id=product_id
    )



from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404



# =========================================================
# USER MANAGEMENT
# =========================================================

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render


# =========================================================
# ALL USERS
# =========================================================

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render


# =========================================================
# ALL USERS
# =========================================================

@login_required(login_url="/admin-login/")
def all_users(request):

    # Sirf staff/superuser ko users page access milega
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have permission to access user management."
        )
        return redirect("admin-dashboard")

    users = User.objects.all().order_by("-date_joined")

    return render(
        request,
        "admin/all_users.html",
        {
            "users": users
        }
    )


# =========================================================
# ADD USER
# ONLY SUPERUSER
# =========================================================

@login_required(login_url="/admin-login/")
def add_user(request):

    # -------------------------------------------------
    # ONLY SUPERUSER CAN ADD USERS
    # -------------------------------------------------

    if not request.user.is_superuser:

        messages.error(
            request,
            "Only the superuser can add new users."
        )

        return redirect("all-users")


    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        is_staff = request.POST.get(
            "is_staff"
        ) == "on"

        is_active = request.POST.get(
            "is_active"
        ) == "on"


        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not username:

            messages.error(
                request,
                "Username is required."
            )

            return redirect("add-user")


        if not email:

            messages.error(
                request,
                "Email address is required."
            )

            return redirect("add-user")


        if not password:

            messages.error(
                request,
                "Password is required."
            )

            return redirect("add-user")


        if not confirm_password:

            messages.error(
                request,
                "Please confirm your password."
            )

            return redirect("add-user")


        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("add-user")


        # -------------------------------------------------
        # DUPLICATE USERNAME
        # -------------------------------------------------

        if User.objects.filter(
            username__iexact=username
        ).exists():

            messages.error(
                request,
                f"Username '{username}' already exists. Please choose another username."
            )

            return redirect("add-user")


        # -------------------------------------------------
        # DUPLICATE EMAIL
        # -------------------------------------------------

        if User.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                f"Email '{email}' is already registered. Please use another email address."
            )

            return redirect("add-user")


        # -------------------------------------------------
        # CREATE USER
        # -------------------------------------------------

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = is_staff
        user.is_active = is_active

        # IMPORTANT:
        # Newly created user ko superuser nahi banayenge.
        user.is_superuser = False

        user.save()


        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        messages.success(
            request,
            f"User '{username}' created successfully."
        )

        return redirect("all-users")


    # -------------------------------------------------
    # GET REQUEST
    # -------------------------------------------------

    return render(
        request,
        "admin/add_user.html"
    )


# =========================================================
# USER DETAILS
# STAFF + SUPERUSER CAN VIEW
# =========================================================

@login_required(login_url="/admin-login/")
def user_details(request, user_id):

    # -------------------------------------------------
    # ONLY STAFF/SUPERUSER
    # -------------------------------------------------

    if not request.user.is_staff:

        messages.error(
            request,
            "You do not have permission to view users."
        )

        return redirect("admin-dashboard")


    user = get_object_or_404(
        User,
        id=user_id
    )

    return render(
        request,
        "admin/user_details.html",
        {
            "user": user
        }
    )


# =========================================================
# EDIT USER
# ONLY SUPERUSER
# =========================================================

@login_required(login_url="/admin-login/")
def edit_user(request, user_id):

    # -------------------------------------------------
    # ONLY SUPERUSER CAN EDIT
    # -------------------------------------------------

    if not request.user.is_superuser:

        messages.error(
            request,
            "Only the superuser can edit users."
        )

        return redirect("all-users")


    user = get_object_or_404(
        User,
        id=user_id
    )


    if request.method == "POST":

        first_name = request.POST.get(
            "first_name",
            ""
        ).strip()

        last_name = request.POST.get(
            "last_name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip().lower()


        # -------------------------------------------------
        # EMAIL REQUIRED
        # -------------------------------------------------

        if not email:

            messages.error(
                request,
                "Email address is required."
            )

            return redirect(
                "edit-user",
                user_id=user.id
            )


        # -------------------------------------------------
        # DUPLICATE EMAIL
        # -------------------------------------------------

        if User.objects.filter(
            email__iexact=email
        ).exclude(
            id=user.id
        ).exists():

            messages.error(
                request,
                f"Email '{email}' is already being used by another user."
            )

            return redirect(
                "edit-user",
                user_id=user.id
            )


        # -------------------------------------------------
        # UPDATE USER
        # -------------------------------------------------

        user.first_name = first_name

        user.last_name = last_name

        user.email = email


        # -------------------------------------------------
        # STAFF PERMISSION
        # -------------------------------------------------

        user.is_staff = (
            request.POST.get("is_staff") == "on"
        )


        # -------------------------------------------------
        # IMPORTANT
        # -------------------------------------------------
        # Existing superuser ko edit karte waqt bhi
        # accidentally superuser status remove nahi hoga.

        if user.is_superuser:

            user.is_superuser = True


        # -------------------------------------------------
        # ACTIVE STATUS
        # -------------------------------------------------

        user.is_active = (
            request.POST.get("is_active") == "on"
        )


        user.save()


        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        messages.success(
            request,
            "User updated successfully."
        )

        return redirect(
            "user-details",
            user_id=user.id
        )


    # -------------------------------------------------
    # GET REQUEST
    # -------------------------------------------------

    return render(
        request,
        "admin/edit_user.html",
        {
            "user": user
        }
    )


# =========================================================
# DELETE USER
# ONLY SUPERUSER
# =========================================================

@login_required(login_url="/admin-login/")
def delete_user(request, user_id):

    # -------------------------------------------------
    # ONLY SUPERUSER CAN DELETE
    # -------------------------------------------------

    if not request.user.is_superuser:

        messages.error(
            request,
            "Only the superuser can delete users."
        )

        return redirect("all-users")


    # -------------------------------------------------
    # DELETE SHOULD ONLY HAPPEN WITH POST
    # -------------------------------------------------

    if request.method != "POST":

        messages.error(
            request,
            "Invalid request."
        )

        return redirect("all-users")


    user = get_object_or_404(
        User,
        id=user_id
    )


    # -------------------------------------------------
    # PREVENT SUPERUSER FROM DELETING HIMSELF
    # -------------------------------------------------

    if user.id == request.user.id:

        messages.error(
            request,
            "You cannot delete your own account."
        )

        return redirect("all-users")


    username = user.username

    user.delete()


    # -------------------------------------------------
    # SUCCESS
    # -------------------------------------------------

    messages.success(
        request,
        f"User '{username}' deleted successfully."
    )

    return redirect("all-users")


from django.db.models import Avg
from .models import Review


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Review
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Review

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from .models import Review


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg

from .models import Review


# =========================================================
# ADMIN REVIEWS
# =========================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg

from .models import Review


# =========================================================
# SUBMIT CUSTOMER REVIEW
# =========================================================


from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.core.mail import send_mail
from django.conf import settings

from .models import Review


# =========================================================
# SUBMIT REVIEW
# =========================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.db.models import Avg

from .models import Review


# =========================================================
# SUBMIT CUSTOMER REVIEW
# =========================================================

def submit_review(request):

    # =====================================================
    # ONLY POST REQUEST ALLOWED
    # =====================================================

    if request.method != "POST":
        return redirect("home")

    # =====================================================
    # GET FORM DATA
    # =====================================================

    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    rating = request.POST.get("rating", "").strip()
    review_text = request.POST.get("review", "").strip()

    # =====================================================
    # BASIC VALIDATION
    # =====================================================

    if not name or not email or not rating or not review_text:

        messages.error(
            request,
            "Please fill in all review fields.",
            extra_tags="review-error"
        )

        return redirect("home")

    # =====================================================
    # VALIDATE RATING
    # =====================================================

    try:

        rating = int(rating)

    except (ValueError, TypeError):

        messages.error(
            request,
            "Please select a valid rating.",
            extra_tags="review-error"
        )

        return redirect("home")

    # =====================================================
    # RATING RANGE VALIDATION
    # =====================================================

    if rating < 1 or rating > 5:

        messages.error(
            request,
            "Rating must be between 1 and 5.",
            extra_tags="review-error"
        )

        return redirect("home")

    # =====================================================
    # CREATE REVIEW
    #
    # status=False
    # Means admin approval is required.
    # =====================================================

    review_obj = Review.objects.create(

        name=name,
        email=email,
        rating=rating,
        review=review_text,
        status=False

    )

    # =====================================================
    # CREATE RATING STARS
    # =====================================================

    stars = (
        "★" * rating +
        "☆" * (5 - rating)
    )

    # =====================================================
    # ADMIN EMAIL
    # =====================================================

    admin_subject = (
        f"New Customer Review Received | "
        f"SunGreen Solar | {rating}/5"
    )

    # =====================================================
    # ADMIN HTML EMAIL
    # =====================================================

    admin_html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>New Customer Review | SunGreen Solar</title>

</head>

<body style="
    margin:0;
    padding:0;
    background:#ecfeff;
    font-family:Arial,Helvetica,sans-serif;
">

<table width="100%"
       cellpadding="0"
       cellspacing="0"
       border="0"
       style="
           width:100%;
           background:#ecfeff;
           padding:40px 15px;
       ">

<tr>

<td align="center">

<table width="620"
       cellpadding="0"
       cellspacing="0"
       border="0"
       style="
           width:100%;
           max-width:620px;
           background:#ffffff;
           border-radius:24px;
           overflow:hidden;
           border:1px solid #cffafe;
           box-shadow:0 20px 55px rgba(8,145,178,0.12);
       ">

<!-- HEADER -->

<tr>

<td style="
    padding:38px 25px;
    text-align:center;
    background:linear-gradient(
        135deg,
        #ecfdf5 0%,
        #ecfeff 48%,
        #f0fdfa 100%
    );
    border-bottom:1px solid #d1fae5;
">

<div style="
    width:72px;
    height:72px;
    line-height:72px;
    margin:0 auto;
    border-radius:50%;
    background:#ffffff;
    border:1px solid #a7f3d0;
    color:#0891b2;
    font-size:31px;
    font-weight:bold;
">

☀

</div>

<h1 style="
    margin:18px 0 0 0;
    color:#065f46;
    font-size:27px;
    line-height:1.3;
    font-weight:800;
">

SunGreen Solar

</h1>

<p style="
    margin:8px 0 0 0;
    color:#0e7490;
    font-size:14px;
">

New Customer Review Received

</p>

<div style="
    display:inline-block;
    margin-top:16px;
    padding:7px 15px;
    border-radius:30px;
    background:#cffafe;
    color:#0e7490;
    font-size:12px;
    font-weight:bold;
">

● NEW REVIEW

</div>

</td>

</tr>

<!-- CONTENT -->

<tr>

<td style="
    padding:32px 28px;
">

<h2 style="
    margin:0 0 22px 0;
    color:#064e3b;
    font-size:21px;
">

Customer Review Details

</h2>

<!-- NAME -->

<div style="
    margin-bottom:12px;
    padding:16px 18px;
    background:#f0fdfa;
    border:1px solid #ccfbf1;
    border-radius:14px;
">

<div style="
    color:#0f766e;
    font-size:11px;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:0.7px;
    margin-bottom:6px;
">

Customer Name

</div>

<div style="
    color:#1f2937;
    font-size:16px;
    font-weight:700;
">

{name}

</div>

</div>

<!-- EMAIL -->

<div style="
    margin-bottom:12px;
    padding:16px 18px;
    background:#ecfeff;
    border:1px solid #cffafe;
    border-radius:14px;
">

<div style="
    color:#0e7490;
    font-size:11px;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:0.7px;
    margin-bottom:6px;
">

Customer Email

</div>

<div style="
    color:#1f2937;
    font-size:15px;
    font-weight:600;
    word-break:break-word;
">

{email}

</div>

</div>

<!-- RATING -->

<div style="
    margin:18px 0;
    padding:23px;
    text-align:center;
    background:linear-gradient(
        135deg,
        #f0fdfa,
        #ecfeff
    );
    border:1px solid #bae6fd;
    border-radius:16px;
">

<div style="
    color:#0e7490;
    font-size:11px;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:1px;
    margin-bottom:10px;
">

Customer Rating

</div>

<div style="
    color:#f59e0b;
    font-size:30px;
    line-height:1;
    letter-spacing:4px;
">

{stars}

</div>

<div style="
    margin-top:10px;
    color:#047857;
    font-size:15px;
    font-weight:800;
">

{rating} / 5

</div>

</div>

<!-- REVIEW -->

<div style="
    margin-bottom:22px;
    padding:20px;
    background:#f0fdfa;
    border:1px solid #ccfbf1;
    border-radius:16px;
">

<div style="
    color:#0f766e;
    font-size:11px;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:0.8px;
    margin-bottom:12px;
">

Customer Review

</div>

<div style="
    padding:17px;
    background:#ffffff;
    border-left:4px solid #22c55e;
    border-radius:10px;
    color:#374151;
    font-size:15px;
    line-height:1.75;
">

"{review_text}"

</div>

</div>

<!-- APPROVAL -->

<div style="
    padding:20px;
    background:linear-gradient(
        135deg,
        #ecfdf5,
        #ecfeff
    );
    border:1px solid #a7f3d0;
    border-radius:15px;
">

<div style="
    color:#047857;
    font-size:16px;
    font-weight:800;
    margin-bottom:8px;
">

✓ Approval Required

</div>

<div style="
    color:#4b5563;
    font-size:13px;
    line-height:1.7;
">

This review has been saved successfully
and is currently waiting for administrator approval.

It will not appear publicly until it is approved.

</div>

</div>

<!-- REVIEW ID -->

<div style="
    margin-top:22px;
    padding:12px;
    text-align:center;
    background:#f8fafc;
    border-radius:10px;
">

<span style="
    color:#94a3b8;
    font-size:12px;
">

Review ID:

</span>

<strong style="
    color:#0f766e;
    font-size:12px;
">

{review_obj.id}

</strong>

</div>

</td>

</tr>

<!-- FOOTER -->

<tr>

<td style="
    padding:25px 20px;
    text-align:center;
    background:linear-gradient(
        135deg,
        #f0fdf4,
        #ecfeff
    );
    border-top:1px solid #d1fae5;
">

<div style="
    color:#065f46;
    font-size:15px;
    font-weight:800;
">

SunGreen Solar

</div>

<div style="
    margin-top:6px;
    color:#0e7490;
    font-size:12px;
">

Smart • Clean • Sustainable Energy

</div>

<div style="
    margin-top:13px;
    color:#94a3b8;
    font-size:10px;
">

This is an automated administrative notification.

</div>

</td>

</tr>

</table>

</td>

</tr>

</table>

</body>

</html>
"""

    # =====================================================
    # ADMIN PLAIN TEXT
    # =====================================================

    admin_text = f"""
New Customer Review Received

SunGreen Solar
================================

Customer Name:
{name}

Customer Email:
{email}

Rating:
{rating}/5

Stars:
{stars}

Customer Review:
{review_text}

================================

Approval Required

The review is currently pending approval.

Review ID:
{review_obj.id}
"""

    # =====================================================
    # SEND ADMIN EMAIL
    # =====================================================

    try:

        admin_email = EmailMultiAlternatives(

            subject=admin_subject,

            body=admin_text,

            from_email=settings.DEFAULT_FROM_EMAIL,

            to=[
                settings.EMAIL_HOST_USER
            ]

        )

        admin_email.attach_alternative(
            admin_html,
            "text/html"
        )

        admin_email.send(
            fail_silently=False
        )

    except Exception as e:

        print(
            "Review admin email error:",
            e
        )

    # =====================================================
    # CUSTOMER EMAIL
    # =====================================================

    customer_subject = (
        "Thank You for Your Review | SunGreen Solar"
    )

    # =====================================================
    # CUSTOMER HTML EMAIL
    # =====================================================

    customer_html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Thank You | SunGreen Solar</title>

</head>

<body style="
    margin:0;
    padding:0;
    background:#ecfeff;
    font-family:Arial,Helvetica,sans-serif;
">

<table width="100%"
       cellpadding="0"
       cellspacing="0"
       border="0"
       style="
           background:#ecfeff;
           padding:40px 15px;
       ">

<tr>

<td align="center">

<table width="620"
       cellpadding="0"
       cellspacing="0"
       border="0"
       style="
           width:100%;
           max-width:620px;
           background:#ffffff;
           border-radius:24px;
           overflow:hidden;
           border:1px solid #cffafe;
           box-shadow:0 20px 55px rgba(8,145,178,0.12);
       ">

<!-- HEADER -->

<tr>

<td style="
    padding:40px 25px;
    text-align:center;
    background:linear-gradient(
        135deg,
        #ecfdf5,
        #ecfeff,
        #f0fdfa
    );
    border-bottom:1px solid #d1fae5;
">

<div style="
    width:76px;
    height:76px;
    line-height:76px;
    margin:0 auto;
    border-radius:50%;
    background:#ffffff;
    border:1px solid #a7f3d0;
    color:#16a34a;
    font-size:35px;
    font-weight:800;
">

✓

</div>

<h1 style="
    margin:18px 0 0 0;
    color:#065f46;
    font-size:28px;
">

Thank You!

</h1>

<p style="
    margin:8px 0 0 0;
    color:#0e7490;
    font-size:14px;
">

Your feedback means a lot to us

</p>

</td>

</tr>

<!-- CONTENT -->

<tr>

<td style="
    padding:32px 28px;
">

<h2 style="
    margin:0 0 16px 0;
    color:#064e3b;
    font-size:21px;
">

Dear {name},

</h2>

<p style="
    margin:0 0 20px 0;
    color:#4b5563;
    font-size:15px;
    line-height:1.75;
">

Thank you for taking the time to share
your experience with

<strong style="color:#047857;">
SunGreen Solar
</strong>.

Your review has been successfully received
and submitted for approval.

</p>

<!-- SUCCESS -->

<div style="
    margin-bottom:22px;
    padding:17px;
    text-align:center;
    background:#ecfdf5;
    border:1px solid #a7f3d0;
    border-radius:14px;
">

<div style="
    color:#047857;
    font-size:15px;
    font-weight:800;
">

✓ Review Submitted Successfully

</div>

<div style="
    margin-top:6px;
    color:#4b5563;
    font-size:12px;
">

Your review is now awaiting approval.

</div>

</div>

<!-- RATING -->

<div style="
    margin-bottom:22px;
    padding:24px;
    text-align:center;
    background:linear-gradient(
        135deg,
        #f0fdfa,
        #ecfeff
    );
    border:1px solid #bae6fd;
    border-radius:17px;
">

<div style="
    color:#0e7490;
    font-size:11px;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:1px;
    margin-bottom:11px;
">

Your Rating

</div>

<div style="
    color:#f59e0b;
    font-size:32px;
    line-height:1;
    letter-spacing:4px;
">

{stars}

</div>

<div style="
    margin-top:10px;
    color:#047857;
    font-size:15px;
    font-weight:800;
">

{rating} / 5

</div>

</div>

<!-- REVIEW -->

<div style="
    margin-bottom:23px;
    padding:20px;
    background:#f0fdfa;
    border:1px solid #ccfbf1;
    border-radius:16px;
">

<div style="
    color:#0f766e;
    font-size:11px;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:0.8px;
    margin-bottom:12px;
">

Your Review

</div>

<div style="
    padding:17px;
    background:#ffffff;
    border-left:4px solid #22c55e;
    border-radius:10px;
    color:#374151;
    font-size:15px;
    line-height:1.75;
">

"{review_text}"

</div>

</div>

<!-- NEXT -->

<div style="
    padding:20px;
    background:linear-gradient(
        135deg,
        #ecfdf5,
        #ecfeff
    );
    border:1px solid #a7f3d0;
    border-radius:15px;
">

<div style="
    color:#047857;
    font-size:15px;
    font-weight:800;
    margin-bottom:8px;
">

🌿 What's Next?

</div>

<div style="
    color:#4b5563;
    font-size:13px;
    line-height:1.7;
">

Our team will review your feedback.

Once approved, your review will appear
in the <strong>Customer Reviews</strong>
section of the SunGreen Solar website.

</div>

</div>

<p style="
    margin:25px 0 0 0;
    color:#4b5563;
    font-size:14px;
    line-height:1.75;
">

We truly appreciate your time and feedback.
Your experience helps us improve our services
and helps future customers make informed decisions.

</p>

<p style="
    margin:25px 0 0 0;
    color:#374151;
    font-size:14px;
    line-height:1.7;
">

Best Regards,<br>

<strong style="
    color:#065f46;
    font-size:15px;
">

SunGreen Solar

</strong>

<br>

<span style="
    color:#0e7490;
">

Customer Support Team

</span>

</p>

</td>

</tr>

<!-- FOOTER -->

<tr>

<td style="
    padding:26px 20px;
    text-align:center;
    background:linear-gradient(
        135deg,
        #f0fdf4,
        #ecfeff
    );
    border-top:1px solid #d1fae5;
">

<div style="
    color:#065f46;
    font-size:15px;
    font-weight:800;
">

SunGreen Solar

</div>

<div style="
    margin-top:6px;
    color:#0e7490;
    font-size:12px;
">

Smart • Clean • Sustainable Energy

</div>

<div style="
    margin-top:13px;
    color:#94a3b8;
    font-size:10px;
">

This is an automated email.
Please do not reply directly to this email.

</div>

</td>

</tr>

</table>

</td>

</tr>

</table>

</body>

</html>
"""

    # =====================================================
    # CUSTOMER PLAIN TEXT
    # =====================================================

    customer_text = f"""
Dear {name},

Thank you for sharing your experience
with SunGreen Solar.

Your review has been successfully received.

Your Rating:
{stars}

Rating:
{rating}/5

Your Review:
"{review_text}"

Your review has been submitted for approval
by our team.

Once approved, it will appear in the
Customer Reviews section of our website.

We truly appreciate your time and feedback.

Best Regards,

SunGreen Solar
Customer Support Team

This is an automated email.
Please do not reply directly to this email.
"""

    # =====================================================
    # SEND CUSTOMER EMAIL
    # =====================================================

    try:

        customer_email = EmailMultiAlternatives(

            subject=customer_subject,

            body=customer_text,

            from_email=settings.DEFAULT_FROM_EMAIL,

            to=[
                email
            ]

        )

        customer_email.attach_alternative(
            customer_html,
            "text/html"
        )

        customer_email.send(
            fail_silently=False
        )

    except Exception as e:

        print(
            "Review customer email error:",
            e
        )

    # =====================================================
    # SUCCESS MESSAGE
    # =====================================================

    messages.success(

        request,

        "Thank you! Your review has been submitted successfully and is now awaiting approval.",

        extra_tags="review-success"

    )

    # =====================================================
    # REDIRECT HOME
    # =====================================================

    return redirect("home")


# =========================================================
# ADMIN REVIEWS
# =========================================================

def admin_reviews(request):

    # =====================================================
    # GET ALL REVIEWS
    # =====================================================

    reviews = Review.objects.all().order_by("-created")

    # =====================================================
    # TOTAL REVIEWS
    # =====================================================

    total_reviews = Review.objects.count()

    # =====================================================
    # APPROVED REVIEWS
    # =====================================================

    approved_count = Review.objects.filter(
        status=True
    ).count()

    # =====================================================
    # PENDING / REJECTED REVIEWS
    # =====================================================

    pending_count = Review.objects.filter(
        status=False
    ).count()

    # =====================================================
    # AVERAGE RATING
    # =====================================================

    average_rating = Review.objects.aggregate(
        average=Avg("rating")
    )["average"]

    if average_rating is None:

        average_rating = 0

    else:

        average_rating = round(
            average_rating,
            1
        )

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "reviews": reviews,

        "total_reviews": total_reviews,

        "approved_count": approved_count,

        "pending_count": pending_count,

        "average_rating": average_rating,

    }

    # =====================================================
    # RENDER
    # =====================================================

    return render(
        request,
        "admin/reviews.html",
        context
    )


# =========================================================
# APPROVE REVIEW
# =========================================================

def approve_review(request, review_id):

    if request.method == "POST":

        review = get_object_or_404(
            Review,
            id=review_id
        )

        # =================================================
        # APPROVE
        # =================================================

        review.status = True

        review.save(
            update_fields=["status"]
        )

        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        messages.success(
            request,
            f"Review by {review.name} has been approved."
        )

    return redirect("admin-reviews")


# =========================================================
# REJECT REVIEW
# =========================================================

def reject_review(request, review_id):

    if request.method == "POST":

        review = get_object_or_404(
            Review,
            id=review_id
        )

        # =================================================
        # REJECT / PENDING
        # =================================================

        review.status = False

        review.save(
            update_fields=["status"]
        )

        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        messages.success(
            request,
            f"Review by {review.name} has been rejected."
        )

    return redirect("admin-reviews")


# =========================================================
# DELETE REVIEW
# =========================================================

def delete_review(request, review_id):

    if request.method == "POST":

        review = get_object_or_404(
            Review,
            id=review_id
        )

        # =================================================
        # SAVE NAME BEFORE DELETE
        # =================================================

        review_name = review.name

        # =================================================
        # DELETE
        # =================================================

        review.delete()

        # =================================================
        # SUCCESS MESSAGE
        # =================================================

        messages.success(
            request,
            f"Review by {review_name} has been deleted."
        )

    return redirect("admin-reviews")


import random
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone


# =========================================================
# FORGOT PASSWORD
# =========================================================

def admin_forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip()

        # -------------------------------------------------
        # EMAIL CHECK
        # -------------------------------------------------

        if not email:

            return render(
                request,
                "admin/forgot_password.html",
                {
                    "error": "Please enter your registered email address."
                }
            )

        # -------------------------------------------------
        # FIND USER
        # -------------------------------------------------

        try:

            user = User.objects.get(
                email__iexact=email
            )

        except User.DoesNotExist:

            return render(
                request,
                "admin/forgot_password.html",
                {
                    "error": "No account found with this email address."
                }
            )

        # -------------------------------------------------
        # GENERATE 6 DIGIT OTP
        # -------------------------------------------------

        otp = str(
            random.randint(100000, 999999)
        )

        # -------------------------------------------------
        # SAVE SESSION
        # -------------------------------------------------

        request.session["forgot_password_user_id"] = user.id

        request.session["forgot_password_otp"] = otp

        request.session["forgot_password_otp_created"] = (
            timezone.now().isoformat()
        )

        request.session["otp_verified"] = False

        # -------------------------------------------------
        # EMAIL SUBJECT
        # -------------------------------------------------

        subject = "Your Sungreen Solar Password Reset OTP"

        # -------------------------------------------------
        # PLAIN TEXT FALLBACK
        # -------------------------------------------------

        text_message = f"""
Hello {user.first_name or user.username},

We received a request to reset your Sungreen Solar Admin account password.

Your verification code is:

{otp}

This OTP is valid for 5 minutes.

For your security:
- Do not share this OTP with anyone.
- Sungreen Solar will never ask you for this code.
- If you did not request this password reset, you can safely ignore this email.

Regards,
Sungreen Solar
Admin Security Team
"""

        # -------------------------------------------------
        # PREMIUM HTML EMAIL
        # -------------------------------------------------

        html_message = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Sungreen Solar Password Reset</title>

</head>


<body
    style="
        margin:0;
        padding:0;
        background:#f1f5f9;
        font-family:Arial,Helvetica,sans-serif;
        color:#172033;
    "
>


<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        background:#f1f5f9;
        padding:45px 15px;
    "
>

<tr>

<td align="center">


<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        max-width:620px;
        background:#ffffff;
        border-radius:18px;
        overflow:hidden;
        border:1px solid #e2e8f0;
        box-shadow:0 15px 45px rgba(15,23,42,.08);
    "
>


<!-- =====================================================
     TOP GREEN LINE
     ===================================================== -->

<tr>

<td
    style="
        height:5px;
        background:#059669;
        font-size:0;
        line-height:0;
    "
>
</td>

</tr>


<!-- =====================================================
     HEADER
     ===================================================== -->

<tr>

<td
    align="center"
    style="
        padding:38px 35px 25px;
        background:#ffffff;
    "
>


<div
    style="
        width:62px;
        height:62px;
        line-height:62px;
        border-radius:50%;
        background:#ecfdf5;
        color:#059669;
        font-size:28px;
        font-weight:bold;
        margin:0 auto 18px;
    "
>
    🔐
</div>


<div
    style="
        color:#064e3b;
        font-size:11px;
        font-weight:bold;
        letter-spacing:2px;
        text-transform:uppercase;
        margin-bottom:8px;
    "
>
    SUNGREEN SOLAR
</div>


<h1
    style="
        margin:0;
        color:#0f172a;
        font-size:26px;
        line-height:1.3;
        font-weight:700;
    "
>
    Password Reset Verification
</h1>


<p
    style="
        margin:12px 0 0;
        color:#64748b;
        font-size:14px;
        line-height:1.7;
    "
>
    Hello {user.first_name or user.username},
    <br>
    we received a request to reset your admin account password.
</p>


</td>

</tr>


<!-- =====================================================
     OTP SECTION
     ===================================================== -->

<tr>

<td
    style="
        padding:10px 35px 30px;
    "
>


<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        background:#f0fdf4;
        border:1px solid #bbf7d0;
        border-radius:14px;
    "
>

<tr>

<td
    align="center"
    style="
        padding:28px 20px;
    "
>


<div
    style="
        color:#047857;
        font-size:11px;
        font-weight:bold;
        letter-spacing:1.5px;
        text-transform:uppercase;
        margin-bottom:12px;
    "
>
    YOUR VERIFICATION CODE
</div>


<div
    style="
        color:#064e3b;
        font-size:38px;
        line-height:1.2;
        font-weight:800;
        letter-spacing:9px;
        font-family:Arial,Helvetica,sans-serif;
    "
>
    {otp}
</div>


<div
    style="
        margin-top:15px;
        color:#64748b;
        font-size:12px;
    "
>
    This code expires in
    <strong style="color:#dc2626;">
        5 minutes
    </strong>
</div>


</td>

</tr>

</table>


</td>

</tr>


<!-- =====================================================
     SECURITY NOTICE
     ===================================================== -->

<tr>

<td
    style="
        padding:0 35px 28px;
    "
>


<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        background:#f8fafc;
        border:1px solid #e2e8f0;
        border-radius:12px;
    "
>

<tr>

<td
    style="
        padding:20px;
    "
>


<div
    style="
        color:#0f172a;
        font-size:13px;
        font-weight:700;
        margin-bottom:10px;
    "
>
    🛡️ Security Notice
</div>


<p
    style="
        margin:0;
        color:#64748b;
        font-size:12px;
        line-height:1.8;
    "
>
    Never share this verification code with anyone.
    Sungreen Solar will never ask you to provide your OTP
    by phone, email, or message.
</p>


</td>

</tr>

</table>


</td>

</tr>


<!-- =====================================================
     REQUEST NOTICE
     ===================================================== -->

<tr>

<td
    style="
        padding:0 35px 30px;
    "
>


<p
    style="
        margin:0;
        color:#64748b;
        font-size:12px;
        line-height:1.7;
        text-align:center;
    "
>
    If you did not request a password reset,
    you can safely ignore this email.
    Your account remains secure.
</p>


</td>

</tr>


<!-- =====================================================
     FOOTER
     ===================================================== -->

<tr>

<td
    align="center"
    style="
        padding:24px 30px;
        background:#064e3b;
    "
>


<div
    style="
        color:#ffffff;
        font-size:13px;
        font-weight:700;
        margin-bottom:6px;
    "
>
    Sungreen Solar
</div>


<div
    style="
        color:#a7f3d0;
        font-size:11px;
        line-height:1.6;
    "
>
    Admin Security Team
    <br>
    This is an automated security email.
</div>


</td>

</tr>


</table>


<!-- =====================================================
     BOTTOM COPYRIGHT
     ===================================================== -->

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        max-width:620px;
    "
>

<tr>

<td
    align="center"
    style="
        padding:20px 10px 0;
        color:#94a3b8;
        font-size:10px;
        line-height:1.6;
    "
>
    © Sungreen Solar · All rights reserved.
</td>

</tr>

</table>


</td>

</tr>

</table>


</body>

</html>
"""

        # -------------------------------------------------
        # SEND EMAIL
        # -------------------------------------------------

        try:

            email_message = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=None,
                to=[user.email],
            )

            email_message.attach_alternative(
                html_message,
                "text/html"
            )

            email_message.send(
                fail_silently=False
            )

        except Exception as e:

            print("EMAIL ERROR:", e)

            return render(
                request,
                "admin/forgot_password.html",
                {
                    "error":
                    "Unable to send OTP. Please check your email settings."
                }
            )

        # -------------------------------------------------
        # REDIRECT TO OTP PAGE
        # -------------------------------------------------

        return redirect("admin_verify_otp")


    # =====================================================
    # GET REQUEST
    # =====================================================

    return render(
        request,
        "admin/forgot_password.html"
    )




# =========================================================
# VERIFY OTP
# =========================================================

def admin_verify_otp(request):

    user_id = request.session.get(
        "forgot_password_user_id"
    )

    saved_otp = request.session.get(
        "forgot_password_otp"
    )

    otp_created = request.session.get(
        "forgot_password_otp_created"
    )

    # -------------------------------------------------
    # SESSION CHECK
    # -------------------------------------------------

    if not user_id or not saved_otp or not otp_created:

        return redirect(
            "admin_forgot_password"
        )

    # -------------------------------------------------
    # CHECK OTP TIME
    # -------------------------------------------------

    try:

        created_time = timezone.datetime.fromisoformat(
            otp_created
        )

        # Make timezone aware if required
        if timezone.is_naive(created_time):

            created_time = timezone.make_aware(
                created_time
            )

    except Exception:

        return redirect(
            "admin_forgot_password"
        )

    now = timezone.now()

    elapsed_time = now - created_time

    # 5 MINUTES
    if elapsed_time > timedelta(minutes=5):

        # Delete expired OTP
        request.session.pop(
            "forgot_password_otp",
            None
        )

        request.session.pop(
            "forgot_password_otp_created",
            None
        )

        return render(
            request,
            "admin/verify_otp.html",
            {
                "error":
                "OTP has expired. Please request a new OTP.",
                "otp_expired": True
            }
        )

    # -------------------------------------------------
    # REMAINING TIME
    # -------------------------------------------------

    remaining_seconds = int(
        timedelta(minutes=5).total_seconds()
        - elapsed_time.total_seconds()
    )

    if remaining_seconds < 0:
        remaining_seconds = 0

    # -------------------------------------------------
    # POST - VERIFY OTP
    # -------------------------------------------------

    if request.method == "POST":

        entered_otp = request.POST.get(
            "otp",
            ""
        ).strip()

        # -------------------------------------------------
        # EMPTY OTP
        # -------------------------------------------------

        if not entered_otp:

            return render(
                request,
                "admin/verify_otp.html",
                {
                    "error": "Please enter the OTP.",
                    "remaining_seconds": remaining_seconds
                }
            )

        # -------------------------------------------------
        # CHECK OTP
        # -------------------------------------------------

        if entered_otp != saved_otp:

            return render(
                request,
                "admin/verify_otp.html",
                {
                    "error":
                    "Invalid OTP. Please enter the correct OTP.",
                    "remaining_seconds": remaining_seconds
                }
            )

        # -------------------------------------------------
        # OTP SUCCESS
        # -------------------------------------------------

        request.session["otp_verified"] = True

        # OTP should not be usable again
        request.session.pop(
            "forgot_password_otp",
            None
        )

        request.session.pop(
            "forgot_password_otp_created",
            None
        )

        # -------------------------------------------------
        # IMPORTANT
        # GO TO NEW PASSWORD PAGE
        # -------------------------------------------------

        return redirect(
            "admin_new_password"
        )

    # -------------------------------------------------
    # GET OTP PAGE
    # -------------------------------------------------

    return render(
        request,
        "admin/verify_otp.html",
        {
            "remaining_seconds": remaining_seconds
        }
    )


# =========================================================
# NEW PASSWORD
# =========================================================

def admin_new_password(request):

    user_id = request.session.get(
        "forgot_password_user_id"
    )

    otp_verified = request.session.get(
        "otp_verified"
    )

    # -------------------------------------------------
    # SECURITY CHECK
    # -------------------------------------------------

    if not user_id or not otp_verified:

        return redirect(
            "admin_forgot_password"
        )

    # -------------------------------------------------
    # GET USER
    # -------------------------------------------------

    try:

        user = User.objects.get(
            id=user_id
        )

    except User.DoesNotExist:

        # Clear session
        request.session.pop(
            "forgot_password_user_id",
            None
        )

        request.session.pop(
            "otp_verified",
            None
        )

        return redirect(
            "admin_forgot_password"
        )

    # -------------------------------------------------
    # POST
    # -------------------------------------------------

    if request.method == "POST":

        password = request.POST.get(
            "password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        # -------------------------------------------------
        # EMPTY
        # -------------------------------------------------

        if not password or not confirm_password:

            return render(
                request,
                "admin/new_password.html",
                {
                    "error":
                    "Please enter both password fields."
                }
            )

        # -------------------------------------------------
        # MATCH
        # -------------------------------------------------

        if password != confirm_password:

            return render(
                request,
                "admin/new_password.html",
                {
                    "error":
                    "Passwords do not match."
                }
            )

        # -------------------------------------------------
        # LENGTH
        # -------------------------------------------------

        if len(password) < 8:

            return render(
                request,
                "admin/new_password.html",
                {
                    "error":
                    "Password must be at least 8 characters."
                }
            )

        # -------------------------------------------------
        # SET PASSWORD
        # -------------------------------------------------

        user.set_password(password)

        user.save()

        # -------------------------------------------------
        # CLEAR RESET SESSION
        # -------------------------------------------------

        request.session.pop(
            "forgot_password_user_id",
            None
        )

        request.session.pop(
            "forgot_password_otp",
            None
        )

        request.session.pop(
            "forgot_password_otp_created",
            None
        )

        request.session.pop(
            "otp_verified",
            None
        )

        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        return render(
            request,
            "admin/new_password.html",
            {
                "success":
                "Password changed successfully. You can now login."
            }
        )

    # -------------------------------------------------
    # GET
    # -------------------------------------------------

    return render(
        request,
        "admin/new_password.html"
    )


import random

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone


# =========================================================
# RESEND OTP
# =========================================================

def admin_resend_otp(request):

    # =====================================================
    # ONLY POST ALLOWED
    # =====================================================

    if request.method != "POST":

        return redirect(
            "admin_verify_otp"
        )


    # =====================================================
    # GET USER ID FROM SESSION
    # =====================================================

    user_id = request.session.get(
        "forgot_password_user_id"
    )


    if not user_id:

        return redirect(
            "admin_forgot_password"
        )


    # =====================================================
    # GET USER
    # =====================================================

    try:

        user = User.objects.get(
            id=user_id
        )

    except User.DoesNotExist:

        return redirect(
            "admin_forgot_password"
        )


    # =====================================================
    # GENERATE NEW 6 DIGIT OTP
    # =====================================================

    otp = str(
        random.randint(
            100000,
            999999
        )
    )


    # =====================================================
    # UPDATE SESSION
    # =====================================================

    request.session[
        "forgot_password_otp"
    ] = otp


    # -----------------------------------------------------
    # IMPORTANT:
    # RESET OTP CREATED TIME
    # -----------------------------------------------------

    request.session[
        "forgot_password_otp_created"
    ] = timezone.now().isoformat()


    # -----------------------------------------------------
    # OTP VERIFICATION RESET
    # -----------------------------------------------------

    request.session[
        "otp_verified"
    ] = False


    # =====================================================
    # EMAIL SUBJECT
    # =====================================================

    subject = "Your New Sungreen Solar Password Reset OTP"


    # =====================================================
    # PLAIN TEXT FALLBACK
    # =====================================================

    text_message = f"""
Hello {user.first_name or user.username},

A new password reset verification code has been generated
for your Sungreen Solar Admin account.

Your new verification code is:

{otp}

This OTP is valid for 5 minutes.

Security Notice:
- Do not share this OTP with anyone.
- Sungreen Solar will never ask you for this code.
- If you did not request a password reset, please ignore this email.

Regards,
Sungreen Solar
Admin Security Team
"""


    # =====================================================
    # PREMIUM HTML EMAIL
    # =====================================================

    html_message = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>
New Sungreen Solar OTP
</title>

</head>


<body
    style="
        margin:0;
        padding:0;
        background:#f1f5f9;
        font-family:Arial,Helvetica,sans-serif;
        color:#172033;
    "
>


<!-- =====================================================
     MAIN WRAPPER
     ===================================================== -->

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        background:#f1f5f9;
        padding:45px 15px;
    "
>

<tr>

<td align="center">


<!-- =====================================================
     EMAIL CARD
     ===================================================== -->

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        max-width:620px;
        background:#ffffff;
        border-radius:18px;
        overflow:hidden;
        border:1px solid #e2e8f0;
        box-shadow:0 15px 45px rgba(15,23,42,.08);
    "
>


<!-- =====================================================
     GREEN TOP BAR
     ===================================================== -->

<tr>

<td
    style="
        height:5px;
        background:#059669;
        font-size:0;
        line-height:0;
    "
>
</td>

</tr>


<!-- =====================================================
     HEADER
     ===================================================== -->

<tr>

<td
    align="center"
    style="
        padding:38px 35px 25px;
    "
>


<!-- SECURITY ICON -->

<div
    style="
        width:62px;
        height:62px;
        line-height:62px;
        border-radius:50%;
        background:#ecfdf5;
        color:#059669;
        font-size:27px;
        font-weight:bold;
        margin:0 auto 18px;
    "
>
    🔄
</div>


<!-- BRAND -->

<div
    style="
        color:#059669;
        font-size:11px;
        font-weight:bold;
        letter-spacing:2px;
        text-transform:uppercase;
        margin-bottom:8px;
    "
>
    SUNGREEN SOLAR
</div>


<!-- TITLE -->

<h1
    style="
        margin:0;
        color:#0f172a;
        font-size:26px;
        line-height:1.3;
        font-weight:700;
    "
>
    New Verification Code
</h1>


<!-- DESCRIPTION -->

<p
    style="
        margin:12px 0 0;
        color:#64748b;
        font-size:14px;
        line-height:1.7;
    "
>
    Hello {user.first_name or user.username},
    <br>
    a new password reset verification code
    has been generated for your account.
</p>


</td>

</tr>


<!-- =====================================================
     OTP CARD
     ===================================================== -->

<tr>

<td
    style="
        padding:10px 35px 30px;
    "
>


<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        background:#f0fdf4;
        border:1px solid #bbf7d0;
        border-radius:14px;
    "
>

<tr>

<td
    align="center"
    style="
        padding:28px 20px;
    "
>


<div
    style="
        color:#047857;
        font-size:11px;
        font-weight:bold;
        letter-spacing:1.5px;
        text-transform:uppercase;
        margin-bottom:12px;
    "
>
    NEW OTP CODE
</div>


<!-- OTP -->

<div
    style="
        color:#064e3b;
        font-size:38px;
        line-height:1.2;
        font-weight:800;
        letter-spacing:9px;
        font-family:Arial,Helvetica,sans-serif;
    "
>
    {otp}
</div>


<!-- EXPIRY -->

<div
    style="
        margin-top:15px;
        color:#64748b;
        font-size:12px;
    "
>
    Valid for
    <strong style="color:#dc2626;">
        5 minutes
    </strong>
    from the time this email was sent.
</div>


</td>

</tr>

</table>


</td>

</tr>


<!-- =====================================================
     NEW CODE NOTICE
     ===================================================== -->

<tr>

<td
    style="
        padding:0 35px 22px;
    "
>


<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        background:#fffbeb;
        border:1px solid #fde68a;
        border-radius:12px;
    "
>

<tr>

<td
    style="
        padding:17px 18px;
    "
>


<div
    style="
        color:#92400e;
        font-size:12px;
        font-weight:700;
        margin-bottom:5px;
    "
>
    ⚡ Previous OTP replaced
</div>


<div
    style="
        color:#a16207;
        font-size:11px;
        line-height:1.7;
    "
>
    Your previous verification code is no longer valid.
    Please use this new code to continue.
</div>


</td>

</tr>

</table>


</td>

</tr>


<!-- =====================================================
     SECURITY NOTICE
     ===================================================== -->

<tr>

<td
    style="
        padding:0 35px 28px;
    "
>


<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        background:#f8fafc;
        border:1px solid #e2e8f0;
        border-radius:12px;
    "
>

<tr>

<td
    style="
        padding:20px;
    "
>


<div
    style="
        color:#0f172a;
        font-size:13px;
        font-weight:700;
        margin-bottom:10px;
    "
>
    🛡️ Security Notice
</div>


<p
    style="
        margin:0;
        color:#64748b;
        font-size:12px;
        line-height:1.8;
    "
>
    Never share this verification code with anyone.
    Sungreen Solar will never ask you to provide
    your OTP by phone, email, or message.
</p>


</td>

</tr>

</table>


</td>

</tr>


<!-- =====================================================
     NOT YOU MESSAGE
     ===================================================== -->

<tr>

<td
    align="center"
    style="
        padding:0 35px 30px;
    "
>


<p
    style="
        margin:0;
        color:#64748b;
        font-size:12px;
        line-height:1.7;
    "
>
    If you did not request this password reset,
    please ignore this email.
    Your account remains secure.
</p>


</td>

</tr>


<!-- =====================================================
     FOOTER
     ===================================================== -->

<tr>

<td
    align="center"
    style="
        padding:24px 30px;
        background:#064e3b;
    "
>


<div
    style="
        color:#ffffff;
        font-size:13px;
        font-weight:700;
        margin-bottom:6px;
    "
>
    Sungreen Solar
</div>


<div
    style="
        color:#a7f3d0;
        font-size:11px;
        line-height:1.6;
    "
>
    Admin Security Team
    <br>
    This is an automated security email.
</div>


</td>

</tr>


</table>


<!-- =====================================================
     COPYRIGHT
     ===================================================== -->

<table
    width="100%"
    cellpadding="0"
    cellspacing="0"
    border="0"
    style="
        max-width:620px;
    "
>

<tr>

<td
    align="center"
    style="
        padding:20px 10px 0;
        color:#94a3b8;
        font-size:10px;
        line-height:1.6;
    "
>
    © Sungreen Solar · All rights reserved.
</td>

</tr>

</table>


</td>

</tr>

</table>


</body>

</html>
"""


    # =====================================================
    # SEND EMAIL
    # =====================================================

    try:

        email_message = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=None,
            to=[user.email],
        )

        email_message.attach_alternative(
            html_message,
            "text/html"
        )

        email_message.send(
            fail_silently=False
        )

    except Exception as e:

        print(
            "RESEND OTP EMAIL ERROR:",
            e
        )

        return render(
            request,
            "admin/verify_otp.html",
            {
                "error":
                    "Unable to resend OTP. Please try again."
            }
        )


    # =====================================================
    # SUCCESS
    # =====================================================

    return render(
        request,
        "admin/verify_otp.html",
        {
            "success":
                "A new OTP has been sent to your email."
        }
    )


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import (
    MountingKit,
    MountingKitImage,
    MountingKitPDF,
    EVCharger,
    EVChargerImage,
    EVChargerPDF,
)


# =========================================================
# PUBLIC - MOUNTING KITS
# =========================================================

def public_mounting_kits(request):

    mounting_kits = (
        MountingKit.objects
        .prefetch_related(
            "images",
            "pdfs",
        )
        .order_by("-created_at")
    )

    categories = (
        MountingKit.objects
        .exclude(category="")
        .exclude(category__isnull=True)
        .values_list(
            "category",
            flat=True
        )
        .distinct()
        .order_by("category")
    )

    return render(
        request,
        "mounting_kits.html",
        {
            "mounting_kits": mounting_kits,
            "categories": categories,
        }
    )


def mounting_kit_detail(request, id):

    mounting_kit = get_object_or_404(
        MountingKit.objects.prefetch_related(
            "images",
            "pdfs",
        ),
        id=id
    )

    return render(
        request,
        "mounting_kit_detail.html",
        {
            "mounting_kit": mounting_kit,
        }
    )


# =========================================================
# ADMIN - MANAGE MOUNTING KITS
# =========================================================


# =========================================================
# ADMIN - MOUNTING KITS LIST
# =========================================================

def mounting_kits(request):

    products = (
        MountingKit.objects
        .prefetch_related(
            "images",
            "pdfs",
        )
        .order_by("-created_at")
    )

    # -----------------------------------------------------
    # CATEGORY FILTER
    # -----------------------------------------------------

    selected_category = request.GET.get(
        "category",
        ""
    ).strip()

    if selected_category:

        products = products.filter(
            category=selected_category
        )

    # -----------------------------------------------------
    # GET UNIQUE CATEGORIES
    # -----------------------------------------------------

    categories = (
        MountingKit.objects
        .exclude(category="")
        .exclude(category__isnull=True)
        .values_list(
            "category",
            flat=True
        )
        .distinct()
        .order_by("category")
    )

    return render(
        request,
        "admin/mounting_kits.html",
        {
            "products": products,
            "categories": categories,
            "selected_category": selected_category,
        }
    )


# =========================================================
# ADMIN - ADD MOUNTING KIT
# =========================================================

def add_mounting_kit(request):

    if request.method == "POST":

        # -------------------------------------------------
        # TEXT FIELDS
        # -------------------------------------------------

        category = request.POST.get(
            "category",
            ""
        ).strip()

        name1 = request.POST.get(
            "name1",
            ""
        ).strip()

        name2 = request.POST.get(
            "name2",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not category:

            messages.error(
                request,
                "Please enter a mounting kit category."
            )

            return render(
                request,
                "admin/add_mounting_kit.html",
                {
                    "category": category,
                    "name1": name1,
                    "name2": name2,
                    "description": description,
                }
            )

        if not name1:

            messages.error(
                request,
                "Please enter the product name."
            )

            return render(
                request,
                "admin/add_mounting_kit.html",
                {
                    "category": category,
                    "name1": name1,
                    "name2": name2,
                    "description": description,
                }
            )

        if not description:

            messages.error(
                request,
                "Please enter the product description."
            )

            return render(
                request,
                "admin/add_mounting_kit.html",
                {
                    "category": category,
                    "name1": name1,
                    "name2": name2,
                    "description": description,
                }
            )

        # -------------------------------------------------
        # IMAGES
        # -------------------------------------------------

        images = request.FILES.getlist(
            "images"
        )

        if not images:

            messages.error(
                request,
                "Please upload at least one mounting kit image."
            )

            return render(
                request,
                "admin/add_mounting_kit.html",
                {
                    "category": category,
                    "name1": name1,
                    "name2": name2,
                    "description": description,
                }
            )

        # -------------------------------------------------
        # CREATE MOUNTING KIT
        # -------------------------------------------------

        product = MountingKit.objects.create(
            category=category,
            name1=name1,
            name2=name2,
            description=description,
        )

        # -------------------------------------------------
        # SAVE ALL IMAGES
        # -------------------------------------------------

        for image in images:

            if image:

                MountingKitImage.objects.create(
                    product=product,
                    image=image,
                )

        # -------------------------------------------------
        # SAVE FIRST IMAGE AS MAIN IMAGE
        # -------------------------------------------------

        if images:

            product.image = images[0]

            product.save(
                update_fields=["image"]
            )

        # -------------------------------------------------
        # PDF FILES
        # -------------------------------------------------

        pdfs = request.FILES.getlist(
            "pdfs"
        )

        pdf_titles = request.POST.getlist(
            "pdf_titles"
        )

        # -------------------------------------------------
        # SAVE PDFs
        # -------------------------------------------------

        for index, pdf in enumerate(pdfs):

            if not pdf:
                continue

            title = ""

            if index < len(pdf_titles):

                title = pdf_titles[index].strip()

            MountingKitPDF.objects.create(
                product=product,
                pdf=pdf,
                title=title,
            )

        # -------------------------------------------------
        # SUCCESS MESSAGE
        # -------------------------------------------------

        messages.success(
            request,
            f'"{product.name1}" has been added successfully.'
        )

        return redirect(
            "mounting_kits"
        )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    return render(
        request,
        "admin/add_mounting_kit.html"
    )


# =========================================================
# ADMIN - EDIT MOUNTING KIT
# =========================================================

def edit_mounting_kit(
    request,
    product_id
):

    product = get_object_or_404(
        MountingKit,
        id=product_id
    )

    if request.method == "POST":

        # -------------------------------------------------
        # TEXT FIELDS
        # -------------------------------------------------

        category = request.POST.get(
            "category",
            ""
        ).strip()

        name1 = request.POST.get(
            "name1",
            ""
        ).strip()

        name2 = request.POST.get(
            "name2",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not category:

            messages.error(
                request,
                "Please enter a mounting kit category."
            )

            return redirect(
                "edit_mounting_kit",
                product_id=product.id
            )

        if not name1:

            messages.error(
                request,
                "Please enter the product name."
            )

            return redirect(
                "edit_mounting_kit",
                product_id=product.id
            )

        if not description:

            messages.error(
                request,
                "Please enter the product description."
            )

            return redirect(
                "edit_mounting_kit",
                product_id=product.id
            )

        # -------------------------------------------------
        # UPDATE PRODUCT
        # -------------------------------------------------

        product.category = category
        product.name1 = name1
        product.name2 = name2
        product.description = description

        product.save()

        # -------------------------------------------------
        # NEW IMAGES
        # -------------------------------------------------

        images = request.FILES.getlist(
            "images"
        )

        for image in images:

            if image:

                MountingKitImage.objects.create(
                    product=product,
                    image=image,
                )

        # -------------------------------------------------
        # UPDATE MAIN IMAGE
        # -------------------------------------------------

        if images:

            product.image = images[0]

            product.save(
                update_fields=["image"]
            )

        # -------------------------------------------------
        # NEW PDFs
        # -------------------------------------------------

        pdfs = request.FILES.getlist(
            "pdfs"
        )

        pdf_titles = request.POST.getlist(
            "pdf_titles"
        )

        for index, pdf in enumerate(pdfs):

            if not pdf:
                continue

            title = ""

            if index < len(pdf_titles):

                title = pdf_titles[index].strip()

            MountingKitPDF.objects.create(
                product=product,
                pdf=pdf,
                title=title,
            )

        # -------------------------------------------------
        # SUCCESS MESSAGE
        # -------------------------------------------------

        messages.success(
            request,
            f'"{product.name1}" has been updated successfully.'
        )

        return redirect(
            "mounting_kits"
        )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    return render(
        request,
        "admin/edit_mounting_kit.html",
        {
            "product": product,
        }
    )


# =========================================================
# ADMIN - DELETE MOUNTING KIT
# =========================================================

def delete_mounting_kit(
    request,
    product_id
):

    product = get_object_or_404(
        MountingKit,
        id=product_id
    )

    if request.method == "POST":

        product.delete()

    return redirect(
        "mounting_kits"
    )


# =========================================================
# ADMIN - DELETE MOUNTING KIT IMAGE
# =========================================================

def delete_mounting_kit_image(
    request,
    image_id
):

    image = get_object_or_404(
        MountingKitImage,
        id=image_id
    )

    product_id = image.product.id

    if request.method == "POST":

        image.delete()

    return redirect(
        "edit_mounting_kit",
        product_id=product_id
    )


# =========================================================
# ADMIN - DELETE MOUNTING KIT PDF
# =========================================================

def delete_mounting_kit_pdf(
    request,
    pdf_id
):

    pdf = get_object_or_404(
        MountingKitPDF,
        id=pdf_id
    )

    product_id = pdf.product.id

    if request.method == "POST":

        pdf.delete()

    return redirect(
        "edit_mounting_kit",
        product_id=product_id
    )






# =========================================================
# PUBLIC - EV CHARGERS
# =========================================================

def public_ev_chargers(request):

    ev_chargers = (
        EVCharger.objects
        .prefetch_related(
            "images",
            "pdfs",
        )
        .order_by("-created_at")
    )

    categories = (
        EVCharger.objects
        .exclude(category="")
        .exclude(category__isnull=True)
        .values_list(
            "category",
            flat=True
        )
        .distinct()
        .order_by("category")
    )

    return render(
        request,
        "ev_chargers.html",
        {
            "ev_chargers": ev_chargers,
            "categories": categories,
        }
    )


# =========================================================
# PUBLIC - EV CHARGER DETAIL
# =========================================================

def ev_charger_detail(request, id):

    ev_charger = get_object_or_404(
        EVCharger.objects.prefetch_related(
            "images",
            "pdfs",
        ),
        id=id
    )

    return render(
        request,
        "ev_charger_detail.html",
        {
            "ev_charger": ev_charger,
        }
    )


# =========================================================
# ADMIN - EV CHARGERS LIST
# =========================================================

def ev_chargers(request):

    products = (
        EVCharger.objects
        .prefetch_related(
            "images",
            "pdfs",
        )
        .order_by("-created_at")
    )

    # -----------------------------------------------------
    # CATEGORY FILTER
    # -----------------------------------------------------

    selected_category = request.GET.get(
        "category",
        ""
    ).strip()

    if selected_category:

        products = products.filter(
            category=selected_category
        )

    # -----------------------------------------------------
    # UNIQUE CATEGORIES
    # -----------------------------------------------------

    categories = (
        EVCharger.objects
        .exclude(category="")
        .exclude(category__isnull=True)
        .values_list(
            "category",
            flat=True
        )
        .distinct()
        .order_by("category")
    )

    return render(
        request,
        "admin/ev_chargers.html",
        {
            "products": products,
            "categories": categories,
            "selected_category": selected_category,
        }
    )


# =========================================================
# ADMIN - ADD EV CHARGER
# =========================================================

def add_ev_charger(request):

    if request.method == "POST":

        # -------------------------------------------------
        # TEXT FIELDS
        # -------------------------------------------------

        category = request.POST.get(
            "category",
            ""
        ).strip()

        name1 = request.POST.get(
            "name1",
            ""
        ).strip()

        name2 = request.POST.get(
            "name2",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not category:

            messages.error(
                request,
                "Please enter an EV charger category."
            )

            return render(
                request,
                "admin/add_ev_charger.html",
                {
                    "category": category,
                    "name1": name1,
                    "name2": name2,
                    "description": description,
                }
            )

        if not name1:

            messages.error(
                request,
                "Please enter the product name."
            )

            return render(
                request,
                "admin/add_ev_charger.html",
                {
                    "category": category,
                    "name1": name1,
                    "name2": name2,
                    "description": description,
                }
            )

        if not description:

            messages.error(
                request,
                "Please enter the product description."
            )

            return render(
                request,
                "admin/add_ev_charger.html",
                {
                    "category": category,
                    "name1": name1,
                    "name2": name2,
                    "description": description,
                }
            )

        # -------------------------------------------------
        # IMAGES
        # -------------------------------------------------

        images = request.FILES.getlist(
            "images"
        )

        if not images:

            messages.error(
                request,
                "Please upload at least one EV charger image."
            )

            return render(
                request,
                "admin/add_ev_charger.html",
                {
                    "category": category,
                    "name1": name1,
                    "name2": name2,
                    "description": description,
                }
            )

        # -------------------------------------------------
        # CREATE PRODUCT
        # -------------------------------------------------

        product = EVCharger.objects.create(
            category=category,
            name1=name1,
            name2=name2,
            description=description,
        )

        # -------------------------------------------------
        # SAVE ALL IMAGES
        # -------------------------------------------------

        for image in images:

            if image:

                EVChargerImage.objects.create(
                    product=product,
                    image=image,
                )

        # -------------------------------------------------
        # SAVE FIRST IMAGE AS MAIN IMAGE
        # -------------------------------------------------

        if images:

            product.image = images[0]

            product.save(
                update_fields=["image"]
            )

        # -------------------------------------------------
        # PDF FILES
        # -------------------------------------------------

        pdfs = request.FILES.getlist(
            "pdfs"
        )

        pdf_titles = request.POST.getlist(
            "pdf_titles"
        )

        # -------------------------------------------------
        # SAVE PDFs
        # -------------------------------------------------

        for index, pdf in enumerate(pdfs):

            if not pdf:
                continue

            title = ""

            if index < len(pdf_titles):

                title = pdf_titles[index].strip()

            EVChargerPDF.objects.create(
                product=product,
                pdf=pdf,
                title=title,
            )

        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        messages.success(
            request,
            f'"{product.name1}" has been added successfully.'
        )

        return redirect(
            "ev_chargers"
        )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    return render(
        request,
        "admin/add_ev_charger.html"
    )


# =========================================================
# ADMIN - EDIT EV CHARGER
# =========================================================

def edit_ev_charger(
    request,
    product_id
):

    product = get_object_or_404(
        EVCharger,
        id=product_id
    )

    if request.method == "POST":

        # -------------------------------------------------
        # TEXT FIELDS
        # -------------------------------------------------

        category = request.POST.get(
            "category",
            ""
        ).strip()

        name1 = request.POST.get(
            "name1",
            ""
        ).strip()

        name2 = request.POST.get(
            "name2",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not category:

            messages.error(
                request,
                "Please enter an EV charger category."
            )

            return redirect(
                "edit_ev_charger",
                product_id=product.id
            )

        if not name1:

            messages.error(
                request,
                "Please enter the product name."
            )

            return redirect(
                "edit_ev_charger",
                product_id=product.id
            )

        if not description:

            messages.error(
                request,
                "Please enter the product description."
            )

            return redirect(
                "edit_ev_charger",
                product_id=product.id
            )

        # -------------------------------------------------
        # UPDATE PRODUCT
        # -------------------------------------------------

        product.category = category
        product.name1 = name1
        product.name2 = name2
        product.description = description

        product.save()

        # -------------------------------------------------
        # NEW IMAGES
        # -------------------------------------------------

        images = request.FILES.getlist(
            "images"
        )

        for image in images:

            if image:

                EVChargerImage.objects.create(
                    product=product,
                    image=image,
                )

        # -------------------------------------------------
        # UPDATE MAIN IMAGE
        # -------------------------------------------------

        if images:

            product.image = images[0]

            product.save(
                update_fields=["image"]
            )

        # -------------------------------------------------
        # NEW PDFs
        # -------------------------------------------------

        pdfs = request.FILES.getlist(
            "pdfs"
        )

        pdf_titles = request.POST.getlist(
            "pdf_titles"
        )

        for index, pdf in enumerate(pdfs):

            if not pdf:
                continue

            title = ""

            if index < len(pdf_titles):

                title = pdf_titles[index].strip()

            EVChargerPDF.objects.create(
                product=product,
                pdf=pdf,
                title=title,
            )

        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        messages.success(
            request,
            f'"{product.name1}" has been updated successfully.'
        )

        return redirect(
            "ev_chargers"
        )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    return render(
        request,
        "admin/edit_ev_charger.html",
        {
            "product": product,
        }
    )


# =========================================================
# ADMIN - DELETE EV CHARGER
# =========================================================

def delete_ev_charger(
    request,
    product_id
):

    product = get_object_or_404(
        EVCharger,
        id=product_id
    )

    if request.method == "POST":

        product.delete()

    return redirect(
        "ev_chargers"
    )


# =========================================================
# ADMIN - DELETE EV CHARGER IMAGE
# =========================================================

def delete_ev_charger_image(
    request,
    image_id
):

    image = get_object_or_404(
        EVChargerImage,
        id=image_id
    )

    product_id = image.product.id

    if request.method == "POST":

        image.delete()

    return redirect(
        "edit_ev_charger",
        product_id=product_id
    )


# =========================================================
# ADMIN - DELETE EV CHARGER PDF
# =========================================================

def delete_ev_charger_pdf(
    request,
    pdf_id
):

    pdf = get_object_or_404(
        EVChargerPDF,
        id=pdf_id
    )

    product_id = pdf.product.id

    if request.method == "POST":

        pdf.delete()

    return redirect(
        "edit_ev_charger",
        product_id=product_id
    )
