from pathlib import Path
from pypdf import PdfReader, PdfWriter
import argparse

def subargs(parser: argparse.ArgumentParser):
    parser.add_argument("file", type=str, help="The source PDF file to extract pages from")
    parser.add_argument("pages", type=str, help="Pages to extract, e.g., '1,3-5,7'")
    parser.add_argument("--output", "-o", type=str, default=None, help="Where to save the extracted PDF")

def parse_pages(pages_str):
    """
    Parses a page string like '1,3-5,7' into a list of zero-based page indices.
    """
    pages = set()
    for part in pages_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages.update(range(start - 1, end))
        else:
            pages.add(int(part) - 1)
    return sorted(pages)

def main(args: argparse.Namespace):
    source_pdf = Path(args.file).absolute()
    if not source_pdf.exists():
        raise FileNotFoundError(f"Source file not found: {source_pdf}")

    output_pdf = Path(args.output).absolute() if args.output else source_pdf.with_name(source_pdf.stem + "_extracted.pdf")

    pages_to_extract = parse_pages(args.pages)

    reader = PdfReader(str(source_pdf))
    writer = PdfWriter()

    total_pages = len(reader.pages)
    for page_num in pages_to_extract:
        if page_num < 0 or page_num >= total_pages:
            raise ValueError(f"Page number out of range: {page_num + 1}")
        writer.add_page(reader.pages[page_num])

    with open(output_pdf, "wb") as out_fp:
        writer.write(out_fp)

    print(f"Extracted pages {args.pages} from {source_pdf} -> {output_pdf}")
