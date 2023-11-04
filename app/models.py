from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


# Create your models here.
def criminal_image_upload_to(instance, filename):
    # Get the associated Criminal instance's name
    full_name = (f"{instance.Criminal.Criminal_Firstname}_"
                 f"{instance.Criminal.Criminal_Middlename}_"
                 f"{instance.Criminal.Criminal_Lastname}")

    # Create the dynamic upload path
    return f"criminal/database/{full_name.lower()}/{filename}"


class Criminal(models.Model):
    Criminal_Firstname = models.CharField(max_length=100, default="")
    Criminal_Middlename = models.CharField(max_length=5, default="")
    Criminal_Lastname = models.CharField(max_length=100, default="")
    Criminal_Description = models.CharField(max_length=1000)

    @property
    def full_name(self):
        return (f"{self.Criminal_Firstname} "
                f"{self.Criminal_Middlename} "
                f"{self.Criminal_Lastname}")

    def __str__(self):
        return self.full_name


class CriminalImage(models.Model):
    Criminal = models.ForeignKey(Criminal, default=None, on_delete=models.CASCADE)
    Criminal_Image = models.ImageField(upload_to=criminal_image_upload_to)

    def __str__(self):
        full_name = self.Criminal.full_name

        # Get the filename from the criminal_image field
        filename = self.Criminal_Image.name.split('/')[-1]

        # Combine the full name and the filename
        return f"{full_name}/{filename}"

    def save(self, *args, **kwargs):
        if self.pk:  # If it's an update (not a new image)
            # Get the original instance
            original = CriminalImage.objects.get(pk=self.pk)

            # Check if the new image is different from the original
            if original.Criminal_Image != self.Criminal_Image:
                # Delete the old image
                original.Criminal_Image.delete(False)
        super(CriminalImage, self).save(*args, **kwargs)


@receiver(pre_delete, sender=CriminalImage)
def delete_criminal_image(sender, instance, **kwargs):
    # Delete the associated image file from the filesystem
    instance.Criminal_Image.delete(False)
