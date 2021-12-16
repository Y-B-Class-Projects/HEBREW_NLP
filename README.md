# HEBREW_NLP

Python script that processes documents in Hebrew and uses YAP software written by the Hebrew University.

To run the script, download this repository and add all the files from the YAP repository.
The main.py script must be run by python 3.

All the files are inside the folder named docs.
Inside the docs folder there is a folder called Clean_Punctuation where there are 30K articles in Hebrew
First, the script converts those articles into tokens with which it will later be able to perform the natural language processing (NLP).
Creating tokens in Hebrew is not an easy task, so we used a tool written by the Hebrew University called YAP.

Examples of converting a word to a token in Hebrew:
The word "כשאכלתי" will be converted to the words "כש" "אכל" "תי" when the root of the word will be "אכל".

Since YAP is software and not a library for Python, it was necessary for our script to know how to convert the articles according to the requirements of YAP, run YAP and read its products and then convert back to files.
For each article we built two file types and put them in folders named type_1 and type_2.

For example, for the sentence 

"אתמול כשאכלתי ארוחה טובה ראיתי כמה נקודות על הקיר"

The options will be:

1:אכל ארוחה טוב ראה כמה נקודה על קיר

2:אתמול כש אכל תי ארוחה טוב ה ראה תי כמה נקודה ות על ה קיר
