from ex3 import FlameFactory, TransformCreatureFactory
from ex3.factories import CreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()

    print(base.describe())
    print(base.attack())

    print(evolved.describe())
    print(evolved.attack())


def test_battle(
    factory1: CreatureFactory,
    factory2: CreatureFactory
) -> None:
    creature1 = factory1.create_base()
    creature2 = factory2.create_base()

    print(creature1.describe())
    print(" vs.")
    print(creature2.describe())
    print(" fight!")

    print(creature1.attack())
    print(creature2.attack())


if __name__ == "__main__":

    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()

    print("Testing factory")
    test_factory(flame_factory)

    print("\nTesting factory")
    test_factory(transform_factory)

    print("\nTesting battle")
    test_battle(flame_factory, transform_factory)
