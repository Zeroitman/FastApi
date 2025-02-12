import factory
from backend.db.schemas.banner import BannerBaseSchema


class BannerFactory(factory.Factory):
    id = factory.Sequence(lambda n: n + 1)
    image = factory.Sequence(
        lambda n: f"http://0.0.0.0:6196/media/banner/{n}/"
    )

    class Meta:
        model = BannerBaseSchema
