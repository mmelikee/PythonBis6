from ex3 import TransformCreatureFactory


def test_transformation(creature) -> None:
    print(creature.describe())
    print(creature.attack())
    print(creature.transform())
    print(creature.attack())
    print(creature.revert())


if __name__ == "__main__":

    factory = TransformCreatureFactory()

    base = factory.create_base()
    evolved = factory.create_evolved()

    print("Testing Creature with transform capability")

    print(" base:")
    test_transformation(base)

    print(" evolved:")
    test_transformation(evolved)
