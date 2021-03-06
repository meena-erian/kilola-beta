from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.auth.models import User


class Crop(models.Model):
    name = models.CharField('Name of the fruit/crop', max_length=200)
    icon = models.CharField(
        'Link for an SVG icon for the corp (https://iconscout.com/)',
        max_length=500
    )
    yield_per_acre = models.DecimalField(
        'Average production of this crop in kg per acre',
        max_digits=20,
        decimal_places=2
    )
    time_required = models.DurationField(
        'Average time required to plant this crop.'
    )

    def __str__(self):
        return self.name


class Farmer(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.user.__str__()


class Farm(models.Model):
    name = models.CharField('Farm name', max_length=200)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    location = PlainLocationField(based_fields=['city'], zoom=7)
    size = models.DecimalField(
        'How many acres is this farm',
        max_digits=20,
        decimal_places=2
    )

    def __str__(self):
        return self.name


class Batch(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.RESTRICT)
    farm = models.ForeignKey(Farm, on_delete=models.RESTRICT)
    area = models.DecimalField(
        'How many acres in this batch',
        max_digits=20,
        decimal_places=2
    )
    weight = models.DecimalField(
        "Approximately how many kgs.\
        default is crop.yield_per_acre*area",
        max_digits=20,
        decimal_places=2
    )
    planting_date = models.DateField()
    harvesting_date = models.DateField(
        "The estimated harvesting date\
        default is planting_date+crop.time_required",
    )
    description = models.TextField(
        "Please accurately describe the quality of your crop\
        and any additional details that the buyer needs to know."
    )

    def __str__(self):
        return str(self.farm.farmer) + ":" + str(self.farm)\
            + ":" + self.description


class Buyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)

    def __str__(self):
        return self.user.__str__()


class BatchReservation(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.RESTRICT)
    buyer = models.ForeignKey(Buyer, on_delete=models.RESTRICT)
    acres = models.DecimalField(
        "The amount is reserved in acres because\
        the farm area is the only fact on the ground",
        max_digits=20,
        decimal_places=2
    )
    price_per_kilo = models.DecimalField(
        "Enter the amount you are willing to pay per kilo\
        (if the farmer found a better offer, they can decline yours)",
        max_digits=20,
        decimal_places=2
    )
    approved_by_farmer = models.BooleanField(
        default=False
    )
    logistics = models.CharField(
        'Can be either "on_farmer", "on_buyer", or "on_kilola"',
        max_length=100
    )
    logistics = models.CharField(
        'Additional comment to farmer',
        max_length=500
    )
