# create_hashtags
Text extraction script in python. This was written as part of an interview process for a company specialising in NLP.   
CREATE_HASHTAGS.PY
==================

Python 2.7 program to calculate the n most frequent words appearing in
a given set of text documents and outputs the words, containing documents,
and sentences containing those words to a html table.

OPTIONS:

 -f <file1> <file2> ...
    filenames of text documents to scan

 -n <number of words>
    top n words to output

 --html
    flag to turn on html output - currently only outputs in html

OUTPUT FILES;

 most_common_words.html
    HTML table of most common words, containing documents and sentences

EXAMPLE:

$ python2.7 create_hashtags.py -f doc1.txt doc2.txt -n 5 --html

Calculates the top 5 words in doc1.txt and doc2.txt and outputs the words,
containing document names and sentences containing the words to the file
"most_common_words.html"

ABOUT THE CODE:

The code predominantly uses the "re" regular expressions package to find
the most common words and subsequently locate these strings as words (using
the "\b" regex option) and extract the containing sentences (for which the
sentence structure must be prescibed). These strings are then processed and
output to an html table.


In this method regex presents some limitations as in this case standard
punctuation is used as a delimiter. Another option would be to use the NLTK
package suite to identify sentence structures and tokens in the text, and use
methods which may be applicable to other text based data, i.e. not limited
to transcripts or prose with regular punctuation.

I made an attempt to use tokenize_sent to extract sentences then search for the
given word string but I ran into encoding problems that I didn't have time
to fix.


--Jordan Muscatello (jordan.muscatello@gmail.com)
