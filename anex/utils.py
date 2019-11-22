# Credits : generation of variants within 2-edit Levenshtein's distance was
# taken from this crystal clear article from Peter Norvig
# https://norvig.com/spell-correct.html

import matplotlib.pyplot as plt
import numpy as np


def edits1(word):
    """All edits that are one edit away from `word`."""
    letters = 'aàâbcçdeéèêëfghiîïjklmnoœpqrstuüvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    """All edits that are two edits away from `word`."""
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def select_by_count(input_serie,
                    threshold=None,
                    top=None):
    """Computes the number of occurrence per value and select the ones
    beyond an occurrence threshold or the top N most represented ones
    """
    count_by_value = input_serie.value_counts()
    if threshold:
        selected_values = count_by_value[count_by_value >= threshold]
    elif top:
        selected_values = count_by_value.head(top)
    else:
        raise ValueError("Missing selection condition, specify either "
                         "an occurrence threshold (threshold) or a number "
                         "of values you wish to select (top).")
    return selected_values


def plot_histogram(count_by_label, title=''):
    fig, ax = plt.subplots(figsize=(10, 15))
    labels = count_by_label.index.values
    heights = count_by_label.values
    y_pos = np.arange(len(count_by_label))
    ax.barh(y_pos, heights, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    plt.setp(ax.yaxis.get_majorticklabels(), rotation=45)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Number of occurrences')
    # Text on the at the end of each barplot
    for i in range(len(labels)):
        plt.text(x=heights[i] + 0.5, y=y_pos[i], s=str(heights[i]), size=4)
    ax.set_title(title)
    # fig = px.bar(count_by_label) # , x='hour', y='count',
    # color='season',height=400)
    return fig
