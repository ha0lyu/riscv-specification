#!/usr/bin/env python3
"""
convert_pdfs_to_md.py

Batch convert PDF files in a specified directory to Markdown using the `markitdown` CLI,
saving outputs under the directory's `markdown/` subdirectory.

Usage:
    python convert_pdfs_to_md.py /path/to/dir
    python convert_pdfs_to_md.py /path/to/dir --recursive --workers 4 --overwrite

Requirements:
    - The `markitdown` command must be installed and available in PATH
    - Python 3.8+
"""
from pathlib import Path
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys

def run_markitdown(pdf_path: Path, out_path: Path) -> tuple:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["markitdown", str(pdf_path), "-o", str(out_path)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return (pdf_path, True, proc.stdout or proc.stderr or "")
    except subprocess.CalledProcessError as e:
        return (pdf_path, False, e.stderr or e.stdout or str(e))

def collect_pdfs(base_dir: Path, recursive: bool):
    if recursive:
        candidates = base_dir.rglob("*.pdf")
    else:
        candidates = base_dir.glob("*.pdf")
    return [p for p in candidates if p.is_file()]

def main():
    parser = argparse.ArgumentParser(description="Batch convert PDFs to Markdown using markitdown")
    parser.add_argument("directory", help="Target directory (contains pdf files)")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively search for pdf files in subdirectories (preserve relative structure)")
    parser.add_argument("-w", "--workers", type=int, default=4, help="Number of parallel worker threads (default 4)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files")
    parser.add_argument("--dry-run", action="store_true", help="List files that would be converted without actually calling markitdown")
    args = parser.parse_args()

    base_dir = Path(args.directory).expanduser().resolve()
    if not base_dir.exists() or not base_dir.is_dir():
        print(f"Error: {base_dir} is not a valid directory", file=sys.stderr)
        sys.exit(2)

    pdfs = collect_pdfs(base_dir, args.recursive)
    if not pdfs:
        print("No PDF files found.")
        return

    out_base = base_dir / "markdown"
    print(f"Found {len(pdfs)} PDF files — outputs will be saved to: {out_base}")

    tasks = []
    for p in pdfs:
        if args.recursive:
            rel = p.relative_to(base_dir)
            out_file = out_base / rel.with_suffix(".md")
        else:
            out_file = out_base / (p.stem + ".md")
        tasks.append((p, out_file))

    if args.dry_run:
        print("Dry run: the following files will be converted → output path")
        for p, o in tasks:
            print(f"{p}  ->  {o}")
        return

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as ex:
        futures = {}
        for p, o in tasks:
            if o.exists() and not args.overwrite:
                print(f"Skipping (already exists): {o}")
                continue
            futures[ex.submit(run_markitdown, p, o)] = (p, o)

        for fut in as_completed(futures):
            p, o = futures[fut]
            try:
                pdf_path, ok, msg = fut.result()
                if ok:
                    print(f"Converted: {pdf_path} -> {o}")
                else:
                    print(f"Failed: {pdf_path}  Error: {msg}", file=sys.stderr)
            except Exception as e:
                print(f"Task exception: {p}  Exception: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()