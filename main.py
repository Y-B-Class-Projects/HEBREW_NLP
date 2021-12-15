import os
from zipfile import ZipFile
import pandas as pd


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
    os.system(command_01)

    command_02 = "\"" + os.getcwd() + "\yap.exe\" joint -in input.lattice -os output.segmentation -om output.mapping -oc output.conll"
    os.system(command_02)

    os.remove("input.lattice")
    os.remove("output.conll")
    os.remove("output.segmentation")


def type_A(file):
    with open(file, encoding="utf8") as f:
        lines = f.readlines()

    for line in lines:
        words = line.split()
        if len(words) > 5:
            if not words[5] in ["PREPOSITION", "CONJ", "DEF", "TEMP", "REL"]:
                print(words[3], end=" ")
    print()


def type_B(file):
    with open(file, encoding="utf8") as f:
        lines = f.readlines()
    prev_word_n = 0
    for line in lines:
        words = line.split()
        if len(words) > 7:
            word_n = words[7]

            if word_n != prev_word_n:
                prev_word_n = word_n
                if prev_word_n != 0:
                    print("&&", end=" ")
                print("@@", end=" ")
            print(words[3], end=" ")
    print()


def my_unzip(docs_list):
    index = 0
    with ZipFile('Clean_Punctuation.zip', 'r') as zipObj:
        listOfFileNames = ["Clean_Punctuation/"+str(n)+".txt" for n in docs_list] #zipObj.namelist()
        for fileName in listOfFileNames:
            zipObj.extract(fileName, 'docs')
            index += 1


def my_csv():
    pd.options.display.max_rows = 10
    df = pd.read_csv('180000.csv', names=["num", "doc", "type"])
    my_docs = df["doc"][:30000].tolist()
    my_docs.sort()
    # print(len(my_docs))
    return my_docs


# fix_file_format("input.txt")
# yap("input.txt")
# type_A("output.mapping")
# type_B("output.mapping")
# docs_list = my_csv()
# my_unzip(docs_list)
