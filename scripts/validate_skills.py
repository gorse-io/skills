#!/usr/bin/env python3
"""Validate this portable Markdown skill collection using only the standard library."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


PRIVATE = re.compile(
    r"/home/[^\s`]+|/Users/[^\s`]+|[A-Z]:\\Users\\|"
    r"gorse-cloud/|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"github_pat_[A-Za-z0-9_]{20,}|\[SKILL_PRUNED\]|"
    r"https://github\.com/[^\s)]+/(?:pull|issues)/\d+"
)
LINK = re.compile(r"\[[^\]]*\]\(([^\s)]+)\)")


def validate(root: Path) -> tuple[list[str], int]:
    root = root.resolve()
    errors = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    if not skills:
        errors.append("skills/: no SKILL.md files found")
    readme = root / "README.md"
    readme_text = readme.read_text() if readme.is_file() else ""
    if not readme_text:
        errors.append("README.md: missing or empty")
    for directory in sorted((root / "skills").iterdir()) if (root / "skills").is_dir() else []:
        if directory.is_dir() and not (directory / "SKILL.md").is_file():
            errors.append(f"{directory.relative_to(root)}: missing SKILL.md")
    for skill in skills:
        rel = skill.relative_to(root)
        text = skill.read_text()
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        fields = {}
        if not match:
            errors.append(f"{rel}: missing YAML frontmatter")
        else:
            for key in ("name", "description"):
                value = re.search(rf"^{key}:\s*(.+)$", match.group(1), re.M)
                fields[key] = value.group(1).strip().strip('\"\'') if value else ""
                if not fields[key] or fields[key] in ("|", ">"):
                    errors.append(f"{rel}: {key} must be a nonempty single-line scalar")
            name = fields.get("name", "")
            if name != skill.parent.name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
                errors.append(f"{rel}: invalid name or directory mismatch")
        if len(text.splitlines()) > 200:
            errors.append(f"{rel}: move long details into references (over 200 lines)")
        if f"]({rel.as_posix()})" not in readme_text:
            errors.append(f"{rel}: not indexed in README.md")
    for path in sorted(root.rglob("*.md")):
        if ".git" in path.relative_to(root).parts:
            continue
        text = path.read_text()
        rel = path.relative_to(root)
        if PRIVATE.search(text):
            errors.append(f"{rel}: private path, credential, or session-specific reference")
        fence = None
        for line in text.splitlines():
            opening = re.match(r"^\s*(`{3,}|~{3,})", line)
            if opening:
                marker = opening.group(1)
                if fence is None:
                    fence = marker
                elif marker[0] == fence[0] and len(marker) >= len(fence):
                    fence = None
        if fence:
            errors.append(f"{rel}: unclosed code fence")
        for target in LINK.findall(text):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = (path.parent / unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(root):
                errors.append(f"{rel}: link escapes collection: {target}")
            elif not resolved.exists():
                errors.append(f"{rel}: missing local link: {target}")
    return errors, len(skills)


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors, count = validate(root)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"Validated {count} skills: structure, frontmatter, local links, and portability checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
