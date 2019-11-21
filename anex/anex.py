from pathlib import Path
from anex.utils import edits2
import pandas as pd
import logging
import sys

# Set up logger
logger = logging.getLogger("AnnotationExplorer")
stream_handler = logging.StreamHandler(sys.stdout)
log_format = '%(asctime)s [%(levelname)s] %(name)s - %(message)s'
formatter = logging.Formatter(log_format)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)


# TODO add write method (to csv)
class AnnotationExplorer:

    def __init__(self, path, annot_col_name, sep=',', encoding='utf8'):
        self.annot_data_path = Path() / path
        self.annot_col_name = annot_col_name
        self.separator = sep
        self.encoding = encoding
        self.annot_df: pd.DataFrame = pd.read_csv(self.annot_data_path,
                                                  sep=self.separator,
                                                  encoding=self.encoding)
        if self.annot_col_name not in self.annot_df.columns:
            raise ValueError("Missing annotation column in file [{}]".format(
                annot_col_name))

    def value(self):
        return self.annot_df

    def clean(self):
        initial_label_count = len(self.annot_df)
        # Dropping rows with missing annotations
        self.annot_df.dropna(subset=[self.annot_col_name], inplace=True)
        na_rows_count = initial_label_count - len(self.annot_df)
        logger.info('Dropped %s (na) rows', na_rows_count)
        # Putting all annotations in lower case
        self.annot_df[self.annot_col_name] = \
            self.annot_df[self.annot_col_name] \
                .map(lambda annot: annot.lower().strip())
        # Removing duplicates
        duplicated_rows_count = self.annot_df.duplicated().sum()
        self.annot_df.drop_duplicates(inplace=True)
        logger.info('Dropped %s (duplicated) rows', duplicated_rows_count)
        return na_rows_count, duplicated_rows_count

    def filter(self, pattern=None, out=False, inplace=True):
        if pattern is None and not inplace:
            return self.annot_df
        if pattern is not None:
            contains_pattern = self.annot_df[self.annot_col_name].str \
                .contains(pattern)
            if out and inplace:
                self.annot_df = self.annot_df[~contains_pattern]
                return self
            if out and not inplace:
                return self.annot_df[~contains_pattern]
            if not out and inplace:
                self.annot_df = self.annot_df[contains_pattern]
                return self
            if not out and not inplace:
                return self.annot_df[contains_pattern]

    def find_misspelled_candidates(self, word):
        candidates = set(edits2(word.lower().strip()))
        unique_labels = set(self.annot_df[self.annot_col_name])
        tokens = set([token for label in unique_labels
                      for token in label.split(' ')])
        return candidates.intersection(tokens)
