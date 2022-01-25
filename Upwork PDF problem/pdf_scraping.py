from PyPDF2 import PdfFileReader
import pandas as pd
import re

def pdf_reader(pdf_path):
    names = []
    addresses = []

    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        number_of_pages = pdf.getNumPages()
        for i in range(number_of_pages):
            page = pdf.getPage(i)
            text = page.extractText()
            # print(text)
            pattern = re.compile(r'Case\sNumber\:.*?Details\sof\sApplication', re.DOTALL)
            matches = pattern.finditer(text)
            for match in matches:
                # print(match.group())
                pattern2 = re.compile(r'\bCase\sNumber:.*?T.*?\d{5,}', re.DOTALL)
                matches2 = pattern2.finditer(match.group())
                for match2 in matches2:
                    # print(match2.group())
                    start_index = match2.span()[1]
                    match3 = match.group()[start_index:].split("Details of Application")[0].strip()
                    # print(match3)
                    final_pattern = re.compile(r'\s{4,}')
                    final_matches = final_pattern.finditer(match3)
                    for final_match in final_matches:
                        start_space = final_match.span()[0]
                        end_space = final_match.span()[1]
                        name = match3[:start_space].strip().replace("\n", " ").strip()
                        address = match3[end_space:].strip().replace("\n", " ").strip()
                        # print(name)
                        # print(address)
                        # print()
                        names.append(name)
                        addresses.append(address)
    zipped_list = list(zip(names,addresses))
    columns = ["Names", "Addresses"]
    df = pd.DataFrame(zipped_list, columns=columns)
    print(df.head())
    df.to_excel('business_list.xlsx', index = False)

pdf_reader('Bulletin_12_29_21_.pdf')