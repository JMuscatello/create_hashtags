"""create_hashtags.py 

Python 2.7 script to calculate the n most frequent words appearing in
a given set of text documents and outputs the words, containing documents,
and sentences containing those words to a html table.

OPTIONS:

    -f <file1> <file2> ...
    filenames of text documents to scan

    -n <number of words>
    top n words to output

    --html
    flag to turn on html output - currently only outputs in html

OUTPUT FILES:

    most_common_words.html -HTML table of most common words, containing 
    documents and sentences

EXAMPLE:

    $ python2.7 create_hashtags.py -f doc1.txt doc2.txt -n 5 --html

    Calculates the top 5 words in doc1.txt and doc2.txt and outputs the words,
    containing document names and sentences containing the words to the file
    "most_common_words.html"

ABOUT:

    This revised verison of the code uses the NLTK library to first tokenize
    each document into sentences. This is more general than using regex 
    to do this as it uses a pretrained tokenizer model to extract sentences.
    The word_tokenize routine (which uses regex) is then used to split
    the sentence string into words. 
    
    The words are then counted and matched. In this sense this version of the 
    code can be used more generally for other text sources so long as sentences
    can be idientified with the tokenizer.  

    

--Jordan Muscatello (jordan.muscatello@gmail.com)

"""
import argparse
import re
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize

def initialize_html_table():
    """
    Initializes output file for html table
   
    Returns:
    f_html_out : file object 
          html output
    """
    
    f_html_out = open("most_common_words.html", 'w')
    
    f_html_out.write("<html>\n<head>\n<meta charset=\"utf-8\"/>\n<style>\n")
    f_html_out.write("table, th, td {\n"+
                     "border: 1px solid black;\n"+
                     "border-collapse: collapse;\n"+
                     "} th, td {\n"+
                     "padding: 5px;\n"+
                     "text-align: left;}\n"+
                     "</style>\n </head>\n")

    f_html_out.write("<body>\n")
    f_html_out.write("<h2>Most Common Words in Test Documents</h2>\n")
    f_html_out.write("<table style=\"width:100%\">\n")
    f_html_out.write("<tr>\n<th>Word(#)</th>\n<th>Documents</th>\n"+
                     "<th>Sentences containing the word</th>\n</tr>\n")


    return f_html_out 

def finalize_html_table(f_html_out):
    """
    Finalizes output file for html table
 
    Parameters:
    f_html_out : file object 
          html output
   
    Returns:
    f_html_out : file object 
          html output
    """
    f_html_out.write("</table>\n")
    f_html_out.write("</body>\n")
    f_html_out.write("</html>\n")
    f_html_out.close()

def output_word_html(f_html_out, word, sentences_docs):
    """
    Outputs words, frequency and sentences in html table

    Parameters:
    f_out : file object 
          output file
    word : str 
          word to add table entry
    freq : int
          frequency of word in all documents
    sentence_doc_list : list (str, str) 
          list containing sentence and document tuples 
    """ 
 
    ## Determine containing documents
    #print sentences_docs
 #  for a in sentences_docs: print len(a)
    sentence_list, doc_list = zip(*sentences_docs)
    doc_list = list(set(doc_list))

    ## 
    f_html_out.write("<tr>\n")
    
    ## Output word
    f_html_out.write("<td valign=\"top\">"+word+"</td>\n")

    ## Output containing document
    doc_string = ""
    for doc in doc_list: doc_string += doc+", "
    doc_string = doc_string.rstrip(", ")
    f_html_out.write("<td valign=\"top\">"+doc_string+"</td>\n")

    ## Output sentences
    f_html_out.write("<td>\n")
    for sentence in sentence_list:
        search = re.compile(r'\b(%s)\b' % word, re.I)
        sentence_out = search.sub('<b>\\1</b>', sentence)
        f_html_out.write(sentence_out.encode('utf-8')+"<br>\n")
    f_html_out.write("</td>\n")

    ##
    f_html_out.write("</tr>\n")


def return_counter(f_in_list, n):
    """
    Returns a list of tuples of words and frequency from all files
    Uses regex
   
    Parameters:
    f_in_list : list of file objects
          list of open text files to scan
    n : int 
          n most common words to return

    Returns:
    most_common_words : list of (str, int) 
          containing most common words and respective frequency 
          - from Counter object
    """
    ## concatenate documents
    ## make lower case, add whitespace at end of string
    long_doc = ""
    for f_in in f_in_list:
        long_doc += f_in.read().lower()+" " 
    
    # Use regex to split into words
    words = re.findall(r'\w+\'?\w+?|\b\s\w\b|(?:[A-Z]\.)', long_doc)
    # Use Counter object to find most common words
    most_common_words = Counter(words).most_common(n) 
    return most_common_words   

def return_counter_nltk(f_in_list, n):
    """
    Returns a list of tuples of words and frequency from all files
    Uses NLTK word_tokenize   

    Parameters:
    f_in_list : list of file objects
          list of open text files to scan
    n : int 
          n most common words to return

    Returns:
    most_common_words : list of (str, int) 
          containing most common words and respective frequency 
          - from Counter object
    sentences_docs : list (str, str)
          sentences and containing document name
    """
    
    sent_list = []
    sentences_docs = []
    for f_in in f_in_list:
        doc = f_in.read().decode('utf-8')
            
        # Use NLTK sent_tokenize to split into sentences    
        sentences = sent_tokenize(doc) 
        sent_list.extend(sentences)
        for s in sentences:
            sentences_docs.append((s, f_in.name))
        f_in.close()

    # Use NLTK to split into word tokens
    words = []
    for sent in sent_list:
        words.extend(word_tokenize(sent)) 
  # print words
    # JM - Need to handle punctuation etc
    word_list = []
    for word in words:
        # match anything with alphanumeric characters 
        if re.search(r'\w+', word): 
            word_list.append(word)
    
    # Use Counter object to find most common words
    most_common_words = Counter(word_list).most_common(n) 
    return most_common_words, sentences_docs   

def return_matching_sentence(string, f_in_list):
    """
    Searches for string in all documents, returns list of tuples
    containing sentence and document name - uses regex to locate sentence
    
    Parameters:
    string : str 
          string to locate
    f_in_list : list of file objects 
          list of open input files

    Returns:
    sentence_list : list (str, str) 
          list of tuples containing sentence and document name
    
    """

    sentence_list = []
        
    for i in range(len(f_in_list)):
        f_in_list[i].seek(0)
        sentences = re.findall(r'([^.]*\b'+string+r'\b[^.]*[\.\?\!])', 
                               f_in_list[i].read(), re.I)
        for s in sentences:
            new_s = s.lstrip()
            sentence_list.append((new_s, f_in_list[i].name))
        
    return sentence_list

def return_matching_sentence_nltk(string, sentences_docs):
    """
    Uses NLTK to extract sentences using sent_tokenize. Regex is then used to
    match against word string

    Parameters:
    string : str 
          string to locate
    sentences_docs : list (str, str) 
          list of tuples containing sentence and document name

    Returns:
    sentences_docs_out : list (str, str) 
          list of tuples containing sentence and document name
   
    """

    sentences_docs_out = []
 
    for s, docname in sentences_docs:
        word_flag = False
        words = word_tokenize(s)
        for word in words:
            if word == string:
                word_flag = True
        if word_flag: sentences_docs_out.append((s, docname))
            #   print s , f_in_list[i].name
    return sentences_docs_out



def print_stats(n, most_common_words):
    """
    Displays the top n most common words and their frequencies across all 
    documents
    
    Parameters:
    n : int
          Top n words with highest frequency
    most_common_words : list of (str, str)
          list of tuples containing n most common words and frequencies
    """

    print "Top {} most common words:".format(n)
    i = 1
    print "Word : Frequency"
    for word, freq in most_common_words:
        print "{}. {} : {}".format(i, word, freq) 
        i += 1
     
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, nargs='+',
                        help='list of files to open',
                        required=True)
    parser.add_argument('-n', type=int, 
                        help='output top <n> most common words (default 10)',
                        default=10)
    parser.add_argument('--html', help='writes output to html table', 
                        action='store_true')

    args = parser.parse_args()
    fname_list = args.f
    n = args.n
    html_flag = args.html = True

    if html_flag: f_html_out = initialize_html_table()
        
    ## open files
    f_in_list = []
    for fname in fname_list:
        f_in_list.append(open(fname, 'r'))

    most_common_words, sentences_docs = return_counter_nltk(f_in_list, n)

    print_stats(n, most_common_words) 
  
    print "Generating table..." 
    for word,freq in most_common_words: 
        sentences_docs_out = return_matching_sentence_nltk(word, sentences_docs)
        if html_flag: output_word_html(f_html_out, word, sentences_docs_out)    
   
    if html_flag: finalize_html_table(f_html_out) 
    print "Done."

if __name__ == "__main__":
    main()
    
