import unittest

from attack_library.loader import load_attack_library
from shared.models import AttackCategory


class AttackLibraryLoaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.strategies = load_attack_library()

    def test_loader_returns_strategies(self):
        self.assertGreaterEqual(len(self.strategies), 5)

    def test_every_strategy_has_required_fields(self):
        for strategy in self.strategies:
            self.assertIsInstance(strategy.category, AttackCategory)
            self.assertTrue(strategy.tactic)
            self.assertTrue(strategy.objective)
            self.assertTrue(strategy.template_name)

    def test_loader_includes_expected_categories(self):
        categories = {strategy.category for strategy in self.strategies}

        self.assertTrue(
            {
                AttackCategory.PROMPT_INJECTION,
                AttackCategory.JAILBREAK,
                AttackCategory.ROLEPLAY,
                AttackCategory.SENSITIVE_DISCLOSURE,
                AttackCategory.MULTILINGUAL,
            }.issubset(categories)
        )

    def test_template_names_are_unique(self):
        template_names = [strategy.template_name for strategy in self.strategies]

        self.assertEqual(len(template_names), len(set(template_names)))


if __name__ == "__main__":
    unittest.main()
