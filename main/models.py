from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class TutorialCategory(models.Model):
    tutorial_category = models.CharField(max_length=200)
    category_summary = models.CharField(max_length=200)
    tutorial_cat_image = models.ImageField(default=False)
    category_slug = models.CharField(max_length=200, )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.tutorial_category


class TutorialSeries(models.Model):
    tutorial_series = models.CharField(max_length=200)
    tutorial_category = models.ForeignKey(TutorialCategory, default=1, verbose_name="Categories",
                                          on_delete=models.SET_DEFAULT)
    series_summary = models.CharField(max_length=200)
    tutorial_series_image = models.ImageField(default=False)

    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        return self.tutorial_series


class Tutorials(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_content = RichTextUploadingField()
    tutorial_image = models.ImageField(default=False)
    tutorial_created = models.DateTimeField("date created", auto_now_add=True)

    tutorial_series = models.ForeignKey(TutorialSeries, default=1, verbose_name="Series", on_delete=models.SET_DEFAULT)
    tutorial_slug = models.CharField(max_length=200)

    def __str__(self):
        return self.tutorial_title
