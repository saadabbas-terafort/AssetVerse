import factory

from .models import App, RecordStatus


class RecordStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecordStatus

    lable = factory.Sequence(lambda n: f"Status {n}")
    code = factory.Sequence(lambda n: f"STATUS_{n}")
    is_active = True
    sortorder = factory.Sequence(lambda n: n)


class AppFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = App

    slug = factory.Sequence(lambda n: f"app-{n}")
    lable = factory.Sequence(lambda n: f"App {n}")
    status = factory.SubFactory(RecordStatusFactory)
    sortorder = factory.Sequence(lambda n: n)

