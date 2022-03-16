import enum
import itertools as it
import re


class Possibility(enum.Enum):
    V = 'vert'
    G = 'Gris'
    J = 'Jaune'


def patternMaker(word: str, pattern: tuple) -> list:
    wordPattern = []
    for i, j in zip(word, pattern):
        match j:
            case Possibility.G:  # Lettre absente
                wordPattern += [f'{i}-']
            case Possibility.J:  # Lettre présente à la mauvaise place
                wordPattern += [f'{i}=']
            case Possibility.V:  # Lettre présente et à la bonne place
                wordPattern += [f'{i}+']
    return wordPattern


with open('dico/liste_francais.txt') as dico:
    wordle = [x.lower().replace('\n', '') for x in dico.readlines() if len(x) == 6]
    print(len(wordle))
for i in wordle:
    if re.search('[^a][^a][^r][^o][^n]', i):
        print(i)