from PyPDF2 import PdfReader
import tabula
from datetime import datetime
from typing import Optional
from functools import lru_cache
import pandas as pd
from rich import box
from rich.console import Console
from rich.table import Table
import os
from src.schemas import Document
from src.utils import count_tokens

class PDFExtractor():
    def __init__(self,pdf_path):
        self.path = pdf_path
        self.documents = []

    @lru_cache
    def _extract_text(self):
        for p in os.listdir(self.path):
            reader = PdfReader(os.path.join(self.path,p))
            for i,page in enumerate(reader.pages):
                if count_tokens(page.extract_text()) >= 50:
                    self.documents.append(Document(page_content=page.extract_text()))
        return self.documents

    @lru_cache
    def _extract_table(self):
        dfs = tabula.read_pdf(self.path, pages='all')
        res_df = []
        for df in dfs:
            df.dropna(axis=1, thresh = int(0.2*df.shape[0]), inplace=True)
            res_df.append(df)
        return res_df

    @lru_cache
    def _df_to_table(
        pandas_dataframe: pd.DataFrame,
        rich_table: Table,
        show_index: bool = True,
        index_name: Optional[str] = None,
        ) -> Table:

        if show_index:
            index_name = str(index_name) if index_name else ""
            rich_table.add_column(index_name)
            rich_indexes = pandas_dataframe.index.to_list()

        for column in pandas_dataframe.columns:
            rich_table.add_column(str(column))

        for index, value_list in enumerate(pandas_dataframe.values.tolist()):
            row = [str(rich_indexes[index])] if show_index else []
            row += [str(x) for x in value_list]
            rich_table.add_row(*row)

        return rich_table

    @lru_cache
    def extract(self):
        text_content = self._extract_text()
        return text_content
