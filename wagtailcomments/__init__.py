from ._version import version as __version__
from ._version import version_info as VERSION
from .registry import Registry

__all__ = ['get_comment_model', 'registry', 'allow_comments', '__version__',
           'VERSION']

registry = Registry()


def allow_comments(model):
    """Allow comments against a model"""
    registry.add(model)
    return model
