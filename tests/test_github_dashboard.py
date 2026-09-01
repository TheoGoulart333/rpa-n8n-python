import unittest

from github_dashboard import demo_data, render


class DashboardTest(unittest.TestCase):
    def test_demo_page_contains_repository_and_metrics(self):
        page = render(demo_data())
        self.assertIn("TheoGoulart333/rpa-n8n-python", page)
        self.assertIn("Estrelas", page)
        self.assertIn("modo demonstração", page)


if __name__ == "__main__":
    unittest.main()
