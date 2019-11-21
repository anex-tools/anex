from anex.anex import AnnotationExplorer
import pytest


def test_init():
    # Given
    annotation_file = 'tests/epilepsy_tweets.csv'
    annotation_col_name = 'full_text'
    annotation_wrong_col_name = 'annot'

    # When
    anex = AnnotationExplorer(annotation_file, annotation_col_name)

    # Then
    assert anex.value().shape == (1000, 4)
    with pytest.raises(ValueError):
        AnnotationExplorer(annotation_file, annotation_wrong_col_name)


def test_clean():
    # Given
    annotation_file_1 = 'tests/epilepsy_tweets.csv'
    annotation_col_name_1 = 'full_text'
    annotation_file_2 = 'tests/annot_test_file.csv'
    annotation_col_name_2 = 'annotation'

    # When
    anex1 = AnnotationExplorer(annotation_file_1, annotation_col_name_1)
    anex2 = AnnotationExplorer(annotation_file_2, annotation_col_name_2)
    anex1.clean()
    anex2.clean()

    # Then
    assert anex1.value().shape == (1000, 4)
    assert anex2.value().shape == (3, 3)


def test_filter():
    # Given
    annotation_file = 'tests/epilepsy_tweets.csv'
    annotation_col_name = 'full_text'

    # When
    anex = AnnotationExplorer(annotation_file, annotation_col_name)
    unfiltered_df = anex.filter(inplace=False)
    selected_df = anex.filter(pattern='seizure', inplace=False)
    anex.filter(pattern='seizure', out=True)

    # Then
    assert unfiltered_df.shape == (1000, 4)
    assert selected_df.shape == (139, 4)
    assert anex.value().shape == (861, 4)


def test_find_misspelled_candidates():
    # Given
    annotation_file = 'tests/annot_test_file.csv'
    annotation_col_name = 'annotation'
    word_1 = 'crise'
    word_2 = 'chapeau'
    word_3 = 'YuEx'

    # When
    anex = AnnotationExplorer(annotation_file, annotation_col_name)
    anex.clean()

    # Then
    assert anex.find_misspelled_candidates(word_1) == {'cirse', 'crise'}
    assert anex.find_misspelled_candidates(word_2) == set()
    assert anex.find_misspelled_candidates(word_3) == {'yeux'}
