from django.shortcuts import render, redirect
# we need to import our class based views
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
# in order to use the model, we have to import
from .models import Cat, Toy, Photo
from .forms import FeedingForm

# for adding photos we need more imports
import uuid
import boto3
import os

# These are the old cats, now we use models.
# cats = [
#     {'name': 'Lolo', 'breed': 'tabby', 'description': 'furry little demon', 'age': 3},
#     {'name': 'Sachi', 'breed': 'calico', 'description': 'gentle and loving', 'age': 2},
# ]

# Create your views here.

# define the home view
def home(request):
    # unlike EJS templating, we need the html file extension
    return render(request, 'home.html')

# define the about view
def about(request):
    return render(request, 'about.html')

# Index View for all cats
def cats_index(request):
    # we can pass data to templates, JUST like we did in express.
    # return render(request, 'cats/index.html', {'cats': cats })
    # we need to retrieve our list of cats
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', { 'cats': cats })

# Detail view for a single cat
def cats_detail(request, cat_id):
    # find the cat
    cat = Cat.objects.get(id=cat_id)
    # instantiate a feeding form to be rendered in the template
    feeding_form = FeedingForm()
    id_list = cat.toys.all().values_list('id')
    # print(f'The id_list for the cat toys: {id_list}')
    toys_cat_doesnt_have = Toy.objects.exclude(id__in=id_list)
    # print(f'the toys cat dont got: {toys_cat_doesnt_have}')
    return render(request, 'cats/detail.html', { 'cat': cat, 'feeding_form': feeding_form, 'toys': toys_cat_doesnt_have })

# View for adding a feeding to a cat
def add_feeding(request, cat_id):
    # create a ModelForm instance using the data in request.POST
    form = FeedingForm(request.POST)
    # we need to make sure the form data is valid
    if form.is_valid():
        # then we need to add/save the feeding
        # we dont want to save the feeding until the cat is associated
        new_feeding = form.save(commit=False)
        # associate the feeding with a cat
        new_feeding.cat_id = cat_id
        # save the feeding 
        new_feeding.save()
    # finally, redirect back to the detail page(which refreshes the info)
    return redirect('detail', cat_id=cat_id)

# Now we can inherit from the CreateView to make our cats create view
class CatCreate(CreateView):
    model = Cat
    # fields = '__all__'
    fields = ['name', 'breed', 'description', 'age']
    # special string pattern for a successful create
    # success_url = '/cats/{cat_id}'

# UpdateView, very similar to CreateView, needs model and fields
class CatUpdate(UpdateView):
    model = Cat
    # let's make it so you cant rename a cat
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    # instead of fields or using the absolure_url, we just use a success_url
    success_url = '/cats'


# Views for Toys

# ToyList
class ToyList(ListView):
    model = Toy
    template_name = 'toys/index.html'

# ToyDetail
class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/detail.html'

# ToyCreate
class ToyCreate(CreateView):
    model = Toy
    fields = ['name', 'color']

    def form_valid(self, form):
        return super().form_valid(form)
    
# ToyUpdate
class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

# ToyDelete
class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

# adds toy to cat
def assoc_toy(request, cat_id, toy_id):
    # to make the association, we target the cat and pass the toy id
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

# removes toy from cat
def unassoc_toy(request, cat_id, toy_id):
    # to make the association, we target the cat and pass the toy id
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', cat_id=cat_id)


# adding photos via s3
def add_photo(request, cat_id):
    # we need a photo file (named via the 'name' attribute in the form field)
    photo_file = request.FILES.get('photo-file', None)
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    # check if we actually got a photo, do something if we did, do something else if we didnt
    if photo_file:
        # here's where we'll do our S3 stuff
        # target s3
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        # we need a unique name for all of our files, so we'll use uuid to generate one automatically
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # we'll build the entire url string
            url = f'{os.environ["S3_BASE_URL"]}{bucket}/{key}'
            # we create the photo and associate it with the cat
            Photo.objects.create(url=url, cat_id=cat_id)
        except Exception as e:
            print('An error occured uploading to s3')
            print(e)

    return redirect('detail', cat_id=cat_id)