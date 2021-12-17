import os
import subprocess
from datetime import datetime
from os import listdir
from zipfile import ZipFile
import pandas as pd
from os.path import isfile, join
from shutil import copyfile
from tqdm import tqdm
import multiprocessing as mp


def fix_file_format(file):
    with open(file, 'r', encoding="utf8") as f:
        lines = f.readlines()
    with open(file, 'w+', encoding="utf8") as f:
        for line in lines:
            words = line.split()
            f.writelines("\n".join(words))
            f.write("\n")
        f.write("\n")


def yap(file):
    command_01 = "\"" + os.getcwd() + "\yap.exe\" hebma -raw " + file + " -out input.lattice"
    p = subprocess.Popen(command_01, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()
    command_02 = "\"" + os.getcwd() + "\yap.exe\" md -in input.lattice -om output.mapping"
    p = subprocess.Popen(command_02, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()

    os.remove("input.lattice")


def type_A(file):
    with open("output.mapping", encoding="utf8") as f:
        lines = f.readlines()

    with open(file, 'w+', encoding="utf8") as f:
        for line in lines:
            words = line.split()
            if len(words) > 5:
                if not words[5] in ["PREPOSITION", "CONJ", "DEF", "TEMP", "REL"]:
                    if words[3] != '_':
                        f.write(words[3] + " ")
                    else:
                        f.write(words[2] + " ")


def type_B(file):
    with open("output.mapping", encoding="utf8") as f:
        lines = f.readlines()

    with open(file, 'w+', encoding="utf8") as f:
        prev_word_n = 0
        for line in lines:
            words = line.split()
            if len(words) > 7:
                word_n = words[7]

                if word_n != prev_word_n:
                    prev_word_n = word_n
                    if prev_word_n != 0:
                        f.write("&& ")
                    f.write("@@ ")
                if words[3] != '_':
                    f.write(words[3] + " ")
                else:
                    f.write(words[2] + " ")


def my_unzip(docs_list):
    index = 0
    with ZipFile('Clean_Punctuation.zip', 'r') as zipObj:
        listOfFileNames = ["Clean_Punctuation/" + str(n) + ".txt" for n in docs_list]
        for fileName in listOfFileNames:
            zipObj.extract(fileName, 'docs')
            index += 1


def my_csv():
    pd.options.display.max_rows = 102
    df = pd.read_csv('180000.csv', names=["num", "doc", "type"])
    my_docs = df["doc"][:30000].tolist()
    my_docs.sort()
    print(len(my_docs))
    return my_docs


def process_doc(doc):
    _doc = "doc.txt"
    doc_type1 = "docs/type_1/" + doc
    doc_type2 = "docs/type_2/" + doc
    copyfile("docs/Clean_Punctuation/" + doc, _doc)
    fix_file_format(_doc)
    yap(_doc)
    type_A(doc_type1)
    type_B(doc_type2)


def main():
    docs = [f for f in listdir("docs/Clean_Punctuation") if isfile(join("docs/Clean_Punctuation", f))]

    for doc in tqdm(docs[1000:10000]):
        if not isfile(join("docs/type_2", doc)):
            try:
                process_doc(doc)
            except Exception as ex:
                print("ERROR", doc, ex)


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))