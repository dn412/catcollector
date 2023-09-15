from django.db import models
# need the reverse method from django urls for redirects
from django.urls import reverse
# import date module from datetime
from datetime import date

# A tuple of 2-tuples
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.

# model for toys
# toys will be a M:M with cats
#  Cats >---< Toys 
class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.color} {self.name}'
    
    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})

class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)

    def __str__(self):
        return self.name
    
    # this is used for redirects from class based views
    def get_absolute_url(self):
        return reverse('detail', kwargs={'cat_id': self.id})
    
    # add a method to determine cat hunger
    def fed_for_today(self):
        # filter produces an <QuerySet> for all feedings from current date
        # count the items in that array, compare to the length of MEALS (tuple)
        # we'll return a boolean that we can use in our template
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)


# Model for Feedings (Cat -|---< Feeding)
class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
        max_length=1,
        # add the choices field option (creates a dropdown)
        choices=MEALS,
        # set a default for our choices
        default=MEALS[0][0]
    )

    # creates cat FK reference
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        # this will use a method for obtaining the value of a field.choice
        return f"{self.get_meal_display()} on {self.date}"
    
    # add Meta class to change the default sorting
    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for cat_id: {self.cat_id} @{self.url}"