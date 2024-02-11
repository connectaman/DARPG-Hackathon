from scrapper.dataset_scrape import get_org_code_from_category_code_mapping,get_action_history
from scrapper.document_scrape import PDFExtractor
from scrapper.pgportal_scrape import scrape_table_with_pagination,scrape_faq_from_pgportal,scrape_about_paragraphs

import os, ast, json
from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)


logging.info("# --------- Preparing data from PDF files --------- #")
pdf_files = os.listdir(os.environ["pdf_files_path"])

logging.info("Found "+str(len(pdf_files))+" PDF files")

data = []

for pdf_file in pdf_files:
    logging.info("Extracting pdf file : "+str(pdf_file))
    pdf_content = PDFExtractor(os.path.join(os.environ["pdf_files_path"],pdf_file)).extract()
    data.extend(pdf_content)

logging.info("# --------- Preparing data from PDF files Complete --------- #")

logging.info("# --------- Scraping data from CPGRAMS website --------- #")

logging.info("# --------- Scraping NodalPgOfficers Page --------- #")
res = scrape_table_with_pagination(url=os.environ["NodalPgOfficers"])
data.extend(res)

logging.info("# --------- Scraping NodalPgOfficersState Page --------- #")
res = scrape_table_with_pagination(url=os.environ["NodalPgOfficersState"])
data.extend(res)

logging.info("# --------- Scraping NodalAuthorityForAppeal Page --------- #")
res = scrape_table_with_pagination(url=os.environ["NodalAuthorityForAppeal"])
data.extend(res)

logging.info("# --------- Scraping Faq Page --------- #")
res = scrape_faq_from_pgportal(url=os.environ['Faq'])
data.extend(res)

logging.info("# --------- Scraping AboutUs Page --------- #")
res = scrape_about_paragraphs(url=os.environ["AboutUs"])
data.extend(res)

logging.info("# --------- Scraping data from CPGRAMS website Complete --------- #")

logging.info("# --------- Preparing data from CPGRAMS Dataset --------- #")

# res = get_org_code_from_category_code_mapping(path=os.environ["CategoryCode_Mapping"])
# data.extend(res)

# res = get_action_history(path=os.environ["no_pii_action_history"])
# data.extend(res)

logging.info("# --------- Preparing data from CPGRAMS Dataset Complete --------- #")

with open(os.environ["write_data_path"]+"/data.json","w") as f:
    f.write(str(data))
