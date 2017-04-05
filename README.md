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
    HTML table of most common words, containing document name and sentences

EXAMPLE:

$ python2.7 create_hashtags.py -f doc1.txt doc2.txt -n 5 --html

Calculates the top 5 words in doc1.txt and doc2.txt and outputs the words,
containing document names and sentences containing the words to the file 
"most_common_words.html"

ABOUT THE CODE:

This revised verison of the code uses the NLTK library to first tokenize
each document into sentences. This is more general than using regex 
to do this as it uses a pretrained tokenizer model to extract sentences.
The word_tokenize routine (which uses regex) is then used to split
the sentence string into words. 
    
The words are then counted and matched. In this sense this version of the 
code can be used more generally for other text sources so long as sentences
can be idientified with the tokenizer.

TO DO;

Contractions could be handled in a tidier manner

--Jordan Muscatello (jordan.muscatello@gmail.com)
