from tasks.models import TasksModel, TaskList, UserModel,CommentsModel
from django import forms


class TaskForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    completion_status = forms.FloatField(widget=forms.NumberInput(
        attrs={'class': 'form-control', 'value': 0}
    ))
    description = forms.CharField(max_length=300, widget=forms.Textarea(
        attrs={'class': 'form-control'}
    ))

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.iteritems():
            if key == 'description':
                self.fields[key].required = False
    class Meta:
        model = TasksModel
        fields = ['name', 'completion_status', 'description']


class TasklistForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}
    ))
    notes = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}
    ))
    status = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control'}
    ))

    def __init__(self, *args, **kwargs):
        super(TasklistForm, self).__init__(*args, **kwargs)

        for key, field in self.fields.iteritems():
            if key != 'name':
                self.fields[key].required = False

    class Meta:
        model = TaskList
        fields = ['name','description', 'notes', 'status']

class CommentForm(forms.ModelForm):
    comment=forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Write Your Comment Here'}
    ),label='')
    class Meta:
        model=CommentsModel
        fields=['comment']


class Subtaskform(TaskForm):
    pass

