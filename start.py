"""
Cross-platform Docker helper using only Python built-ins.

Usage:
    python start.py [--prod|--dev] <command> [args]
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
NO_SSL_OVERRIDE = REPO_ROOT / "docker-compose.nossl.yml"
CERT_WILDCARD = REPO_ROOT / "certs" / "_.cyberfortress.local.crt"
CERT_KEY = REPO_ROOT / "certs" / "_.cyberfortress.local.key"


def compose_cmd(files: list[Path], use_ssl: bool) -> list[str]:
    cmd: list[str] = ["docker", "compose"]
    for f in files:
        cmd += ["-f", str(f)]
    if use_ssl:
        cmd += ["--profile", "ssl"]
    return cmd


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def call_setup(script_path: Path) -> None:
    run([sys.executable, str(script_path)])


def add_manage_args(base: list[str], extra: list[str]) -> list[str]:
    return base + extra


def color_env_label(environment: str) -> str:
    base = f"[{environment}]"
    if not sys.stdout.isatty():
        return base
    color = "\033[92m" if environment == "prod" else "\033[94m"
    return f"\033[1m{color}{base}\033[0m"


def env_status_lines(environment: str, use_ssl: bool) -> str:
    label = color_env_label(environment)
    ssl_note = "on" if use_ssl else "off"
    return f"{label} SSL/TLS={ssl_note}"


def env_access_urls(use_ssl: bool) -> str:
    access_urls = (
        "https://localhost, https://library.cyberfortress.local (if you installed Root CA and set hosts)"
        if use_ssl
        else "http://localhost:8080"
    )
    return f"Access: {access_urls}"


def color_warning(text: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"\033[1m\033[93m{text}\033[0m"  # Bright yellow/orange

def color_info(text: str) -> str:
    if not sys.stdout.isatty():
        return text
    return f"\033[1m\033[94m{text}\033[0m"  # Bright blue

def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--prod", action="store_true", help="Use production compose file")
    parser.add_argument("--dev", action="store_true", help="Use development compose file (default)")
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("rest", nargs=argparse.REMAINDER, help="Extra args for manage.py commands")
    args = parser.parse_args(argv)

    compose_file = REPO_ROOT / ("docker-compose.prod.yml" if args.prod else "docker-compose.yml")
    use_ssl = CERT_WILDCARD.exists() and CERT_KEY.exists()
    compose_files = [compose_file] if use_ssl else [compose_file, NO_SSL_OVERRIDE]
    c = compose_cmd(compose_files, use_ssl)
    environment = "prod" if args.prod else "dev"
    status_line = env_status_lines(environment, use_ssl)

    print(status_line)
    print("─" * 50)

    cmd = args.command or "help"
    extra = args.rest[1:] if args.rest and args.rest[0] == "--" else args.rest

    scripts_dir = REPO_ROOT / "scripts"

    try:
        if cmd == "setup":
            try:
                call_setup(scripts_dir / "setup.py")
                # setup.py already printed success message and next steps
            except subprocess.CalledProcessError as exc:
                # setup.py already printed error messages and next steps
                return exc.returncode or 1
        elif cmd == "build":
            # print(f"{status_line}\n")
            if args.prod:
                run(c + ["pull"])
            run(c + ["build"])
            print(color_info(f"\n✓ Build completed.\n"))
            print(color_info("Next: "))
            print("  python start.py up")
        elif cmd in {"up"}:
            # print(f"{status_line}\n")
            run(c + ["up", "-d"])
            print(color_info(f"✓ Services started.\n"))
            print(color_info(f"{env_access_urls(use_ssl)}"))
        elif cmd in {"down"}:
            # print(f"{status_line}\n")
            run(c + ["down"])
            print("✓ Services stopped.")
        elif cmd == "restart":
            # print(f"{status_line}\n")
            run(c + ["restart"])
            print("✓ Services restarted.")
        elif cmd == "logs":
            # print(f"{status_line}\n")
            run(c + ["logs", "-f"])
        elif cmd == "makemigrations":
            # print(f"{status_line}\n")
            run(add_manage_args(c + ["exec", "web", "python", "manage.py", "makemigrations"], extra))
        elif cmd == "migrate":
            # print(f"{status_line}\n")
            run(add_manage_args(c + ["exec", "web", "python", "manage.py", "migrate"], extra))
        elif cmd == "initdata":
            # print(f"{status_line}\n")
            run(c + ["exec", "web", "python", "init_data.py"])
        elif cmd == "createsuperuser":
            # print(f"{status_line}\n")
            run(c + ["exec", "web", "python", "manage.py", "createsuperuser"])
        elif cmd == "shell":
            # print(f"{status_line}\n")
            run(c + ["exec", "web", "python", "manage.py", "shell"])
        elif cmd == "collectstatic":
            # print(f"{status_line}\n")
            run(c + ["exec", "web", "python", "manage.py", "collectstatic", "--noinput"])
        elif cmd == "clean":
            # print(f"{status_line}\n")
            run(c + ["down", "-v"])
            run(["docker", "system", "prune", "-f"])
            print("✓ Cleaned up containers, volumes, and system.")
        elif cmd == "rebuild":
            # print(f"{status_line}\n")
            run(c + ["down"])
            run(c + ["build", "--no-cache"])
            run(c + ["up", "-d"])
            print(f"✓ Rebuilt and started services.\n")
            print(f"{env_access_urls(use_ssl)}")
        elif cmd == "help":
            print(color_info("Library Management System"))
            print("─" * 50)
            print(color_info("Usage: python start.py [--prod|--dev] <command> [args]\n"))
            print(color_info("Commands:"))
            print("  setup           Setup environment (.env, certs, Root CA)")
            print("  build           Build Docker images (pull first in prod)")
            print("  up              Start all services")
            print("  down            Stop all services")
            print("  restart         Restart all services")
            print("  logs            Follow logs")
            print("  makemigrations  Create new migrations (passes extra args)")
            print("  migrate         Run database migrations (passes extra args)")
            print("  initdata        Initialize sample data")
            print("  createsuperuser Create Django superuser")
            print("  shell           Open Django shell")
            print("  collectstatic   Collect static files")
            print("  clean           Remove containers and volumes, prune system")
            print("  rebuild         Clean rebuild and start\n")
            print(color_info("Examples:"))
            print("  python start.py setup")
            print("  python start.py build")
            print("  python start.py up")
            print("  python start.py --prod up")
            print("  python start.py migrate -- app_label")
        else:
            print(f"Unknown command: {cmd}")
            return 1
        
        print(f"\n{status_line}")
        return 0
    except subprocess.CalledProcessError as exc:
        print(f"\n{status_line}")
        return exc.returncode or 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
