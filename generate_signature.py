#!/usr/bin/env python3
"""Generate and deploy a personalized Outlook signature from a template."""

from __future__ import annotations

import argparse
import configparser
import html
import shutil
import subprocess
import sys
from pathlib import Path


def app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


APP_DIR = app_dir()
DEFAULT_CONFIG_PATH = APP_DIR / "config.ini"
PLACEHOLDERS = {
    "name": "{{NAME}}",
    "function": "{{FUNCTION}}",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pull the latest template, generate a personalized Outlook signature, and copy it to the configured destination."
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG_PATH),
        help="Path to the INI config file. Defaults to config.ini in the repository root.",
    )
    parser.add_argument(
        "--skip-pull",
        action="store_true",
        help="Skip the git pull step for local testing or offline use.",
    )
    return parser.parse_args()


def resolve_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = APP_DIR / path
    return path


def load_config(config_path: Path) -> configparser.ConfigParser:
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")

    required = {
        "signature": ("name", "function"),
        "paths": ("template_path", "generated_output_path", "copy_to_path"),
        "workflow": ("run_git_pull", "allow_git_pull_failure"),
    }
    missing = [
        f"{section}.{option}"
        for section, options in required.items()
        for option in options
        if not config.has_option(section, option)
    ]
    if missing:
        raise ValueError(f"Missing required config values: {', '.join(missing)}")

    return config


def pull_latest_template(allow_failure: bool) -> None:
    print("Running git pull --ff-only to update the local template...")
    result = subprocess.run(
        ["git", "pull", "--ff-only"],
        cwd=APP_DIR,
        text=True,
        capture_output=True,
        check=False,
    )

    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)

    if result.returncode != 0:
        message = "git pull --ff-only failed"
        if allow_failure:
            print(f"Warning: {message}; continuing because workflow.allow_git_pull_failure is true.", file=sys.stderr)
            return
        raise RuntimeError(message)


def render_signature(template_path: Path, name: str, function: str) -> str:
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    template = template_path.read_text(encoding="utf-8")
    replacements = {
        PLACEHOLDERS["name"]: html.escape(name, quote=True),
        PLACEHOLDERS["function"]: html.escape(function, quote=True),
    }

    rendered = template
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)

    unresolved = [placeholder for placeholder in PLACEHOLDERS.values() if placeholder in rendered]
    if unresolved:
        raise ValueError(f"Unresolved placeholders remain in template: {', '.join(unresolved)}")

    return rendered


def write_file(path: Path, contents: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def copy_signature(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def main() -> int:
    args = parse_args()
    config_path = resolve_path(args.config)
    config = load_config(config_path)

    run_git_pull = config.getboolean("workflow", "run_git_pull") and not args.skip_pull
    allow_pull_failure = config.getboolean("workflow", "allow_git_pull_failure")
    if run_git_pull:
        pull_latest_template(allow_pull_failure)

    template_path = resolve_path(config.get("paths", "template_path"))
    generated_output_path = resolve_path(config.get("paths", "generated_output_path"))
    copy_to_path = resolve_path(config.get("paths", "copy_to_path"))

    rendered = render_signature(
        template_path=template_path,
        name=config.get("signature", "name"),
        function=config.get("signature", "function"),
    )
    write_file(generated_output_path, rendered)
    copy_signature(generated_output_path, copy_to_path)

    print(f"Generated signature: {generated_output_path}")
    print(f"Copied signature to: {copy_to_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
