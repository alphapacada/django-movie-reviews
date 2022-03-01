from django import forms
from .models import Collections, Movie


class CustomMMCF(forms.ModelMultipleChoiceField):
    def label_from_instance(self, member):
        return "%s" % member.name


class AddToCollectionForm(forms.ModelForm):
    """
    Form to let user add movie to specific folders
    """

    def __init__(self, *args, **kwargs):
        # access user from request to query for folders associated with user.
        self.request = kwargs.pop("request", None)
        super(AddToCollectionForm, self).__init__(*args, **kwargs)
        if self.request is not None:
            self.fields["folders"] = CustomMMCF(
                queryset=Collections.objects.filter(user=self.request.user).all(),
                widget=forms.CheckboxSelectMultiple,
            )

    class Meta:
        model = Movie
        fields = ["folders"]


class CreateFolderForm(forms.ModelForm):
    """
    Form to let user add new folder
    """

    def __init__(self, *args, **kwargs):
        # access user from request to query for folders associated with user.
        self.request = kwargs.pop("request", None)
        super(CreateFolderForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        # Make sure that name will not violate the unique_together constraint on folder.name and
        # folder.user
        name = self.cleaned_data["name"]
        if Collections.objects.filter(name=name, user=self.request.user).exists():
            raise forms.ValidationError("Folder with this Name already exists.")
        return name

    class Meta:
        model = Collections
        exclude = ("user",)
