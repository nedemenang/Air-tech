class BaseRepo:

    def __init__(self, _model):
        self._model = _model

    def fetch_all(self):
        return self._model.query.paginate(error_out=False)
  
    def get(self, *args):
        return self._model.query.get(*args)

    def update(self, model_instance, **kwargs):
        for key, val in kwargs.items():
            setattr(model_instance, key, val)
        model_instance.save()
        return model_instance

    def count(self):
        return self._model.query.count()

    def get_unpaginated(self, **kwargs):
        """Query and filter the data of the model."""
        return self._model.query.filter_by(**kwargs).all()

    def get_first_item(self):
        return self._model.query.first()

    def order_by(self, *args):
        return self._model.query.order_by(*args)

    def filter_all(self, **kwargs):
        return self._model.query.filter(**kwargs).paginate(error_out=False)

    def find_first(self, **kwargs):
        return self._model.query.filter_by(**kwargs).first()

    def filter_by(self, **kwargs):
        return self._model.query.filter_by(**kwargs).paginate(error_out=False)

    def filter_first(self, **kwargs):
        return self._model.query.filter_by(**kwargs).first()

    def filter_and_count(self, **kwargs):
        return self._model.query.filter_by(**kwargs).count()

    def filter_and_order(self, *args, **kwargs):
        return self._model.query.filter_by(*kwargs).order_by(*args)

    def paginate(self, **kwargs):
        return self._model.query.paginate(**kwargs)

    def filter(self, *args):
        return self._model.query.filter(*args)
