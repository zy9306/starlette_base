from spectree import SpecTree

spec = SpecTree("starlette")


def register(app):
    spec.register(app)
