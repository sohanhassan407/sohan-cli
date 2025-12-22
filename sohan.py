#!/usr/bin/env python3
import os
import sys
import subprocess
import difflib
import shlex

HOME = os.path.expanduser("~")

SEARCH_DIRS = [
    f"{HOME}/tools",
    f"{HOME}/xpython",
    f"{HOME}/bin",
]

SECRET_FILE = f"{HOME}/.sohan_secret.txt"


def short_help():
    print("sohan file_or_tool")
    print("sohan find file_or_tool")


def fast_find(name):
    patterns = [name, f"{name}.py", f"{name}.sh"]
    results = []

    for d in SEARCH_DIRS:
        if not os.path.isdir(d):
            continue

        cmd = ["find", d, "-maxdepth", "4", "-type", "f", "("]
        for p in patterns:
            cmd += ["-iname", p, "-o"]
        cmd = cmd[:-1] + [")"]

        try:
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
            results.extend(out.splitlines())
        except subprocess.CalledProcessError:
            pass

    return results


def best_match(name, files):
    if not files:
        return None
    names = [os.path.basename(f) for f in files]
    match = difflib.get_close_matches(name, names, n=1, cutoff=0.4)
    if not match:
        return None
    return files[names.index(match[0])]


def run_file(path, args):
    os.chdir(os.path.dirname(path))

    if path.endswith(".py"):
        cmd = ["python", path] + args
    elif path.endswith(".sh"):
        cmd = ["bash", path] + args
    else:
        cmd = [path] + args

    subprocess.run(cmd)


def main():
    if len(sys.argv) == 1:
        print("sohan is sohan not for you")
        return

    if sys.argv[1] in ("help", "-h", "--help"):
        short_help()
        return

    if sys.argv[1] == "-passwd":
        if not os.path.exists(SECRET_FILE):
            print("secret file not found")
            return
        subprocess.run(["nano", SECRET_FILE])
        return

    if sys.argv[1] == "find":
        if len(sys.argv) < 3:
            print("missing target")
            return

        files = fast_find(sys.argv[2])
        if not files:
            print("not found")
            return

        path = files[0]
        dirpath = os.path.dirname(path)

        print(f"CD:{dirpath}")
        print(f"FOUND:{path}")
        return

    target = sys.argv[1]
    args = sys.argv[2:]

    files = fast_find(target)
    path = best_match(target, files)

    if not path:
        subprocess.run(" ".join(shlex.quote(x) for x in sys.argv[1:]), shell=True)
        return

    run_file(path, args)


if __name__ == "__main__":
    main()
