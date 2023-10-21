from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


# Create your models here.
class Book(models.Model):
    book_name = models.CharField(max_length=100)
    author_name = models.CharField(max_length=100)
    book_price = models.IntegerField()
    book_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.book_name


def criminal_image_upload_to(instance, filename):
    # Get the associated Criminal instance's name
    full_name = (f"{instance.criminal.criminal_firstname}_"
                 f"{instance.criminal.criminal_middlename}_"
                 f"{instance.criminal.criminal_lastname}")

    # Create the dynamic upload path
    return f"static/images/{full_name.lower()}/{filename}"


class Criminal(models.Model):
    criminal_firstname = models.CharField(max_length=100, default="")
    criminal_middlename = models.CharField(max_length=5, default="")
    criminal_lastname = models.CharField(max_length=100, default="")
    criminal_description = models.CharField(max_length=1000)

    @property
    def full_name(self):
        return (f"{self.criminal_firstname} "
                f"{self.criminal_middlename} "
                f"{self.criminal_lastname}")

    def __str__(self):
        return self.full_name


class CriminalImage(models.Model):
    criminal = models.ForeignKey(Criminal, default=None, on_delete=models.CASCADE)
    criminal_image = models.ImageField(upload_to=criminal_image_upload_to)

    def __str__(self):
        full_name = self.criminal.full_name

        # Get the filename from the criminal_image field
        filename = self.criminal_image.name.split('/')[-1]

        # Combine the full name and the filename
        return f"{full_name}/{filename}"


@receiver(pre_delete, sender=CriminalImage)
def delete_criminal_image(sender, instance, **kwargs):
    # Delete the associated image file from the filesystem
    instance.criminal_image.delete(False)
