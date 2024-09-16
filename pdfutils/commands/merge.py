import os
import re
from pathlib import Path
from pypdf import PdfMerger
import argparse

def subargs(parser:argparse.ArgumentParser):
    parser.add_argument("files", type=str, nargs="+", help='List of PDF files to be merged (Can be glob pattern)')

    parser.add_argument('--output','-o', type=str, default=Path(os.getcwd()).absolute() / 'merged.pdf', help="Where to save the merged pdf")
    parser.add_argument('--reversed', action='store_true', help="Reverses typical order of sorting the PDFs to be merged")

def main(args:argparse.Namespace):
    pdfs = sorted([Path(f).absolute() for f in args.files])
    if args.reversed:
        pdfs = pdfs[::-1]

    _str = ',\n'.join([f"\t{_p}" for _p in pdfs])
    print(f"Merging PDFs:\n{_str}")

    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(pdf)

    merger.write(args.output)
    merger.close()
    print(f"Created: {args.output}")
