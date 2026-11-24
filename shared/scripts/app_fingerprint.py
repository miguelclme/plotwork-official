#!/usr/bin/env python3
"""Fingerprint the files of an external prototype's folder, and compare a folder with an earlier fingerprint
(used by the from-app and from-app-update skills).

Usage:
    python app_fingerprint.py write <folder> <out.json> [--skip <relative folder> ...] [--source SRC-n]
    python app_fingerprint.py compare <folder> <old.json> [--skip <relative folder> ...] [--json]

write    walks <folder> and records, for every file, its path (relative to <folder>, with forward slashes), its
         size and its SHA-256, in <out.json>. Run again, it replaces the file: it holds one version only.
compare  walks <folder> the same way and prints the paths added, removed and changed since <old.json>.
         It skips the folders recorded in <old.json> as well as those given with --skip, so a folder skipped
         when the file was written is skipped again. --json prints the result as JSON instead of text.

--skip   a folder to leave out, as a path relative to <folder> (for example docs/old). Repeat it for each
         folder. The caller decides which folders to skip: the script knows no technology and no file layout.
         On Windows a folder is matched without regard to upper and lower case. A --skip that matches no
         folder prints a warning on stderr (it may still be right: the folder may not exist in this version).
         The folder named .git is always left out, wherever it is: it is version-control history, never part of
         the app, and skipped deliberately.
--source the SRC-n the folder is recorded as (kept in the file, and shown by compare).

The script only reads <folder>: it never runs, imports or changes anything in it, and it follows no symbolic
link (a link is left out, and counted). <out.json> must lie outside <folder>.
Exit code: 0 = written, or no difference; 1 = compare found differences; 2 = a problem (a folder or file that
can't be read or written, a bad argument, or an old file that isn't a fingerprint file).
"""
import argparse
import hashlib
import json
import os
import pathlib
import re
import sys

sys.dont_write_bytecode = True  # keep the plugin folder free of __pycache__

FORMAT = 1
SOURCE = re.compile(r"^SRC-[0-9]+$")
DRIVE = re.compile(r"^[A-Za-z]:")
CHUNK = 1 << 20


class FingerprintError(Exception):
    """A problem to report as `ERROR: …` with exit code 2."""


def _clean_skip(value):
    """A --skip value as a normal relative path with forward slashes."""
    text = value.replace("\\", "/").strip()
    if text.startswith("/"):
        raise FingerprintError(f"--skip {value!r} must be relative to the folder: it starts with a slash")
    text = text.strip("/")
    while text.startswith("./"):
        text = text[2:]
    parts = text.split("/") if text else []
    if not parts or DRIVE.match(text) or any(part in ("", ".", "..") for part in parts):
        raise FingerprintError(f"--skip {value!r} must be a folder path relative to the folder, such as docs/old")
    return "/".join(parts)


def _key(path):
    """A path as compared with the skip list: Windows ignores case."""
    return path.casefold() if os.name == "nt" else path


def _is_skipped(path, skips):
    path = _key(path)
    return any(path == _key(skip) or path.startswith(_key(skip) + "/") for skip in skips)


def _warn_unmatched(folder, skips):
    """A warning on stderr for each --skip that matches nothing in the folder."""
    for skip in skips:
        if not os.path.lexists(os.path.join(folder, *skip.split("/"))):
            print(f"WARNING: --skip {skip} matches no folder in {folder}", file=sys.stderr)


def _is_link(entry):
    """A symbolic link, or a Windows junction."""
    is_junction = getattr(entry, "is_junction", None)
    return entry.is_symlink() or bool(is_junction and is_junction())


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint(folder, skips):
    """Return ({relative path: {"size": n, "sha256": hex}}, number of links left out)."""
    files, links, pending = {}, 0, [(str(folder), "")]
    while pending:
        directory, prefix = pending.pop()
        try:
            with os.scandir(directory) as scan:
                entries = sorted(scan, key=lambda entry: entry.name)
        except OSError as exc:
            raise FingerprintError(f"cannot read {directory}: {exc}") from exc
        for entry in entries:
            path = prefix + entry.name
            if entry.name == ".git" or _is_skipped(path, skips):
                continue
            if _is_link(entry):
                links += 1
            elif entry.is_dir(follow_symlinks=False):
                pending.append((entry.path, path + "/"))
            elif entry.is_file(follow_symlinks=False):
                try:
                    files[path] = {"size": entry.stat(follow_symlinks=False).st_size, "sha256": _sha256(entry.path)}
                except OSError as exc:
                    raise FingerprintError(f"cannot read {entry.path}: {exc}") from exc
    return dict(sorted(files.items())), links


def _render(source, skipped, files):
    """The file's text: a few header keys, then one line per file."""
    lines = ["{", f'  "format": {FORMAT},', f'  "source": {json.dumps(source)},',
             f'  "skipped": {json.dumps(skipped)},', '  "files": {']
    entries = [f"    {json.dumps(path)}: {json.dumps(info)}" for path, info in files.items()]
    lines += [",\n".join(entries)] if entries else []
    lines += ["  }", "}"]
    return "\n".join(lines) + "\n"


def _folder_of(value):
    folder = pathlib.Path(value)
    if not folder.is_dir():
        raise FingerprintError(f"{folder} is not a folder")
    return folder.resolve()


def _skips_of(values):
    return sorted({_clean_skip(value) for value in values or []})


def write(folder, out, skips, source):
    folder, out = _folder_of(folder), pathlib.Path(out).resolve()
    _warn_unmatched(folder, skips)
    if out == folder or folder in out.parents:
        raise FingerprintError(f"{out} lies inside {folder}: write the fingerprints outside the folder")
    files, links = fingerprint(folder, skips)
    try:
        with open(out, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(_render(source, skips, files))
    except OSError as exc:
        raise FingerprintError(f"cannot write {out}: {exc}") from exc
    note = f", {links} link(s) left out" if links else ""
    print(f"Wrote {out}: {len(files)} file(s){note}. Skipped folders: {', '.join(skips) or 'none'}.")
    return 0


def _read_old(path):
    """Return (the old file's data, its files). Anything but a fingerprint file is an error."""
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError) as exc:
        raise FingerprintError(f"cannot read {path}: {exc}") from exc
    files = data.get("files") if isinstance(data, dict) else None
    valid = isinstance(files, dict) and all(
        isinstance(info, dict) and isinstance(info.get("size"), int) and isinstance(info.get("sha256"), str)
        for info in files.values())
    if not valid:
        raise FingerprintError(f"{path} is not a fingerprint file written by this script")
    skipped = data.get("skipped")
    data["skipped"] = [item for item in skipped if isinstance(item, str)] if isinstance(skipped, list) else []
    return data, files


def compare(folder, old_path, skips, as_json):
    folder = _folder_of(folder)
    _warn_unmatched(folder, skips)
    data, old_files = _read_old(old_path)
    skips = sorted({*skips, *data["skipped"]})
    old_files = {path: info for path, info in old_files.items() if not _is_skipped(path, skips)}
    new_files, links = fingerprint(folder, skips)
    added = sorted(set(new_files) - set(old_files))
    removed = sorted(set(old_files) - set(new_files))
    changed = sorted(path for path in set(old_files) & set(new_files) if old_files[path] != new_files[path])
    if as_json:
        print(json.dumps({"source": data.get("source"), "skipped": skips, "added": added, "removed": removed,
                          "changed": changed, "compared": len(new_files), "links_left_out": links},
                         ensure_ascii=False, indent=2))
    elif not (added or removed or changed):
        print(f"No file differs ({len(new_files)} file(s) compared, skipped folders: {', '.join(skips) or 'none'}).")
    else:
        print(f"Since {data.get('source') or 'the earlier version'}: {len(added)} added, {len(removed)} removed, "
              f"{len(changed)} changed.")
        for title, paths in (("Added", added), ("Removed", removed), ("Changed", changed)):
            if paths:
                print(f"{title}:")
                print("\n".join(f"  {path}" for path in paths))
    return 1 if added or removed or changed else 0


def _parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    skip_help = "a folder to leave out, relative to <folder>; repeat for each folder"
    writer = commands.add_parser("write", help="write the fingerprints of <folder>")
    writer.add_argument("folder")
    writer.add_argument("out", metavar="out.json")
    writer.add_argument("--skip", action="append", metavar="FOLDER", help=skip_help)
    writer.add_argument("--source", metavar="SRC-n", help="the SRC-n the folder is recorded as")
    comparer = commands.add_parser("compare", help="list what differs from an earlier fingerprint file")
    comparer.add_argument("folder")
    comparer.add_argument("old", metavar="old.json")
    comparer.add_argument("--skip", action="append", metavar="FOLDER", help=skip_help)
    comparer.add_argument("--json", action="store_true", help="print the result as JSON")
    return parser


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = _parser().parse_args(argv)
    try:
        skips = _skips_of(args.skip)
        if args.command == "write":
            if args.source is not None and not SOURCE.match(args.source):
                raise FingerprintError(f"--source {args.source!r} must look like SRC-1")
            return write(args.folder, args.out, skips, args.source)
        return compare(args.folder, args.old, skips, args.json)
    except FingerprintError as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
