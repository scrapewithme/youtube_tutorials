from PyPDF2 import PdfFileReader
import pandas as pd
import re




def pdf_reader(pdf_path):
    names = []
    addresses = []

    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        # information = pdf.getDocumentInfo()
        # information = pdf.getDocumentInfo()
        addresses = []
        businesses = []
        number_of_pages = pdf.getNumPages()

        for i in range(number_of_pages):
            page = pdf.getPage(i)
            text = page.extractText()
            pattern = re.compile(r"Case\sNumber\:.*?Details\sof\sApplication", re.DOTALL)
            matches = pattern.finditer(text)
            i = 0
            matches_list = []
            for match in matches:
                matches_list.append(match.group())

            pattern2 = re.compile(r"\bCase\sNumber\:.*?T.*?\d{5,}", re.DOTALL)
            for match2 in matches_list:
                matches2 = pattern2.finditer(match2)
                for match3 in matches2:
                    # print(match3.group()) first thing to show
                    end_index = match3.span()[1]
                    match4 = match2[end_index:].split("Details of Application")[0].strip()
                    # print(match4)
                    final_pattern = re.compile(r"\s{4,}")
                    final_matches = final_pattern.finditer(match4)
                    for final_match in final_matches:
                        start_space = final_match.span()[0]
                        end_space = final_match.span()[1]
                        name = match4[:start_space].strip().replace("\n", " ").strip()
                        address = match4[end_space:].strip().replace("\n", " ").strip()
                        print(name)
                        print(address)
                        print()
                        names.append(name)
                        addresses.append(address)
    zipped_list = list(zip(names, addresses))
    columns = ["Names", "Addresses"]
    df = pd.DataFrame(zipped_list, columns = columns)
    df.to_excel('business_list.xlsx', index=False)


pdf_reader('Bulletin_12_29_21_.pdf')
