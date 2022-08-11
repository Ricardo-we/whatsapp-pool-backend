from django.db.models import Model


class ModelUtils:
    @staticmethod
    def update_model_obj(model: Model, model_data: dict, invalid_fields=[]):
        for key, value in model_data.items():
            for field in invalid_fields:
                if key == field:
                    continue
            setattr(model, key, value)
        model.save()
        return model

    @staticmethod
    def insert_into_model(model: Model, model_data: dict):
        return model.objects.create(**model_data)
