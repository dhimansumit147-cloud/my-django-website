from django import forms
from .models import CustomerReview


class CustomerReviewForm(forms.ModelForm):

    class Meta:
        model = CustomerReview

        fields = [
            "name",
            "email",
            "rating",
            "review",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "review-input",
                    "placeholder": "Enter your name",
                    "autocomplete": "name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "review-input",
                    "placeholder": "Enter your email (optional)",
                    "autocomplete": "email",
                }
            ),

            "rating": forms.Select(
                attrs={
                    "class": "review-input review-rating-select",
                }
            ),

            "review": forms.Textarea(
                attrs={
                    "class": "review-input review-textarea",
                    "placeholder": "Share your experience with us...",
                    "rows": 5,
                }
            ),
        }

    def clean_review(self):
        review = self.cleaned_data["review"]

        if len(review.strip()) < 10:
            raise forms.ValidationError(
                "Please write at least 10 characters."
            )

        return review