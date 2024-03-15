from django.contrib.gis.db import models
from django.contrib.auth.models import User
from core.models import Partner, Program, Project
import os.path
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='ProfilePartner', null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='ProfileProgram', null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ProfileProject', null=True, blank=True)
    image = models.FileField(upload_to='upload/profile/', null=True, blank=True)
    thumbnail = models.FileField(upload_to='upload/profile/', editable=False, null=True, blank=True)

    def make_thumbnail(self):
        try:
            image = Image.open(self.image)
            image.thumbnail((200, 150), Image.ANTIALIAS)
            thumb_name, thumb_extension = os.path.splitext(self.image.name)
            thumb_extension = thumb_extension.lower()
            thumb_filename = thumb_name + '_thumb' + thumb_extension
            if thumb_extension in ['.jpg', '.jpeg']:
                FTYPE = 'JPEG'
            elif thumb_extension == '.gif':
                FTYPE = 'GIF'
            elif thumb_extension == '.png':
                FTYPE = 'PNG'
            else:
                return False  # Unrecognized file type
            # Save thumbnail to in-memory file as StringIO
            temp_thumb = BytesIO()
            image.save(temp_thumb, FTYPE)
            temp_thumb.seek(0)
            # set save=False, otherwise it will run in an infinite loop
            self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()
            return True
        except:
            return False

    def save(self, *args, **kwargs):
        if self.make_thumbnail():
            super(UserProfile, self).save(*args, **kwargs)
        else:
            self.thumbnail = None
            super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Log(models.Model):
    message = models.CharField(max_length=300, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='UserProfile', null=True, blank=True)
    type = models.CharField(max_length=300, null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.message
