from anex.anex import AnnotationExplorer
from copy import deepcopy
import streamlit as st

DATASET_PATH = 'tests/epilepsy_tweets.csv'
ANNOTATION_COL_NAME = 'full_text'
ENCODING = 'utf8'


@st.cache
def load_annot_dataset(filepath,
                       label_col_name,
                       encoding) -> AnnotationExplorer:
    label_data_analyzer = AnnotationExplorer(filepath, label_col_name,
                                             encoding=encoding)
    return label_data_analyzer


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
## Misspellings
Look for the possible misspelled candidates of a word.
'''
word = st.text_input('Enter a candidate word')
if word != '':
    st.write('The possible misspelled candidates found in the label dataset '
             'are : ', annot_analyzer.find_misspelled_candidates(word))

'''
## Select labels
Select labels containing the following pattern :
'''
select_pattern = st.text_input('Enter a pattern (regex allowed) you want '
                               'to select')
'''
(Regex cheat sheet : https://docs.python.org/3.8/library/re.html)
'''
if select_pattern != '':
    selected_label_df = annot_analyzer.filter(pattern=select_pattern).value()
    st.write(selected_label_df.shape[0], ' label(s) found')
    st.write(selected_label_df)
    unique_labels_selected = selected_label_df[ANNOTATION_COL_NAME].unique()
    tokens = list(set([token for label in unique_labels_selected
                       for token in label.split(' ')]))
    tokens_to_remove = st.multiselect('Filter out label(s) containing these '
                                      'word(s) from results', tokens)
    if tokens_to_remove:
        to_remove_regex = '|'.join(['(\s|^){}(\s|$)'.format(token)
                                    for token in tokens_to_remove])
        filtered_label_df = annot_analyzer \
            .filter(pattern=to_remove_regex, out=True).value()
        st.write(filtered_label_df.shape[0], ' label(s) remaining (on ',
                 selected_label_df.shape[0], ')')
        st.write(filtered_label_df)
