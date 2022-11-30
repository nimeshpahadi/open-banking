from django.db import models
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image


class Product(models.Model):
  product_id = models.CharField(max_length=120)
  effective_from = models.DateField()
  effective_to = models.DateField()
  last_updated = models.DateField()
  product_category = models.CharField(max_length=120)
  name = models.CharField(max_length=120)
  description = models.TextField()
  brand = models.CharField(max_length=120)
  brand_name = models.CharField(max_length=120)
  application_uri = models.TextField(max_length=255)
  is_tailored = models.CharField(max_length=120)
  additional_information_overview_uri = models.TextField(max_length=255)
  additional_information_terms_uri = models.TextField(max_length=255)
  additional_information_eligibility_uri = models.TextField(max_length=255)
  additional_information_fees_and_pricing_uri = models.TextField(max_length=255)
  additional_information_bundle_uri = models.TextField(max_length=255)
  insert_time = models.DateField()
  image = models.ImageField(upload_to='images')

  # override the save method and 
  # use the Image class of the PIL package 
  # to convert it to JPEG
  def save(self, *args, **kwargs):
    if self.image:
      filename = "%s.jpg" % self.image.name.split('.')[0]
      
      image = Image.open(self.image)
      # for PNG images discard the alpha channel and fill it with some color
      if image.mode in ('RGBA', 'LA'):
        background = Image.new(image.mode[:-1], image.size, '#fff')
        background.paste(image, image.split()[-1])
        image = background
        image_io = BytesIO()
        image.save(image_io, format='JPEG', quality=100)
                
        # change the image field value to be the newly modified image value
        self.image.save(filename, ContentFile(image_io.getvalue()), save=False)
    super(Product, self).save(*args, **kwargs)

  def __str__(self):
    return self.name