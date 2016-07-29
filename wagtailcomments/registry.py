class Registry(object):
    def __init__(self):
        self.models = []

    def add(self, model):
        """Register a model as a valid comment target"""
        self.models.append(model)

    def __contains__(self, model):
        """Check if a model (or one of its parent classes) is registered"""
        return any(issubclass(model, valid_model)
                   for valid_model in self.models)
