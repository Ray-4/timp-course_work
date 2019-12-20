from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # on_delete=models.CASCADE - Каскадное удаление. Django эмулирует поведение SQL правила
    # ON DELETE CASCADE и так же удаляет объекты, связанные через ForeignKey.
    website = models.CharField(verbose_name='Веб-сайт', max_length=100, null=True, blank=True)
    # При blank=True, проверка данных в форме позволит сохранять пустое значение в поле.
    # null При True Django сохранит пустое значение как NULL в базе данных.

    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    followers = models.ManyToManyField(User, blank=True, related_name='user_followers')

    def __str__(self):
        return f'{self.user.username} Profile'


# Сохранение проверяет exif информацию для фотографий с мобильных телефонов, чтобы увидеть, какую
# ориентацию фотография была сделана, затем изображение поворачивается в вертикальное положение.
# изображения уменьшены для вывода 200px x 200px для экономии места на сервере.
    def save(self, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        exif = img._getexif()
        orientation_key = 274
        if exif and orientation_key in exif:
            orientation = exif[orientation_key]

            rotate_values = {
                3: Image.ROTATE_180,
                6: Image.ROTATE_270,
                8: Image.ROTATE_90
            }

            if orientation in rotate_values:
                img = img.transpose(rotate_values[orientation])

        output_size = (200, 200)
        img.thumbnail(output_size)
        img.save(self.image.path)
