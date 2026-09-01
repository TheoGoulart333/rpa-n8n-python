import unittest

from github_dashboard import demo_data, render, render_markdown_summary


class DashboardTest(unittest.TestCase):
    def test_demo_page_contains_repository_and_metrics(self):
        page = render(demo_data())
        self.assertIn("TheoGoulart333/rpa-n8n-python", page)
        self.assertIn("Estrelas", page)
        self.assertIn("modo demonstração", page)

    def test_markdown_summary_contains_key_metrics(self):
        summary = render_markdown_summary(demo_data())
        self.assertIn("# Repo Health Summary: TheoGoulart333/rpa-n8n-python", summary)
        self.assertIn("Health score: 82/100", summary)
        self.assertIn("Pull requests abertos: 0", summary)


if __name__ == "__main__":
    unittest.main()
