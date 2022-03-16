import enum
import re
import math
from itertools import product


class Possibility(enum.Enum):
    """
        Enumeration représentant les différentes valeurs que peuvent prendre une case Wordle
    """
    V = 'vert'
    G = 'Gris'
    J = 'Jaune'


# Total des combinaisons que peuvent donner Wordle 3**5 possibilités
p = [x for x in product((Possibility.G, Possibility.V, Possibility.J), repeat=5)]


def word_test(word: str, dico_of_word: list) -> float:
    """
    Calcule l'entropie' d'un mot donné d'apparaitre pour toute les 243 possibilités que peuvent donner Wordle
    :param word: le mot qu'on veut évaluer
    :param dico_of_word: la liste contenant tous les mots
    :return: l'entropie du mot
    """
    global p
    proba = [len(filtre(dico_of_word, *pattern_to_regex(pattern_maker(word, i)))) / len(dico_of_word) for i in p]
    ent = entropie(proba)
    print(f"{word}: ", ent)
    return ent


def pattern_maker(word: str, pattern: tuple) -> list:
    """
    Construit un pattern en fonction des différentes couleurs données. Ce pattern va permettre
    la conversion en regex
    :param word: mots donnés
    :param pattern: sequences de couleur dans un tuple
    :return: liste contenant chaque lettre et son signe dans la phrase
    """
    word_pattern = []
    for i, j in zip(word, pattern):
        match j:
            case Possibility.G:  # Lettre absente
                word_pattern += [f'{i}-']
            case Possibility.J:  # Lettre présente à la mauvaise place
                word_pattern += [f'{i}=']
            case Possibility.V:  # Lettre présente et à la bonne place
                word_pattern += [f'{i}+']
    return word_pattern


def pattern_to_regex(word_pattern: list) -> tuple:
    """
    Convertit le pattern en regex
    :param word_pattern:
    :return:
    """
    pattern = ""
    bad_place = []
    not_include = []
    for i in word_pattern:
        match i[1]:
            case '+':
                pattern += i[0]
            case '-':
                pattern += f'[^{i[0]}]'
                not_include += i[0]
            case '=':
                pattern += f'[^{i[0]}]'
                bad_place += i[0]
    return pattern, bad_place, not_include


def filtre(dico_of_word: list, pattern: str, bad_place: list, not_include: list):
    """
    Filtre le dictionnaire dicoOfWord en ne sélectionnant que les mots vérifiant le modèle et contenant les lettres de
    la liste badPlace. De plus il s'assure que les mots sélectionnés ne contiennent aucun character de notInclude
    :param dico_of_word: dictionnaire à filtrer(list)
    :param pattern: modèle correspondant au mot recherché
    :param bad_place: liste de caractère inclut dans les mots voulus qui sont toutefois à la mauvaise place
    :param not_include: liste de caractère non inclut dans les mots
    :return: dictionnaire filtré
    """
    return [i for i in dico_of_word if re.search(pattern, i) and all(j in i for j in bad_place) and
            all(j not in i for j in not_include)]


def pattern_interpreter(pattern: str) -> tuple:
    """
    Convertir le model obtenue par l'utilisateur en un modèle comprehensible par le programme
    :param pattern: modèle entré par l'utilisateur
    :return: Tuple contenant des valeurs de l'énumération Possibility
    """
    interpretation = []
    for i in pattern:
        match i:
            case 'V':
                interpretation += [Possibility.V]
            case 'G':
                interpretation += [Possibility.G]
            case 'J':
                interpretation += [Possibility.J]
    return tuple(interpretation)


def entropie(probability: list) -> float:
    """
    Calcule l'entropie de la liste des probablité donné
    :param probability: liste des probabilités
    :return: liste des probabilités
    """
    x = [math.log(1 / k, 2) for k in probability if k != 0]
    return sum(i * j for i, j in zip(x, probability))


if __name__ == '__main__':
    with open('dico/francais.txt') as dico:
        wordle = [x.lower().replace('\n', '') for x in dico.readlines() if (re.match('^[a-z]{5}$', x))]
    #best_word = max([(x, word_test(x, wordle)) for x in wordle], key=lambda x: x[1])[0]
    best_word = "jeton"
    #best_word = "visas"
    print("Le meilleur mot est: ", best_word)
    word_input = input("Quelle mot aviez vous saisi: ").lower()
    while 1:
        patternResult = input("Quelle est le model que vous aviez obtenue: (V:Vert, G:Gris, J:Jaune) ").upper()
        if patternResult == "stop":
            print("Merci d'avoir joué")
            break
        wordle = list(filtre(wordle, *pattern_to_regex(pattern_maker(word_input, pattern_interpreter(patternResult)))))
        try:
            best_word = max([(x, word_test(x, wordle)) for x in wordle], key=lambda x: x[1])[0]
            print("Le meilleur mot est: ", best_word)
            word_input = input("Quelle mot aviez vous saisi:").lower()
        except ValueError:
            print("Impossible de diviner le mot désolé")
            break
