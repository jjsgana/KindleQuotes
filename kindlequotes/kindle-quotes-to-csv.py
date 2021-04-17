from itertools import groupby
import re
import pandas as pd
import time
import os
import json

# do not modify | location of the .py file
location = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

# this line defines the name of the file to read and write
filename = os.path.join(location, 'My Clippings.txt')
output = os.path.join(location, 'kindlequotes.csv')


def main():
    """
    1: OpenFileAndSplit
    2: ConsolidateImportantClips
    3: CleanData
    4: ExportToCsv
    """
    ExportToFile(CleanData(ConsolidateImportantClips(OpenFileAndSplit())))


def OpenFileAndSplit():
    """
    * Reads the 'My Clippings.txt' file
    * It Creates chunks after the element '========='
    * converts the file to a list of lists
    """

    with open(filename, 'rb') as f:
        raw_content = f.read().decode('utf-8-sig')
        raw_content = raw_content.splitlines(0)
        raw_content = [x for x in raw_content if x != '']
        raw_content = [list(g) for k, g in groupby(
            raw_content, lambda x:x == '==========') if not k]
        return raw_content


def ConsolidateImportantClips(splittedcontent):
    id_number = 0
    content = []
    for element in splittedcontent:
        # use this to extract everything after ',' which is the date
        c = element[1].find(',') + 2
        id_number += 1
        content.append(
            {   # 1 take book | 2 delete everything inside '()' | 3 delete '()'
                'book':
                re.sub(r'(?<=\().*(?=\))', '', element[0])
                .replace("()", '',).strip(),
                # 1 grab the phrase inside the second parenthesis | 2 delete [' and ']
                'author':
                str(re.findall(r'\(([^()]*)\)$', element[0]))
                .replace("['", '',)
                .replace("']", '').strip(),
                # grab date and position
                'date':
                element[1][c:],
                # 1 grab the numbers | 2 delete [(' , ')] and ', '
                'position':
                str(re.findall(r'(\d+)-(\d+)', element[1]))
                .replace("[('", '',)
                .replace("')]", '')
                .replace("', '", ' - ',).strip(),
                # the quote of the book
                'quote': element[2]
            }

        )
    print(f'processed {id_number} quotes')

    return content


def CleanData(content):
    kindleauthor = 'jjsgana@gmail.com'
    content = pd.DataFrame(content)
    b = content['book'].str.findall(r'.+?(?= - )').str[0].str.strip()
    c = content['book'].str.findall(r'[^-]*$').str[0].str.strip()
    content.loc[(content.author == kindleauthor), 'book'] = c
    content.loc[(content.author == kindleauthor), 'author'] = b
    return content


def ExportToFile(content):
    with open(output, 'w', encoding='utf-8-sig', newline="") as file:
        content.to_csv(file, encoding='utf-8-sig')
    return content


print(f'file written in:\n"{location}"')


main()
