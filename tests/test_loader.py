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
                AttackCategory.SENSITIVE_INFORMATION_DISCLOSURE,
            }.issubset(categories)
        )

    def test_non_sensitive_strategies_use_prompt_injection_category(self):
        non_sensitive = [
            strategy
            for strategy in self.strategies
            if strategy.category == AttackCategory.PROMPT_INJECTION
        ]

        self.assertEqual(len(non_sensitive), 20)

    def test_sensitive_strategies_use_sensitive_information_category(self):
        sensitive = [
            strategy
            for strategy in self.strategies
            if strategy.category
            == AttackCategory.SENSITIVE_INFORMATION_DISCLOSURE
        ]

        self.assertEqual(len(sensitive), 5)

    def test_template_names_are_unique(self):
        template_names = [strategy.template_name for strategy in self.strategies]

        self.assertEqual(len(template_names), len(set(template_names)))


if __name__ == "__main__":
    unittest.main()
