from django import forms
from .models import Post, Comment, Profile
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    body = forms.CharField(
        required=False,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Post something...",
                "class": "textarea is-medium",
            }
        ),
        label="",
    )

    post_image = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        body = cleaned_data.get('body')
        post_image = cleaned_data.get('post_image')

        if not body and not post_image:
            raise forms.ValidationError(
                "You must fill in at least one of the fields."
            )

        return cleaned_data


    class Meta:
        model = Post
        exclude = ("user", "likes", )

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Comment something...",
                "class": "textarea is-success is-medium",
            }
        ),
        label="",
    )
    

    class Meta:
        model = Comment
        exclude = ("user", "post", "likes", "parent")

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

    def clean_username(self):
        username = self.cleaned_data.get('username')  # get the username data
        lowercase_username = username.lower()         # get the lowercase version of it

        return lowercase_username
        


class ProfileExtrasForm(forms.ModelForm):
    display_name = forms.CharField(label="Area name", widget=forms.widgets.Textarea(attrs={"class": "input"}))
    profile_image = forms.ImageField(label="Area picture")
    profile_bio = forms.CharField(label="Bio", required=False, widget=forms.widgets.Textarea(attrs={"placeholder": "Describe yourself...","class": "textarea",}))

    background_image = forms.ImageField(label="Background image", required=False)

    favourite_colour = forms.CharField(widget=forms.TextInput(attrs={"type": 'color'}))

    spotify_id = forms.CharField(label="Spotify song ID", required=False, widget=forms.TextInput(attrs={"class": "input"}))

    youtube_link = forms.CharField(label="YouTube", required=False, widget=forms.TextInput(attrs={"class": "input"}))
    twitch_link = forms.CharField(label="Twitch", required=False, widget=forms.TextInput(attrs={"class": "input"}))
    tiktok_link = forms.CharField(label="TikTok", required=False, widget=forms.TextInput(attrs={"class": "input"}))
    instagram_link = forms.CharField(label="Instagram", required=False, widget=forms.TextInput(attrs={"class": "input"}))
    custom_link = forms.CharField(label="Add site", required=False, widget=forms.TextInput(attrs={"class": "input"}))

    general_interests = forms.CharField(label="General interests", required=False, widget=forms.TextInput(attrs={"class": "input"}))
    music_interests = forms.CharField(label="Music interests", required=False, widget=forms.TextInput(attrs={"class": "input"}))
    television_interests = forms.CharField(label="Television interests", required=False, widget=forms.TextInput(attrs={"class": "input"}))
    movies_interests = forms.CharField(label="Movies interests", required=False, widget=forms.TextInput(attrs={"class": "input"}))
    books_interests = forms.CharField(label="Books interests", required=False, widget=forms.TextInput(attrs={"class": "input"}))

    class Meta:
        model = Profile
        fields = ('display_name', 'profile_image', 'profile_bio', 'background_image', 'favourite_colour', 'spotify_id', 'youtube_link', 'twitch_link', 'tiktok_link', 'instagram_link', 'custom_link', 'general_interests', 'music_interests', 'television_interests', 'movies_interests', 'books_interests',)