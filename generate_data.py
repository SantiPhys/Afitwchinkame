"""
This script scrapes text from a list of Wikipedia URLs containing kaiju information
and creates the necessary output files to train and evaluate the fitwchinme model.

For our corpus, we have selected the Wikipedia articles of the 9 most iconic kaiju 
of Japanese origin (Toho studies) according to screen rant:
    https://screenrant.com/godzilla-most-iconic-kaiju-ranked/

Then we create evaluation sets out of the King Kong article, to test the dialectic 
strength of the Japanese monsters against their most famous Hollywood counterpart:
    https://en.wikipedia.org/wiki/King_Kong

Written by Santiago Poveda Gutiérrez, 2024/06
"""

import re
import requests
from bs4 import BeautifulSoup


#####################################################
# 0. DEFINE NECESSARY FUNCTIONS FOR MODULARITY      #
#####################################################


def substitute_word(word):
    """
    This function substitute every word on a list with 
    its first two characters + "/" + the original word
    """
    if len(word) > 1:
        return f"{word[:2]}/{word}"
    else:
        return f"{word}/{word}"


def word_to_2char(word):
    """
    This function substitute every word on a list with 
    its first two characters + "/" + the original word
    """
    if len(word) > 1:
        return word[:2]
    else:
        return word


def tag_text(text):
    """
    This function processes text and tags it in an input
    format suitable for KyTea training
    """
    # Remove text within square brackets
    text = re.sub(r'\[.*?\]', '', text)
    # Remove words containing special characters (excluding space and punctuation and so on)
    text = re.sub(r'\b\w*[^\w\s]+\w*\b', '', text)
    # Replace slashes with spaces
    text = text.replace('/', ' ')
    # Replace three dots with one dot
    text = text.replace('...', '.')
    # Replace & with and
    text = text.replace('&', 'and')
    # Add spaces before and after punctuation signs
    text = re.sub(r"([.,:;!?()])", r" \1 ", text)

    # Tokenize text and process each word
    words = text.split()
    words = [word for word in words if word]    # Filter out empty strings
    tagged_words = [substitute_word(word) for word in words]

    # Join processed words into a single string
    tagged_text = ' '.join(tagged_words)
    tagged_text = tagged_text.replace('./. ', './.\n')

    return tagged_text


def text_to_2char(text, eval):
    """
    This function processes text and leaves only the first
    two charachters of each token, in a format suitable
    for KyTea evaluation
    """
    if eval:
        # Remove text within square brackets
        text = re.sub(r'\[.*?\]', '', text)
        # Remove words containing special characters (excluding space and punctuation and so on)
        text = re.sub(r'\b\w*[^\w\s]+\w*\b', '', text)
        # Replace slashes with spaces
        text = text.replace('/', ' ')
        # Replace three dots with one dot
        text = text.replace('...', '.')
        # Replace & with and
        text = text.replace('&', 'and')
        # Add spaces before and after punctuation signs
        text = re.sub(r"([.,:;!?()])", r" \1 ", text)
        
        # Tokenize text and process each word
        words = text.split()
        words = [word for word in words if word]        # Filter out empty strings
        words_2char = [word_to_2char(word) for word in words]
        
        # Join processed words into a single string
        text_2char = ''.join(words_2char) + '\n'
        
        return text_2char
    
    else:
        print("text_to_2char is being called even when is_eval is false \
              \n-> returning None")
        return None


#####################################################
# 1. DOWNLOAD WIKIPEDIA TEXT ABOUT KAIJUS           #
#####################################################


# List of Wikipedia article URLs. The URLs used for
# testing need to be at the end of the list
n_testing_urls = 1
urls_ordered  =  [
    'https://en.wikipedia.org/wiki/Godzilla',
    'https://en.wikipedia.org/wiki/Mothra',
    'https://en.wikipedia.org/wiki/King_Ghidorah',
    'https://en.wikipedia.org/wiki/Mechagodzilla',
    'https://en.wikipedia.org/wiki/Biollante',
    'https://en.wikipedia.org/wiki/Gigan',
    'https://en.wikipedia.org/wiki/Rodan',
    'https://en.wikipedia.org/wiki/Hedorah',
    'https://en.wikipedia.org/wiki/Godzilla_vs._Destoroyah',
    'https://en.wikipedia.org/wiki/King_Kong'
    ]


# Output file names
output_files = ['data/' + str(n_kaijus) + '_kaiju_corpus.raw' \
                for n_kaijus in range(1, len(urls_ordered) + 1 - n_testing_urls)]
output_files.append('data/king_kong_eval.raw')

# If true it will stop the cumulative writing
# and also create a .2char file for input to KyTea
is_eval = [False] * (len(output_files)-n_testing_urls)
is_eval += [True] * n_testing_urls

# Write text from articles into their appropriate file, cumulatively
article_text = ''
for output_file, url, eval in zip(output_files, urls_ordered, is_eval):

    # Open the output file in write mode
    with open(output_file, 'w', encoding='utf-8') as file:

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the main content of the article
            content = soup.find(id='bodyContent')

            # Extract text from the paragraphs
            paragraphs = content.find_all('p')

            if eval:
                # Write the text of the current article to the file
                article_text = '\n'.join([para.get_text() for para in paragraphs])
                file.write(article_text + '\n\n')  # Separate articles with double newline

                print(f"{url.split('/')[-1]}'s article has been saved to '{output_file}'")

            else:
                # Combine the text from all paragraphs untill now
                article_text += '\n'.join([para.get_text() for para in paragraphs])
                # Write the article text to the file
                file.write(article_text + '\n\n')  # Separate articles with double newline
                print(f"Articles up to {url.split('/')[-1]} have been saved to '{output_file}'")

        else:
            print(f"Failed to retrieve the article from {url}. \
                    Status code: {response.status_code}")


# #####################################################
# # 2. PREPARE ALL TEXT IN TAGGED FORMAT FOR KyTea    #
# #####################################################

# Read the input text file
input_files = output_files
output_files = [file_name.split('.')[0] + '.full' for file_name in input_files]

# Loop to transform the text into tagged format
for input_file, output_file, eval in zip(input_files, output_files, is_eval):
    with open(input_file, 'r', encoding='utf-8') as file:
        input_text = file.read()

    # Process the text
    processed_text = tag_text(input_text)

    # Write the processed text to an output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(processed_text)

    print(f"Tagged text has been saved to '{output_file}'.")

    # Create processed
    if eval:
        # Process the text
        processed_text = text_to_2char(input_text, eval)
        output_file = output_file.split('.')[0] + '.2char'

        # Write the processed text to an output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(processed_text)

        print(f"Text in two charachter format has been saved to '{output_file}'.")
