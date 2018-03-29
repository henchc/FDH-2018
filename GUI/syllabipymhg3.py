from __future__ import unicode_literals  # for python2 compatibility
# -*- coding: utf-8 -*-
# created at UC Berkeley 2015
# Authors: Christopher Hench, Alex Estes

'''This program contains a function 'syllabipymhg' that syllbifies
Middle High German words for further analysis.
Input is string (word), output is list of strings with syllables.'''

import codecs
import re
import csv  # for generating exception file


def syllabipymhg(word):

    def no_syll_no_vowel(ss):
        # no syllable if no vowel
        nss = []
        front = ""
        for i, syll in enumerate(ss):
            # if following syllable doesn't have vowel,
            # add it to the current one
            if not any(char in vowels for char in syll):
                if len(nss) == 0:
                    front += syll
                else:
                    nss = nss[:-1] + [nss[-1] + syll]
            else:
                if len(nss) == 0:
                    nss.append(front + syll)
                else:
                    nss.append(syll)

        return nss

    # strip extra punctuation and lower case word
    from string import punctuation
    for c in punctuation:
        word = word.replace(c, "")

    word = word.lower()

    # THIS SECTION PREPARES ORTHOGRAPHY AND ASSIGNS VALUE

    # list of basic sounds
    longvowels = "âæāêēîīôœōûū"
    vowels = 'aeiouyàáâäæãåāèéêëēėęîïíīįìôöòóœøōõûüùúūůÿ'  # includes long vowels
    resonants = "lmnrw"
    consonants = "bcdgtkpqvxhçłžsfzj"

    # replace single phonemes represented by
    # multiple letters with single letter
    # THIS IS UNIQUE TO MIDDLE HIGH GERMAN
    if "sch" in word:
        word = word.replace("sch", "ç")
    if "ch" in word:
        word = word.replace("ch", "ł")
    if "ph" in word:
        word = word.replace("ph", "ž")

    vowelcount = 0  # if vowel count is 1, syllable is automatically 1
    sylset = []  # to collect letters and corresponding values

    # cycle through each letter and assign value in SSP (Sonority Sequencing
    # Principle) hierarchy creating list of tuples in sylset
    for letter in word:
        if letter in vowels:
            sylset.append((letter, 3))
            vowelcount += 1  # to check for monosyllabic words
        if letter in resonants:
            sylset.append((letter, 2))
        if letter in consonants:
            sylset.append((letter, 1))

    # THIS SECTION CREATES SYLLABLE BOUNDARIES

    newsylset = []
    if vowelcount == 1:  # finalize word immediately if monosyllabic
        newsylset.append(word)
    if vowelcount != 1:
        syllable = ''  # prepare empty syllable to build upon
        for i, tup in enumerate(sylset):
            if i == 0:  # if it's the first letter, append automatically
                syllable += tup[0]
            # lengths below are in order to not overshoot index
            # when it looks beyond
            else:
                # add whatever is left at end of word, last letter
                if i == len(sylset) - 1:
                    syllable += tup[0]
                    newsylset.append(syllable)

                # accounts for ge prefix in MHG
                elif (i < len(sylset) - 1) and syllable == "ge" and \
                        tup[0] in vowels:
                    # gei and geu are accepted dipthongs in MHG
                    if tup[0] != "i" and tup[0] != "u":
                        # append and break syllable BEFORE appending letter at
                        # index in new syllable
                        newsylset.append(syllable)
                        syllable = ""
                        syllable += tup[0]
                    else:
                        syllable += tup[0]  # accepting dipthongs

                # breaks syllable on vowels followed by long vowels
                elif (i < len(sylset) - 1) and len(syllable) > 0 and \
                        syllable[-1] in longvowels and tup[0] in vowels:
                    # append and break syllable BEFORE appending letter at
                    # index in new syllable
                    newsylset.append(syllable)
                    syllable = ""
                    syllable += tup[0]

                # MAIN ALGORITHM BELOW
                # these cases do not trigger syllable breakS
                elif (i < len(sylset) - 1) and tup[1] < sylset[i + 1][1] and \
                        tup[1] > sylset[i - 1][1]:
                    syllable += tup[0]
                elif (i < len(sylset) - 1) and tup[1] > sylset[i + 1][1] and \
                        tup[1] < sylset[i - 1][1]:
                    syllable += tup[0]
                elif (i < len(sylset) - 1) and tup[1] > sylset[i + 1][1] and \
                        tup[1] > sylset[i - 1][1]:
                    syllable += tup[0]
                elif (i < len(sylset) - 1) and tup[1] > sylset[i + 1][1] and \
                        tup[1] == sylset[i - 1][1]:
                    syllable += tup[0]
                elif (i < len(sylset) - 1) and tup[1] == sylset[i + 1][1] and \
                        tup[1] > sylset[i - 1][1]:
                    syllable += tup[0]
                elif (i < len(sylset) - 1) and tup[1] < sylset[i + 1][1] and \
                        tup[1] == sylset[i - 1][1]:
                    syllable += tup[0]

                # these cases DO trigger syllable break
                # if phoneme value is equal to value of preceding AND following
                # phoneme
                elif (i < len(sylset) - 1) and tup[1] == sylset[i + 1][1] and \
                        tup[1] == sylset[i - 1][1]:
                    syllable += tup[0]
                    # append and break syllable BEFORE appending letter at
                    # index in new syllable
                    newsylset.append(syllable)
                    syllable = ""

                # if phoneme value is less than preceding AND following value
                # (trough)
                elif (i < len(sylset) - 1) and tup[1] < sylset[i + 1][1] and \
                        tup[1] < sylset[i - 1][1]:
                    # append and break syllable BEFORE appending letter at
                    # index in new syllable
                    newsylset.append(syllable)
                    syllable = ""
                    syllable += tup[0]

                # if phoneme value is less than preceding value AND equal to
                # following value
                elif (i < len(sylset) - 1) and tup[1] == sylset[i + 1][1] and \
                        tup[1] < sylset[i - 1][1]:
                    syllable += tup[0]
                    # append and break syllable BEFORE appending letter at
                    # index in new syllable
                    newsylset.append(syllable)
                    syllable = ""

    # THIS SECTION RETURNS ORTHOGRAPHY
    # replace characters treated as one phoneme
    newsylset2 = []
    for syll in newsylset:
        if "ç" in syll:
            syll = syll.replace("ç", "sch")
        if "ł" in syll:
            syll = syll.replace("ł", "ch")
        if "ž" in syll:
            syll = syll.replace("ž", "ph")
        newsylset2.append(syll)

    newsylset = no_syll_no_vowel(newsylset2)

    # read csv of corrections from list generated for compound issues
    # list is generated with onset.py
    tofix = []
    with open("/Users/chench/Box Sync/Hench_Dissertation/diss/code/scripts/corrections.csv", encoding="utf-8") as f:
        data = [tuple(line)
                for line in csv.reader(f)]  # yields tuples with len 4
        for tup in data:  # change asterisks to blanks in the tuple
            if tup[0] == "*":
                tofix.append(("", tup[1], tup[2], tup[3]))
            elif tup[1] == "*":
                tofix.append((tup[0], "", tup[2], tup[3]))
            elif tup[2] == "*":
                tofix.append((tup[0], tup[1], "", tup[3]))
            elif tup[3] == "*":
                tofix.append((tup[0], tup[1], tup[2], ""))
            else:
                tofix.append(tup)

    for correction in tofix:
        newsylset2 = []
        for i, syll in enumerate(newsylset):
            # to break up two characters in following syllable, first string of
            # tuple is blank
            if len(correction[0]) == 0:
                if (i < len(newsylset) - 1) and \
                    newsylset[i + 1][:(len(correction[1]))] == \
                        correction[1]:
                    syll = syll + correction[2]
                    newsylset2.append(syll)
                elif i > 0 and syll[:len(correction[1])] == correction[1]:
                    syll = syll[len(correction[2]):]
                    newsylset2.append(syll)
                else:
                    newsylset2.append(syll)

            # to switch characters between words, first string of tuple not
            # blank
            elif len(correction[0]) > 0:
                if (i < len(newsylset) - 1) and syll[-len(correction[0]):] == \
                        correction[0] and \
                        newsylset[i + 1][:len(correction[1])] == \
                        correction[1]:
                    syll = syll[:-len(correction[0])] + correction[2]
                    newsylset2.append(syll)
                elif i > 0 and newsylset[i - 1][-len(correction[0]):] == \
                        correction[0] and syll[:len(correction[1])] == \
                        correction[1]:
                    syll = correction[3] + syll[len(correction[1]):]
                    newsylset2.append(syll)
                else:
                    newsylset2.append(syll)

            # to break up two characters in current syllable, necessary?
            elif len(correction[1]) == 0:
                if (i < len(newsylset) - 1) and syll[-len(correction[0]):] == \
                        correction[0]:
                    syll = syll[:-len(correction[0])] + correction[2]
                    newsylset2.append(syll)
                elif i > 0 and newsylset[i - 1][-len(correction[0]):] == \
                        correction[0]:
                    syll = syll[len(correction[2]):]
                    newsylset2.append(syll)
                else:
                    newsylset2.append(syll)

        # use new sylset created after each fix, so multiple fixes can be used
        # on same set
        newsylset = newsylset2

    # handling ch intervocalically c-h
    newsylset2 = []
    for i, syll in enumerate(newsylset):
        if (i < len(newsylset) - 1) and syll[-1] in vowels and \
                newsylset[i + 1][:2] == 'ch' and newsylset[i + 1][2] in vowels:
            syll = syll + 'c'
            newsylset2.append(syll)
        elif (i > 0) and newsylset[i - 1][-1] in vowels and syll[:2] == \
                'ch' and syll[2] in vowels:
            syll = syll[1:]
            newsylset2.append(syll)
        else:
            newsylset2.append(syll)

    newsylset = newsylset2

    # handling sch intervocalically

    newsylset2 = []
    for i, syll in enumerate(newsylset):
        if (i < len(newsylset) - 1) and len(syll) > 2 and syll[-1] in vowels \
            and syll[-2] != 'g' and len(newsylset[i + 1]) > 3 and \
            newsylset[i + 1][:3] == 'sch' and \
                newsylset[i + 1][3] in vowels:
            syll = syll + 's'
            newsylset2.append(syll)
        elif (i > 0) and len(newsylset[i - 1]) > 3 and newsylset[i - 1][-1] \
                in vowels and newsylset[i - 1][-2] != 'g' and len(syll) > 2 \
                and syll[:3] == 'sch' and syll[3] in vowels:
            syll = syll[1:]
            newsylset2.append(syll)
        else:
            newsylset2.append(syll)

    newsylset = newsylset2

    # handling long vowel + short vowel (breaking up)
    newsylset2 = []
    for i, syll in enumerate(newsylset):
        if len(syll) >= 2 and syll[-2] in longvowels and syll[-1] in vowels:
            syll = syll[:-1]
            newsylset2.append(syll)
        elif (i > 0) and len(newsylset[i - 1]) >= 2 and newsylset[i - 1][-2] \
                in longvowels and newsylset[i - 1][-1] in vowels:
            syll = newsylset[i - 1][-1] + syll
            newsylset2.append(syll)
        else:
            newsylset2.append(syll)

    newsylset = newsylset2

    # handling 'lich'
    lichreg = re.compile(r"l(i|î)ch")
    licreg = re.compile(r"l(i|î)c")

    if re.search(lichreg, ''.join(newsylset)):
        fix = True
        for i, syll in enumerate(newsylset):
            if licreg.match(syll[:3]):
                fix = False
                lic_ind = False
            elif re.search(licreg, syll):
                lic_ind = i
                lic_str_ind = re.search(licreg, syll).start()
            else:
                fix = False
                lic_ind = False

        if fix and lic_ind:
            newsylset2 = newsylset[:lic_ind - 1]
            newsylset2.append(newsylset[lic_ind - 1] +
                              newsylset[lic_ind][:lic_str_ind])
            newsylset2.append(newsylset[lic_ind][lic_str_ind:])
            newsylset = newsylset2 + newsylset[lic_ind + 1:]

    # handling 'heit' at end of word
    newsylset2 = []
    for i, syll in enumerate(newsylset):
        if (i < len(newsylset) - 1) and len(newsylset[i + 1]) > 4 and \
                newsylset[i + 1][-4:] == "heit":
            syll = syll + newsylset[i + 1][:-4]
            newsylset2.append(syll)
        elif syll[-4:] == "heit":
            syll = syll[-4:]
            newsylset2.append(syll)
        else:
            newsylset2.append(syll)

    newsylset = no_syll_no_vowel(newsylset2)

    return (newsylset)

if __name__ == '__main__':
    # use this to check words, DO NOT USE special characters, will not display
    # due to terminal encoding
    print(syllabipymhg("richtigheite"))
