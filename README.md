# Frontiers in the Digital Humanities - Digital Literary Studies 2018
Title: A Metrical Analysis of Medieval German Poetry using Supervised Learning <br>
Authors: Alex Estes and Christopher Hench

Abstract: <br>
Middle High German (MHG) epic poetry presents a unique solution to the linguistic changes underpinning the transition from classical Latin poetry, based on syllable length, into later vernacular rhythmic poetry, based on phonological stress. The predominating pattern in MHG verse is the alternation between stressed and unstressed syllables, but syllable length also plays a crucial role. There are a total of eight possible metrical values. Single or half mora syllables can carry any one of three types of stress, resulting in six combinations. The seventh value is a double mora, i.e., a long stressed syllable. The eighth value is an elided syllable. We construct a supervised Conditional Random Field (CRF) model to predict the metrical value of syllables, and subsequently investigate medieval German poets’ use of semantic and sonorous emphasis through meter. The features used are: 1) the syllable’s position within the line, 2) the syllable’s length in characters, 3) the syllable’s characters, 4) elision (last two characters of previous syllable and first two characters of focal syllable), 5) syllable weight, and 6) word boundaries. Additional metrical rules are enforced and marginal probabilities are calculated to yield the most likely legal scansion of a line. The model achieves a macro average F-score of .925 on internal cross-validation and .909 on held-out testing data. We determine that trochaic alternation with a one syllable anacrusis and words carrying clear stress assignment are the easiest for the model to scan. Lines with multiple double morae of syllables with few characters are the most difficult. We then rank all the epic poetry in the Mittelhochdeutsche Begriffsdatenbank (MHDBDB) by the difficulty of the meter. Finally, we investigate the double mora, which MHG poets used to draw attention to chosen concepts. We conclude that poets generally chose to use the double mora to emphasize highly sonorant words.


Data and source code for paper. For an updated model, see [this repository](https://github.com/henchc/MHG_Scansion).

Dependencies:

* `sklearn`
* `nltk`
* `pycrfsuite`
