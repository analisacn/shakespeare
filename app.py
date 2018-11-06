import os
import re
from collections import Counter
from operator import itemgetter

FILE_DIR = os.path.abspath("docs")


def get_file_list():
    """
    Walk in the directory path to get the list of files to analyse
    :return: list of filenames
    """
    f = []
    for (dirpath, dirnames, filenames) in os.walk(FILE_DIR):
        f.extend(filenames)
    return f


def sanitize(line):
    """
    Clean line from special characters, possesives and pasts
    :param line: string line to clean
    :return: clean line
    """
    line = line.lower()
    punctuation = """!"#$%&()*+,-./:;<=>?@[\]^_`{|}~"""

    line = re.sub('[%s]' % re.escape(punctuation), '', line)
    line = line.replace("'s", '')  # possesives
    line = line.replace("'d", '')  # pasts

    return line


def process_file(filename, word_counter):
    """
    Read and count every occurrences of words
    :param filename:
    :param word_counter: dict with word occurrences
    :return: updated word_counter dict
    """
    filepath = os.path.join("docs", filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError("File {} cannot be found. "
                                "Please retry".format(filename))

    file = open(filepath)
    line = file.readline()

    while line:
        clean_line = sanitize(line)
        word_counter.update(clean_line.split())
        line = file.readline()

    return word_counter


def print_results(counter):
    """
    Create txt file with every word ordered by occurrences (higher to lower)
    :param counter: dict with word occurrences counter
    """
    f = open("used_words.txt", "w")
    for key, value in sorted(counter.items(), key=itemgetter(1), reverse=True):
        f.write(str("{}:{} \n".format(key, value)))
    f.close()


def main():
    all_words = Counter()
    filenames = get_file_list()

    for filename in filenames:
        process_file(filename, all_words)

    print_results(all_words)


if __name__ == '__main__':
    main()
