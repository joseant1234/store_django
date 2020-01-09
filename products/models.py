from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
import uuid

# Create your models here.
class Product(models.Model):
    # la cantidad de caracteres debe coincidir con lo definido en el formulario
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    slug = models.SlugField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # sobrrescribe el metodo save
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Product, self).save(*args, **kwargs)

    # sobreescribe el metodo str para que muestre un atributo en la consulta
    def __str__(self):
        return self.title

# solo interesa el sender y instance, hay otros argumentos
def set_slug(sender, instance, *args, **kwargs):
    if instance.title and not instance.slug:
        slug = slugify(instance.title)

        while Product.objects.filter(slug=slug).exists():
            slug = slugify(
                '{}-{}'.format(instance.title, str(uuid.uuid4())[:8])
            )
        instance.slug = slug


# se registra callback. Se pone la funcion y el modelo q lo va a utilizar
pre_save.connect(set_slug, sender=Product)
