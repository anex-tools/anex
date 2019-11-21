from anex.anex import AnnotationExplorer
from anex.utils import *
from copy import deepcopy
import streamlit as st
import pandas as pd
import re

DATASET_PATH = 'tests/epilepsy_tweets.csv'
ANNOTATION_COL_NAME = 'full_text'
ENCODING = 'utf8'


@st.cache
def load_annot_dataset(filepath,
                       label_col_name,
                       encoding) -> AnnotationExplorer:
    annot_data_analyzer = AnnotationExplorer(filepath, label_col_name,
                                             encoding=encoding)
    return annot_data_analyzer


annot_analyzer_data = load_annot_dataset(DATASET_PATH,
                                         ANNOTATION_COL_NAME,
                                         ENCODING)
annot_analyzer = deepcopy(annot_analyzer_data)

'''
# Annotation Analysis App
This very simple webapp allows you to explore a dataset of annotations.

## Description
'''
st.write("Dataset path : {} (".format(DATASET_PATH),
         annot_analyzer.value().shape[0], 'rows )')
st.write('Here is a sample :')
st.write(annot_analyzer.value().sample(3, random_state=42))
na_rows_count, duplicated_rows_count = annot_analyzer.clean()
st.write("Cleaning removed ", na_rows_count, ' missing annotations and ',
         duplicated_rows_count, " duplicates.")

'''
## Most represented words in annotations
Displays a histogram of the most represented words in the dataset.
'''
word_occurrences = st.slider('top', 5, 50, 10)
word_serie = pd.Series(annot_analyzer.value()[ANNOTATION_COL_NAME]
                       .map(lambda annot: re.compile(r'\s').split(annot))
                       .sum())
top_N_words_by_count = select_by_count(
    input_serie=word_serie,
    top=word_occurrences)
plot_histogram(top_N_words_by_count, "Top {} cleaned words".format(
    word_occurrences))
st.pyplot(bbox_inches='tight')

'''
## Filter out dataset
Filters out annotations corresponding to any of the following constraints :
'''
filter_pattern = st.text_input('Enter a pattern (regex allowed) you want '
                               'to filter out')
if filter_pattern != '':
    filtered_label_df = annot_analyzer.filter(pattern=filter_pattern, out=True)
    st.write(filtered_label_df.value().shape[0],
             " annotation(s) remaining after filtering")
    st.write(filtered_label_df.value())
    if st.checkbox('Show histogram'):
        remaning_word_serie = pd.Series(
            annot_analyzer.value()[ANNOTATION_COL_NAME]
                .map(lambda annot: re.compile(r'\s').split(annot))
                .sum()
        )
        top_N_remaining_words_by_count = select_by_count(
            remaning_word_serie,
            top=30)
        plot_histogram(top_N_remaining_words_by_count,
                              "Top {} remaining labels"
                              .format(30))
        st.pyplot(bbox_inches='tight')
