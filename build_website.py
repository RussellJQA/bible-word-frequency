"""
Calculates the relative frequencies of each of the words in each chapter.
compared to its frequency in the entire Bible
"""

import csv
import json
import os
import shutil

from get_downloads import get_downloads
from create_kjv_no_subtitles import create_kjv_no_subtitles
from get_bible_data import get_book_nums
from create_raw_freq_data import create_raw_freq_data, get_word_frequency
from write_site_index import write_site_index
from write_examples import write_examples
from write_bible_book_index import write_bible_book_index
from write_bible_chapter import write_bible_chapter


def round_4_to_6_sigfigs(num):
    """ If there are > 4 significant figures to the left of the decimal point:
            Round to the number of sigfits to the left of the decimal point
        Else:
            Round to 4 sigfigs
        Rounding based on:
            https://stackoverflow.com/questions/3410976/how-to-round-a-number-to-significant-figures-in-python/3411731
    NOTE: For words_in_bible = 790663,
          we need to allow for up to 6 sigfigs to the left of the decimal point
    """
    if num >= (10**5):
        return int("%.6g" % num)
    if num >= (10**4):
        return int("%.5g" % num)
    if num >= (10**3):
        return int("%.4g" % num)
    return float("%.4g" % num)


def sort_desc_by_simple_desc_by_weighted_asc_by_word(element):

    sort_key = (-1 * element[1][2], -1 * element[1][3], element[0])
    # -1 * simple_relative_frequency, -1 * weighted_relative_frequency, word

    return sort_key


def get_book_folder(html_folder, book_abbrev):

    zfilled_book_num = str(get_book_nums()[book_abbrev]).zfill(2)
    book_num_name = f"{zfilled_book_num}-{book_abbrev.lower()}"

    book_folder = os.path.join(html_folder, book_num_name)
    os.makedirs(book_folder, exist_ok=True)

    return book_folder


def get_chapter_word_freqs(words_in_bible, words_in_chapter, word_frequencies,
                           word_frequency):

    chapter_word_freqs = {}
    for (chapter_frequency, words) in word_frequencies.items():
        if words != ["TOTAL WORDS"]:
            times_in_chapter = int(chapter_frequency)
            for word in words:
                times_in_bible = word_frequency[word]

                simple_relative_frequency = (words_in_bible *
                                             times_in_chapter) / times_in_bible
                # IOW: words_in_bible * (times_in_chapter / times_in_bible)

                values = [
                    times_in_chapter,
                    times_in_bible,
                    round_4_to_6_sigfigs(simple_relative_frequency),
                    # Below is weighted_relative_frequency (rounded)
                    round_4_to_6_sigfigs((simple_relative_frequency /
                                          words_in_chapter) +
                                         (times_in_chapter - 1)),
                ]

                # weighted_relative_frequency chosen so that (e.g) for Ex. 5's:
                #    8 out of 16 occurrences of straw
                #    1 out of 2 occurrences of dealest
                # weighted_relative_frequency for "straw" > for "dealest"

                # The print() statements below were used (1 at a time) to help
                # to determine what to use for weighted_relative_frequency.

                # if times_in_chapter == times_in_bible:
                #     print(f"\tAll {times_in_chapter} occurrences of {word}")

                # if 2 * times_in_chapter == times_in_bible:
                #     print(
                #         f"\t{times_in_chapter} out of {times_in_bible}"
                #         f" occurrences of {word}"
                #     )

                chapter_word_freqs[word] = values

    return chapter_word_freqs


def get_relative_word_frequency(words_in_bible, word_frequencies,
                                word_frequency):

    words_in_chapter = int(next(iter(word_frequencies)))

    relative_word_frequency = {}
    relative_word_frequency["TOTAL WORDS"] = [words_in_chapter]
    chapter_word_freqs = get_chapter_word_freqs(words_in_bible,
                                                words_in_chapter,
                                                word_frequencies,
                                                word_frequency)
    for chapter_word_freq, values in sorted(
            chapter_word_freqs.items(),
            key=sort_desc_by_simple_desc_by_weighted_asc_by_word):
        relative_word_frequency[chapter_word_freq] = values

    return relative_word_frequency


def write_chapter_csv(words_in_bible, key, csv_fn, relative_word_frequency):

    with open(csv_fn, mode="w", newline="") as csv_file:
        # newline="" prevents blank lines from being added between rows
        writer = csv.writer(csv_file, delimiter=",", quotechar='"')
        writer.writerow([
            "word",
            "numInChap",
            "numInKjv",
            "simpleRelFreq",
            "weightedRelFreq",
        ])
        #   Column header row

        for count, chapter_word_freq in enumerate(relative_word_frequency):
            values = relative_word_frequency[chapter_word_freq]
            if count:  # Data row
                writer.writerow([
                    chapter_word_freq,
                    values[0],
                    values[1],
                    values[2],
                    values[3],
                ])
            else:  # Totals row
                writer.writerow([
                    f"TOTAL ({key})",
                    relative_word_frequency[chapter_word_freq][0],
                    words_in_bible,
                ])


def write_chapter_html(book_abbrev, chapter, relative_word_frequency):

    words_in_chapter = "{:,}".format(relative_word_frequency["TOTAL WORDS"][0])
    del relative_word_frequency[
        "TOTAL WORDS"]  # Not wanted for dict comprehension
    #   OK to do here, since CSVs were already written,
    #   and we're now done with this extra entry

    # Some possible alternatives for the sortable table implementation:
    #   1. https://www.w3schools.com/howto/howto_js_sort_table.asp
    # **2. https://brython.info/gallery/sort_table.html
    # ***3. https://brython.info/gallery/sort_table_template.html
    #   4. https://stefanhoelzl.github.io/vue.py/examples/grid_component/
    #       source at
    #       https://github.com/stefanhoelzl/vue.py/blob/master/examples/grid_component/app.py
    #   5. https://anvil.works/docs/data-tables/
    #           data-tables-in-code#searching-querying-a-table

    # Corresponding .csv column headings:
    #   word, numInChap, numInKjv, simpleRelFreq, weightedRelFreq
    rows = [
        [
            item[0],
            item[1][0],
            "{:,}".format(item[1][1]),  # formats with a 1,000s separator
            "{:,}".format(item[1][2]),
            item[1][3],
        ] for item in relative_word_frequency.items()
    ]

    write_bible_chapter(
        book_abbrev,
        chapter,
        words_in_chapter,
        rows,
        custom_paragraphing=(book_abbrev == "Psa" and chapter == "119"),
    )


def write_chapter_files(words_in_bible, key, book_abbrev, book_folder,
                        relative_word_frequency):

    chapter = key[4:]

    csv_fn = os.path.join(
        book_folder, f"{book_abbrev.lower()}{chapter.zfill(3)}-word-freq.csv")
    write_chapter_csv(words_in_bible, key, csv_fn, relative_word_frequency)

    write_chapter_html(book_abbrev, chapter, relative_word_frequency)


def copy_scripts(html_folder):

    styles_folder = os.path.join(html_folder, "scripts")
    os.makedirs(styles_folder, exist_ok=True)
    shutil.copyfile("scripts/sorttable.js",
                    os.path.join(styles_folder, "sorttable.js"))


def copy_styles(html_folder):

    styles_folder = os.path.join(html_folder, "styles")
    os.makedirs(styles_folder, exist_ok=True)
    shutil.copyfile("styles/style.css", os.path.join(styles_folder,
                                                     "style.css"))
    shutil.copyfile(
        "styles/style-freq-tables.css",
        os.path.join(styles_folder, "style-freq-tables.css"),
    )


def build_web_site():

    html_folder = os.path.join(os.getcwd(), "public_html")
    os.makedirs(html_folder, exist_ok=True)
    copy_scripts(html_folder)
    copy_styles(html_folder)
    get_downloads(
    )  # Download KJV chapter files, GitHub mark, and sorttable.js, if needed
    create_kjv_no_subtitles()

    write_site_index()  # Write master index file
    write_examples()

    # TODO:
    # Refactor using a function which instead of calculating word frequencies
    # in a chapter relative to word frequencies in the Bible,
    # calculates word freq.s in a subunit, relative to word freq.s in a unit.
    # Such a fcn. might be used for calculating (relative) word freq.s for
    # the OT, NT, individual books, daily readings, etc.

    data_dir = os.path.join(os.getcwd(), "data")
    os.makedirs(data_dir, exist_ok=True)

    read_fn = os.path.join(data_dir, "word_frequency_lists_chapters.json")
    if not os.path.exists(read_fn):
        create_raw_freq_data()

    words_in_bible = 790663
    word_frequency = get_word_frequency()

    chapters_relative_word_frequency = {}
    with open(read_fn, "r") as read_file:

        word_frequency_lists_chapters = json.load(read_file)
        for (key, word_frequencies) in word_frequency_lists_chapters.items():
            relative_word_frequency = get_relative_word_frequency(
                words_in_bible, word_frequencies, word_frequency)
            chapters_relative_word_frequency[key] = relative_word_frequency

            book_abbrev = key[0:3]
            if len(key) == 5 and key[4] == "1":  # If chapter 1
                book_folder = get_book_folder(html_folder, book_abbrev)
                write_bible_book_index(book_abbrev)
                print(f"Writing files for {book_abbrev}.")
            write_chapter_files(words_in_bible, key, book_abbrev, book_folder,
                                relative_word_frequency)

    write_fn = os.path.join(data_dir, "chapters_relative_word_frequency.json")
    with open(write_fn, "w") as write_file:
        json.dump(chapters_relative_word_frequency, write_file, indent=4)


def main():
    build_web_site()


if __name__ == "__main__":
    main()
