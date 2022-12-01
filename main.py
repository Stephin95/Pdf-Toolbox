import argparse
from PyPDF2 import PdfMerger
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
import logging


def create_text_file(content, filename, method="w"):
    logging.debug(f"Writing to {filename}")
    with open(filename, method) as f:
        f.write(content)
    return True


def get_pages(reader, writer, pages):

    if pages:
        for page_num in pages:
            # Add all pages to the writer
            page = reader.pages[int(page_num)-1]
            writer.add_page(page)
    else:
        for page in reader.pages:
            writer.add_page(page)

    return writer


def get_arguments():
    parser = argparse.ArgumentParser(
        prog='Pdf Tool Box',
        description='Do various operations on pdfs',
        epilog='----')
    parser.add_argument('filenames', nargs='+',
                        help="File Names", default=".")  # on/off flag
    parser.add_argument('--merge',  action='store_true',
                        help='Merge the files')
    parser.add_argument(
        '--pg', nargs='*',
        help="Page Numbers for relevant Operations",
        default=False)  # on/off flag
    parser.add_argument('--extract_text',  action='store_true',
                        help='Extract text from pdf files')
    parser.add_argument('--decrypt',  action='store_true',
                        help='Decrypt Pdf Files')
    parser.add_argument('--encrypt',  action='store_true',
                        help='Encrypt Pdf Files')
    parser.add_argument('--extract_page',  action='store_true',
                        help='Extract Pdf pages and merge them to a new pdf ')
    args = parser.parse_args()

    logging.debug(
        f"Arguments are: \nFiles :-{args.filenames}\nPage Number :-{args.filenames}\nMerge :-{args.merge}\nExtract Text :-{args.extract_text}\nDecrypt :-{args.decrypt}\nEncrypt :-{args.encrypt}")
    return args


def merge(files):
    logging.debug("Merging Pdfs")
    merger = PdfMerger()
    for pdf in files:
        merger.append(pdf)
    merger.write("merged-pdf.pdf")
    merger.close()


def extract_text(args):
    logging.debug("Extracting Text from Pdfs")
    create_text_file(filename="extracted_text.txt", content="", method="w")
    # extracted_text_list = []
    for file in args.filenames:
        reader = PdfReader(file)
        if args.pg:
            for page_num in args.pg:
                page = reader.pages[int(page_num)-1]
                # extracted_text_list.append(page)
                # print(page.extract_text())
                create_text_file(filename="extracted_text.txt",
                                 content=page.extract_text(), method="a")
        else:
            for page in reader.pages:
                # extracted_text_list.append(page)
                # print(page.extract_text())
                create_text_file(filename="extracted_text.txt",
                                 content=file+str(reader.get_page_number(
                                     page))+page.extract_text(),
                                 method="a")


def decrypt_files(args):
    logging.debug("Decrypting Pdfs")
    for file_name in args.filenames:
        reader = PdfReader(file_name)
        writer = PdfWriter()

        if reader.is_encrypted:
            password = input("Enter password for the pdf")
            reader.decrypt(password)
        writer = get_pages(reader, writer, args.pg)
        # Save the new PDF to a file
        with open(f"{file_name}_decrypted", "wb") as f:
            writer.write(f)


def extract_pages(args):
    logging.debug("Extracting pages")
    for file_name in args.filenames:
        reader = PdfReader(file_name)
        writer = PdfWriter()

        writer = get_pages(reader, writer, args.pg)

        # Save the new PDF to a file
        with open(f"{file_name}_extracted", "wb") as f:
            writer.write(f)


def encrypt_files(args):
    logging.debug("Encrypting Pdfs")
    for file_name in args.filenames:
        reader = PdfReader(file_name)
        writer = PdfWriter()
    # Add all pages to the writer
        writer = get_pages(reader, writer, args.pg)

        password = input("Enter password for the pdf")
        writer.encrypt(password)

    # Save the new PDF to a file
    with open(f"{file_name}_encrypted.pdf", "wb") as f:
        writer.write(f)


def main():
    args = get_arguments()
    if args.merge:
        merge(args.filenames)

    if args.extract_text:
        extract_text(args)

    if args.decrypt:
        decrypt_files(args)

    if args.encrypt:
        encrypt_files(args)

    if args.extract_page:
        extract_pages(args)


if __name__ == "__main__":
    main()
