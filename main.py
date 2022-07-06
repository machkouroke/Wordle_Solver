import enum
import re
import math
import shelve
from itertools import product


class Possibility(enum.Enum):
    """
        Enumeration représentant les différentes valeurs que peuvent prendre une case Wordle
    """
    V = 'vert'
    G = 'Gris'
    J = 'Jaune'


class WordleSolver:
    PATH: dict = {1: 'dico/short_french.txt', 2: 'dico/long_french.txt',
                  3: 'dico/english.txt'}
    # Total des combinaisons que peuvent donner Wordle 3**5 possibilités
    p = list(product((Possibility.G, Possibility.V, Possibility.J), repeat=5))

    def __init__(self):
        self.best_word = None
        self.wordle = None
        self.game_solve()

    @staticmethod
    def word_test(word: str, dico_of_word: list) -> float:
        """
        Calcule l'entropie' d'un mot donné d'apparaitre pour toute les 243 possibilités que peuvent donner Wordle
        :param word: le mot qu'on veut évaluer
        :param dico_of_word: la liste contenant tous les mots
        :return: l'entropie du mot
        """
        proba = [len(WordleSolver.filtre(dico_of_word,
                                         *WordleSolver.pattern_to_regex(WordleSolver.pattern_maker(word, i)))) / len(
            dico_of_word) for i in WordleSolver.p]
        ent = WordleSolver.entropie(proba)
        print(f"{word}: ", ent)
        return ent

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def filtre(dico_of_word: list, pattern: str, bad_place: list, not_include: list):
        """
        Filtre le dictionnaire dicoOfWord en ne sélectionnant que les mots vérifiant le modèle et contenant les lettres
        de la liste badPlace. De plus il s'assure que les mots sélectionnés ne contiennent aucun character de notInclude
        :param dico_of_word: dictionnaire à filtrer(list)
        :param pattern: modèle correspondant au mot recherché
        :param bad_place: liste de caractère inclut dans les mots voulus qui sont toutefois à la mauvaise place
        :param not_include: liste de caractère non inclut dans les mots
        :return: dictionnaire filtré
        """
        return [i for i in dico_of_word if re.search(pattern, i) and all(j in i for j in bad_place) and
                all(j not in i for j in not_include)]

    @staticmethod
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

    @staticmethod
    def entropie(probability: list) -> float:
        """
        Calcule l'entropie de la liste des probablité donné
        :param probability: liste des probabilités
        :return: liste des probabilités
        """
        x = [math.log(1 / k, 2) for k in probability if k != 0]
        return sum(i * j for i, j in zip(x, probability))

    def find_best_word(self, dico: list[str]):
        """
        Trouve le mot le plus probable dans le dictionnaire
        :param dico: dictionnaire de mots
        """
        print('====Recherche du meilleur mot====')
        return max(((x, WordleSolver.word_test(x, self.wordle)) for x in dico), key=lambda x: x[1])[0]

    @staticmethod
    def menu() -> str:
        print("====Bienvenue sur le LOPWorld Solver====")
        print('Quel dictionnaire de mot vouliez vous utiliser')
        print('1 - Dictionnaire francais court (22740 mots)')
        print('2 - Dictionnaire francais long (208914 mots)')
        print('3 - Dictionnaire anglais (84100 mots)')
        return WordleSolver.PATH[int(input("Veuillez saisir votre choix:"))]

    def check_config(self):
        with shelve.open('config') as config:
            if 'dico' not in config:
                config['dico'] = WordleSolver.menu()
            with open(str(config['dico'])) as dico:
                self.wordle = [x.lower().replace('\n', '') for x in dico.readlines() if (re.match('^[a-z]{5}$', x))]
            if 'best_word' not in config:
                config['best_word'] = self.find_best_word(self.wordle)
            self.best_word = config['best_word']

    def game_solve(self):
        self.check_config()
        print("Le meilleur mot est: ", self.best_word)
        word_input = input("Quel mot aviez-vous saisi: ").lower()
        while 1:
            pattern_result = input("Quelle est le model que vous aviez obtenue: (V=>🟩, G=>⬛, J=>🟨) ").upper()
            if pattern_result == "stop":
                print("Merci d'avoir joué")
                break
            if pattern_result == "VVVVV":
                print("Félicitions et merci d'avoir joué")
                break

            self.wordle = list(
                WordleSolver.filtre(self.wordle, *WordleSolver.pattern_to_regex(
                    WordleSolver.pattern_maker(word_input, WordleSolver.pattern_interpreter(pattern_result)))))
            try:
                best_word = max(((x, WordleSolver.word_test(x, self.wordle))
                                 for x in self.wordle), key=lambda x: x[1])[0]

                print("Le meilleur mot est: ", best_word)
                word_input = input("Quel mot aviez-vous saisi:").lower()
            except ValueError:
                print("Impossible de diviner le mot désolé")
                break


if __name__ == '__main__':
    WordleSolver()
