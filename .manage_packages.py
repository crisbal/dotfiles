#!/usr/bin/env python3
import argparse
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set
from itertools import chain as itchain

CONFIG_FILE = Path.home() / ".packages.txt"

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", default=False)
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand", required=True)
    subparsers.add_parser("dump")
    subparsers.add_parser("install")
    return parser

def read_config_file(config_file: Path) -> Dict[str, List[str]]:
    lines = config_file.read_text().splitlines()
    packages: Dict[str, List[str]] = defaultdict(list)
    section_name = None
    for line in lines:
        if len(line) == 0: continue
        if line.startswith("#"):
            section_name = line.split("#")[1].strip()
        else:
            packages[section_name or "OTHER"].append(line)
    return packages

def local_installed_packages() -> Set[str]:
    return set(subprocess.check_output(["pacman", "-Qmq"]).decode("UTF-8").splitlines())

def all_installed_packages() -> Set[str]:
    return set(subprocess.check_output(["pacman", "-Qeq"]).decode("UTF-8").splitlines())

def subcommand_install(dry_run: bool):
    if not CONFIG_FILE.exists():
        raise Exception("Config file does not exist, nothing to install")
    config = read_config_file(CONFIG_FILE)
    packages = set(itchain.from_iterable(pkgs for pkgs in config.values()))
    local_packages = set(pkg for pkg in packages if pkg.endswith("#local"))
    packages_to_install = sorted(packages - local_packages)
    install_command = ["pacman", "-Syu", *packages_to_install]
    print(*install_command)
    if not dry_run:
        subprocess.run(install_command)
    print()
    print("Local packages (install manually with AUR helper):")
    print(*[pkg.replace("#local", "") for pkg in sorted(local_packages)])

def subcommand_dump(dry_run: bool):
    config: Dict[str, List[str]] = defaultdict(list)
    if CONFIG_FILE.exists():
        config = read_config_file(CONFIG_FILE)
    packages_in_config = set(itchain.from_iterable(pkgs for pkgs in config.values()))

    installed_packages = all_installed_packages()
    local_packages = local_installed_packages()
    remote_packages = installed_packages - local_packages
    local_packages_formatted = set(f"{pkg}#local" for pkg in local_packages)

    new_packages = (local_packages_formatted | remote_packages) - packages_in_config
    removed_packages =  packages_in_config - (local_packages_formatted | remote_packages)
    print("NEW", new_packages)
    print("REMOVED", removed_packages)
    print("")

    if new_packages:
        config["NEW"].extend(new_packages)

    output = []
    for section_name in sorted(config.keys()):
        if len(config[section_name]) == 0: continue
        output.append(f"# {section_name}")
        for package in sorted(config[section_name]):
            if package not in removed_packages:
                output.append(package)
        output.append("")
    output = "\n".join(output)
    if not dry_run:
        CONFIG_FILE.write_text(output)
        print("Written to config file, adjust manually")
        print(f"# vim {CONFIG_FILE}")
    else:
        print(output)

def main(): 
    parser = build_parser()
    args = parser.parse_args()
    if args.subcommand == "dump":
        subcommand_dump(args.dry_run)
    elif args.subcommand == "install":
        subcommand_install(args.dry_run)
    else:
        raise Exception("This should never happen")
    print("DONE")

if __name__ == "__main__":
    main()
