from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(
        verbose_name="Название покемона",
        max_length=200)
    title_en = models.CharField(
        verbose_name="Название покемона на английском",
        null=True,
        blank=True,
        max_length=200)
    title_jp = models.CharField(
        verbose_name="Название покемона на японском",
        null=True,
        blank=True,
        max_length=200)
    description = models.TextField(
        verbose_name="Описание",
        null=True)
    photo = models.ImageField(
        verbose_name="Фото",
        upload_to='media',
        null=True)
    parent = models.ForeignKey(
        "self",
        verbose_name="Из кого эволюционировал",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='next_evolutions')

    def __str__(self):
        return '{}'.format(self.title)
    

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon, 
        verbose_name="Покемон",
        on_delete=models.CASCADE)
    lat = models.FloatField(verbose_name="Широта")
    lon = models.FloatField( verbose_name="Долгота")
    appeared_at = models.DateTimeField(verbose_name="Время появления", null=True)
    disappeared_at = models.DateTimeField(verbose_name="Время исчезновения", null=True)
    level = models.IntegerField(verbose_name="Уровень", null=True, blank=True)
    health = models.IntegerField(verbose_name="Здоровье", null=True, blank=True)
    strength = models.IntegerField(verbose_name="Сила", null=True, blank=True)
    defence = models.IntegerField(verbose_name="Защита", null=True, blank=True)
    stamina = models.IntegerField(verbose_name="Выносливость", null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.pokemon)
