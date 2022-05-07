#!/usr/bin/env python3
#
# generates Provides: bundled(npm(...)) = ... lines for each declared dependency and devDependency of package.json
#
import os
import sys
import json
import re
from packaging import version


def scan_package_json(package_dir):
    for root, dirs, files in os.walk(package_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in ["node_modules", "vendor"]]
        if "package.json" in files:
            yield os.path.join(root, "package.json")


def read_declared_pkgs(package_json_path):
    with open(package_json_path) as f:
        package_json = json.load(f)
        return list(package_json.get("dependencies", {}).keys()) + list(
            package_json.get("devDependencies", {}).keys()
        )


def read_installed_pkgs(yarn_lock_path):
    with open(yarn_lock_path) as f:
        lockfile = f.read()
        return re.findall(
            r'^"?'  # can start with a "
            r"(.+?)@.+(?:,.*)?:\n"  # characters up to @
            r'  version "(.+)"',  # and the version
            lockfile,
            re.MULTILINE,
        )


def list_provides(declared_pkgs, installed_pkgs):
    for declared_pkg in declared_pkgs:
        # there can be multiple versions installed of one package (transitive dependencies)
        # but rpm doesn't support Provides: with a single package and multiple versions
        # so let's declare the oldest version here
        versions = [
            version.parse(pkg_version)
            for pkg_name, pkg_version in installed_pkgs
            if pkg_name == declared_pkg
        ]

        if not versions:
            print(f"warning: {declared_pkg} missing in yarn.lock", file=sys.stderr)
            continue

        oldest_version = sorted(versions)[0]
        yield f"Provides: bundled(npm({declared_pkg})) = {oldest_version}"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} package-X.Y.Z/", file=sys.stdout)
        sys.exit(1)

    package_dir = sys.argv[1]
    declared_pkgs = []
    for package_json_path in scan_package_json(package_dir):
        declared_pkgs.extend(read_declared_pkgs(package_json_path))
    installed_pkgs = read_installed_pkgs(f"{package_dir}/yarn.lock")
    provides = list_provides(declared_pkgs, installed_pkgs)
    for provide in sorted(provides):
        print(provide)
