import re
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


class MarkdownLinkTests(unittest.TestCase):
    def test_relative_markdown_links_resolve(self):
        missing = []

        for markdown_file in ROOT.rglob("*.md"):
            if ".git" in markdown_file.parts:
                continue

            text = markdown_file.read_text(encoding="utf-8")
            for match in MARKDOWN_LINK.findall(text):
                target = match.strip().split(maxsplit=1)[0].strip("<>")
                if (
                    not target
                    or "://" in target
                    or target.startswith("#")
                    or target.startswith("mailto:")
                ):
                    continue

                path_text = unquote(target.split("#", 1)[0])
                if not path_text:
                    continue

                resolved = (markdown_file.parent / path_text).resolve()
                if not resolved.exists():
                    missing.append(
                        f"{markdown_file.relative_to(ROOT)} -> {target}"
                    )

        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
