#=
main:
- Julia version: 
- Author: machk
- Date: 2022-07-03
=#
using Match
using Base.Iterators
using BenchmarkTools

@enum Possibility begin
    vert
    jaune
    gris
end
PATH = Dict(1 => "dico/short_french.txt", 2 => "dico/long_french.txt", 3 => "dico/english.txt")

# Total des combinaisons que peuvent donner Wordle 3**5 possibilités
p = product(repeated(("gris", "vert", "jaune"), 5)...) |> Ref |> flatten |> collect


function word_test(word::String, dico_of_word::Array)::Number
    """
    Calcule l'entropie' d'un mot donné d'apparaitre pour toute les 243 possibilités que peuvent donner Wordle
    :param word: le mot qu'on veut évaluer
    :param dico_of_word: la liste contenant tous les mots
    :return: l'entropie du mot
    """

    proba = [length(filtre(dico_of_word, pattern_to_regex(pattern_maker(word, i))...)) / length(dico_of_word)
    for i in p]
    ent = entropie(proba)
    println("$word: $ent")
    return ent
end
function filtre(dico_of_word::Array, pattern::Regex, bad_place::Array, not_include::Array)
    """
    Filtre le dictionnaire dicoOfWord en ne sélectionnant que les mots vérifiant le modèle et contenant les lettres de
    la liste badPlace. De plus il s'assure que les mots sélectionnés ne contiennent aucun character de notInclude
    :param dico_of_word: dictionnaire à filtrer(list)
    :param pattern: modèle correspondant au mot recherché
    :param bad_place: liste de caractère inclut dans les mots voulus qui sont toutefois à la mauvaise place
    :param not_include: liste de caractère non inclut dans les mots
    :return: dictionnaire filtré
    """
    return [i for i in dico_of_word if !isnothing(match(pattern, i)) && all(j ⊆ i for j in bad_place)
    && all(!(j ⊆ i) for j in not_include)]
end

function pattern_to_regex(word_pattern:: Array) :: Tuple
    """
    Convertit le pattern en regex
    :param word_pattern:
    :return:
    """
    pattern = ""
    bad_place = []
    not_include = []
    for i in word_pattern
        if i[2] == '+'
             pattern *= i[1]
        elseif i[2] == '-'
            pattern *= "[^$(i[1])]"
            push!(not_include,  i[1])
        elseif i[2] == '='
            pattern *= "[^$(i[1])]"
            push!(bad_place,  i[1])
        end
    end
    return Regex(pattern), bad_place, not_include
end

function pattern_maker(word::String, pattern::Tuple) :: Array
    """
    Construit un pattern en fonction des différentes couleurs données. Ce pattern va permettre
    la conversion en regex
    :param word: mots donnés
    :param pattern: sequences de couleur dans un tuple
    :return: liste contenant chaque lettre et son signe dans la phrase
    """
    word_pattern = []

    for (i, j) in zip(word, pattern)

        @match string(j) begin
            # Lettre absente
            "gris" => push!(word_pattern, "$i-")
            # Lettre présente à la mauvaise place
            "jaune" => push!(word_pattern, "$i=")
            # Lettre présente et à la bonne place
            "vert" => push!(word_pattern, "$i+")
        end

    end
    return word_pattern
end

function pattern_interpreter(pattern:: String) :: Tuple
    """
    Convertir le model obtenue par l'utilisateur en un modèle comprehensible par le programme
    :param pattern: modèle entré par l'utilisateur
    :return: Tuple contenant des valeurs de l'énumération Possibility
    """

    interpretation = []
    for i in pattern
        @match i begin
            'V' => push!(interpretation , vert::Possibility)
            'G' => push!(interpretation , gris::Possibility)
            'J' => push!(interpretation , jaune::Possibility)
        end
    end

    return tuple(interpretation...)
end

function entropie(probability:: Array) :: Number
    """
    Calcule l'entropie de la liste des probablité donné
    :param probability: liste des probabilités
    :return: liste des probabilités
    """
    x = [log(2, 1 / k) for k in probability if k != 0]
    return sum(i * j for (i, j) in zip(x, probability))
end
function find_best_word(dico::Array{String})
    """
    Trouve le mot le plus probable dans le dictionnaire
    :param dico: dictionnaire de mots
    """
    println("====Recherche du meilleur mot===")
    return argmax(x->x[2], [(x, word_test(x, wordle)) for x in dico])[1]
end
function menu() :: String
    println("====Bienvenue sur le LOPWorld Solver====")
    println("Quel dictionnaire de mot vouliez vous utiliser")
    println("1 - Dictionnaire francais court (22740 mots)")
    println("2 - Dictionnaire francais long (208914 mots)")
    println("3 - Dictionnaire anglais (84100 mots)")
    print("Veuillez saisir votre choix: ")
    return PATH[parse(Int64, readline())]
end
if abspath(PROGRAM_FILE) == @__FILE__
   wordle = open("dico/short_french.txt") do dico
     [lowercase(replace(x, "\n" => "")) for x in eachline(dico) if !isnothing(match(r"^[a-z]{5}$", x))]
   end
    @btime best_word = "jeton"
    println("Le meilleur mot est: ", "jeton")
    print("Quel mot aviez-vous saisi: ")
    word_input = lowercase(readline())
    while true
        global wordle
        global word_input
        print("Quelle est le model que vous aviez obtenue: (V:🟩, G:⬛, J:🟨) ")
        patternResult = uppercase(readline())
        if patternResult == "STOP"
            println("Merci d'avoir joué")
            break
        end
        if patternResult == "VVVVV"
            print("Félicitions et merci d'avoir joué")
            break
        end

        wordle = filtre(wordle, pattern_to_regex(pattern_maker(word_input, pattern_interpreter(patternResult)))...)
        try
            best_word = argmax(x->x[2], [(x, word_test(x, wordle)) for x in wordle])[1]

            println("Le meilleur mot est: ", best_word)
            print("Quel mot aviez-vous saisi:")
            word_input = lowercase(readline())
        catch e
            print("Impossible de diviner le mot désolé: ", e)
            break
        end
    end
end
