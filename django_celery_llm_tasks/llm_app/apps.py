from django.apps import AppConfig


class LlmAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "django_celery_llm_tasks.llm_app"
