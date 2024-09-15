from django.apps import AppConfig


class ModuloStockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modulo_stock'
    verbose_name = 'Módulo de Stock'

    def ready(self):
        # Importar y registrar las señales
        import modulo_stock.signals
