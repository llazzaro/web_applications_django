from django import forms
from tasks.fields import EmailListField
from tasks.models import SubscribedEmail, Task


# Model based form
class TaskForm(forms.ModelForm):
    watchers = EmailListField(required=False)

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["watchers"].initial = ", ".join([watcher.email for watcher in self.instance.watchers.all()])

    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "status",
            "watchers",
            "file_upload",
            "image_upload",
        )

    def save(self, commit=True):
        task = super(TaskForm, self).save(commit=False)

        if commit:
            task.watchers.all().delete()

        for email_str in self.cleaned_data["watchers"]:
            SubscribedEmail.objects.create(email=email_str, task=task)

        return task


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
