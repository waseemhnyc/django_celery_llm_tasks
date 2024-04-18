from django.db import models

# Create your models here.
class LLMTask(models.Model):
    search_input = models.CharField(max_length=200, default=None, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    def __str__(self) -> str:
        return self.search_input

