
from ex3 import FlameFactory, TransformCreatureFactory
from ex3.factories import CreatureFactory
from ex4 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    InvalidStrategyError
)


def battle(
    opponents: list[tuple[CreatureFactory, BattleStrategy]]
) -> None:
    creatures = [
        (factory.create_base(), strategy)
        for factory, strategy in opponents
    ]

    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    for i in range(len(creatures)):
        for j in range(i + 1, len(creatures)):
            creature1, strategy1 = creatures[i]
            creature2, strategy2 = creatures[j]

            print("\n* Battle *")
            print(creature1.describe())
            print(" vs.")
            print(creature2.describe())
            print(" now fight!")

            try:
                strategy1.act(creature1)
                strategy2.act(creature2)
            except InvalidStrategyError as error:
                print(
                    f"Battle error, aborting tournament: {error}"
                )
                return


if __name__ == "__main__":

    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Shiftling+Aggressive) ]")

    battle([
        (FlameFactory(), NormalStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy())
    ])

    print("\nTournament 1 (error)")
    print(" [ (Shiftling+Aggressive), (Flameling+Aggressive) ]")

    battle([
        (TransformCreatureFactory(), AggressiveStrategy()),
        (FlameFactory(), AggressiveStrategy())
    ])
