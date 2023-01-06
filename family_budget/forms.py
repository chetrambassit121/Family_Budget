from django import forms
from .models import Project, Category
from django.http import HttpResponseRedirect, HttpResponse


class ExpenseForm(forms.Form):
    title = forms.CharField()
    amount = forms.IntegerField()
    category = forms.CharField()

class ProjectForm(forms.ModelForm):
    name = forms.CharField(
    	# max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    budget = forms.IntegerField(
        # max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Project
        fields = ["name", "budget"]

    def __init__(self, *args, **kwargs):                                    
        super(ProjectForm, self).__init__(*args, **kwargs)                    
        self.fields['name'].widget.attrs['class'] = 'form-control'            
        self.fields['budget'].widget.attrs['class'] = 'form-control'       
        # self.fields['category'].widget.attrs['class'] = 'form-control' 
        

    # def get_categories(self, *args, **kwargs):
    #     categories = self.request.POST['categoriesString'].split(',')
    #     for category in categories:
    #         Category.objects.create(
    #             project=Project.objects.get(id=self.objects.id),
    #             name=category
    #         ).save()
    #     return HttpResponseRedirect('/' + self.get_success_url())

    