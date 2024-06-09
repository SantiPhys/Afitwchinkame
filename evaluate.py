"""
This script evaluates the performance of the KyTea models obtained by
training with a corpus made out of Wikipedia kaiju articles.

It uses the number of unknown words, as well as the Levenshtein (edit)
distance between the predicted string and the ground truth (King Kong's Wikipedia page)

Written by Santiago Poveda Gutiérrez, 2024/06
"""

import os
from Levenshtein import distance
import matplotlib.pyplot as plt

#####################################################
# 0. DEFINE NECESSARY FUNCTIONS FOR MODULARITY      #
#####################################################

def unknown_count(file_tagged):
    """
    Returns the number of UNK predictions (when there's an unknown 
    input charachter string) in a tagged (prediction) file
    """
    with open(file_tagged, 'r', encoding='utf-8') as file:
        text = file.read()

    # Count the occurrences of the string '/UNK'
    count = text.count('/UNK')
    return count


def word_count(file_tagged):
    """
    Returns the number of words present in a tagged file
    """
    with open(file_tagged, 'r', encoding='utf-8') as file:
        text = file.read()
    return len(text.split())


def string_from_tagged(tagged_file):
    """
    Returns a string composed of the concatenated tags of a file
    tagged in KyTea format (tag separator is '/')
    """
    with open(tagged_file, 'r', encoding='utf-8') as file:
        text = file.read()

    text = text.split()
    string = ''
    for word in text:
        string += word.split('/')[1]

    return string

#####################################################
# 1. DEFINE NAME OF FILES CONTAINING PRED & GTRUTH  #
#####################################################

data_dir = 'data/'
# Iterate over the files in the directory to create pred_files
pred_files_L1SVM, pred_files_L2SVM = [], []
for filename in os.listdir(data_dir):
    # Check if the filename contains the required strings
    if '_L1SVM_king_kong_pred.' in filename:
        pred_files_L1SVM.append(filename)
    
    elif '_L2SVM_king_kong_pred.' in filename:
        pred_files_L2SVM.append(filename)

gtruth_file = data_dir + 'king_kong_eval.full'
gtruth_tot_words = word_count(gtruth_file)
gtruth_string = string_from_tagged(gtruth_file)


#####################################################
# 2. COMPUTE METRICS FOR EACH OF THE MODELS         #
#####################################################

def get_metrics(pred_files, gtruth_string, gtruth_tot_words):
    
    n_kaijus, lev_ratio, unk_ratio = [], [], []
    for pred_file in pred_files:
        pred_string = string_from_tagged(data_dir + pred_file)

        # compute metrics
        n_kaijus.append(int(pred_file.split('_')[0]))
        unk_ratio.append(unknown_count(data_dir + pred_file)/gtruth_tot_words)
        lev_ratio.append(distance(gtruth_string, pred_string)/len(pred_file))

    return n_kaijus, lev_ratio, unk_ratio
    # print('# of kaijus in model: ', n_kaijus[-1])
    # print('ratio of unknown words: ', unk_ratio[-1])
    # print('Levenshtein distance between pred and gtruth: ', lev[-1])
    # print('\n')

def sort_by_n_kaijus(n_kaijus, lev_ratio, unk_ratio):
    """
    Function that sorts the metric lists by the number of kaijus
    in the training corpus
    """
    zipped = list(zip(n_kaijus, lev_ratio, unk_ratio))
    zipped = sorted(zipped)
    n_kaijus, lev_ratio, unk_ratio = zip(*zipped)
    return list(n_kaijus), list(lev_ratio), list(unk_ratio)

# Compute the numer of kaijus, the edit distance, and the ratio of unknown words
n_kaijus_L2SVM, lev_ratio_L2SVM, unk_ratio_L2SVM = get_metrics(pred_files_L2SVM, gtruth_string, gtruth_tot_words)
n_kaijus_L2SVM, lev_ratio_L2SVM, unk_ratio_L2SVM = sort_by_n_kaijus(n_kaijus_L2SVM, lev_ratio_L2SVM, unk_ratio_L2SVM)
n_kaijus_L1SVM, lev_ratio_L1SVM, unk_ratio_L1SVM = get_metrics(pred_files_L1SVM, gtruth_string, gtruth_tot_words)
n_kaijus_L1SVM, lev_ratio_L1SVM, unk_ratio_L1SVM = sort_by_n_kaijus(n_kaijus_L1SVM, lev_ratio_L1SVM, unk_ratio_L1SVM)


#####################################################
# 3. DISPLAY AND SAVE RESULTS FOR EACH MODEL        #
#####################################################

# Create figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=100)

# Plot edit distance against number of kaijus
ax1.plot(n_kaijus_L2SVM, lev_ratio_L2SVM, marker='o', color='b', linestyle='-', linewidth=2, markersize=8, label='L2')
ax1.plot(n_kaijus_L1SVM, lev_ratio_L1SVM, marker='o', color='r', linestyle='-', linewidth=2, markersize=8, label='L1')
ax1.set_title('Levenshtein Distance Ratio vs. Number of Kaijus', fontsize=14)
ax1.set_xlabel('Number of Kaijus', fontsize=12)
ax1.set_ylabel('LDR', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend()

# Plot number of unknown inputs against number of kaijus
ax2.plot(n_kaijus_L2SVM, unk_ratio_L2SVM, marker='o', color='g', linestyle='-', linewidth=2, markersize=8, label='L2')
ax2.plot(n_kaijus_L1SVM, unk_ratio_L1SVM, marker='o', color='orange', linestyle='-', linewidth=2, markersize=8, label='L1')
ax2.set_title('Unknown Ratio vs. Number of Kaijus', fontsize=14)
ax2.set_xlabel('Number of Kaijus', fontsize=12)
ax2.set_ylabel('Unknown Ratio', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend()

# Show the plots and save figures
plt.tight_layout()
plt.show()
fig.savefig('results/eval_standard.png', bbox_inches='tight')
