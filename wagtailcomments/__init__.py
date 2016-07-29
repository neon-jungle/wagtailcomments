from .registry import Registry

__all__ = ['get_comment_model', 'registry', 'allow_comments']

registry = Registry()


def allow_comments(model):
    """Allow comments against a model"""
    registry.add(model)
    return model
