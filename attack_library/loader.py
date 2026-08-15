from pathlib import Path

import yaml

from shared.models import AttackCategory, AttackStrategy


LIBRARY_PATH = Path(__file__).parent


def load_attack_library() -> list[AttackStrategy]:
    """
    Load every YAML attack library file and convert it
    into AttackStrategy objects.
    """

    strategies = []

    for yaml_file in LIBRARY_PATH.glob("*.yaml"):

        with open(yaml_file, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        category = AttackCategory(data["category"])

        for strategy in data["strategies"]:

            strategies.append(
    AttackStrategy(
    category=category,
    tactic=strategy["tactic"],
    objective=strategy["objective"],
    template_name=strategy["template_name"],
)
)

    return strategies