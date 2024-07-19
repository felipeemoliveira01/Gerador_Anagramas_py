import itertools
from dicio import Dicio
import time
import requests
import xml.etree.ElementTree as ET

# Inicializa o objeto Dicio para verificar palavras
dicio = Dicio()


# Função para verificar se uma palavra é válida usando a biblioteca Dicio
def is_valid_word(word):
    try:
        response = dicio.search(word)
        return response is not None
    except Exception as e:
        print(f"Erro ao verificar a palavra '{word}': {e}")
        return False


# Função para checar o significado de uma palavra usando a API do Dicionário Aberto
def check_word_meaning(word):
    url = f"https://api.dicionario-aberto.net/word/{word}"
    response = requests.get(url)

    if response.status_code == 200 and response.text.strip():
        try:
            data = response.json()
            if data:
                root = ET.fromstring(data[0].get("xml", ""))
                definitions = []

                for sense in root.findall(".//sense"):
                    definition = sense.find("def")
                    if definition is not None:
                        definitions.append(definition.text.strip())

                return " | ".join(definitions) if definitions else "Significado não encontrado"
            else:
                return "Significado não encontrado"
        except requests.exceptions.JSONDecodeError:
            return "Erro ao decodificar a resposta JSON"
    else:
        return "Erro na resposta da API ou palavra não encontrada"


# Função para gerar anagramas de uma palavra
def generate_anagrams(word):
    permutations = itertools.permutations(word)
    anagrams = [''.join(perm) for perm in permutations]
    return set(anagrams)


# Função para filtrar anagramas válidos e obter seus significados
def filter_valid_words(anagrams):
    valid_words = {}
    for word in anagrams:
        meaning = check_word_meaning(word)
        if meaning != "Erro na resposta da API ou palavra não encontrada" and meaning != "Significado não encontrado":
            valid_words[word] = meaning
    return valid_words


# Função para imprimir os anagramas, tanto os válidos quanto os inválidos
def print_anagrams(all_anagrams):
    max_length = max(len(anagrams) for anagrams in all_anagrams)

    for i in range(max_length):
        combined_anagram = []
        for anagrams in all_anagrams:
            anagram_list = sorted(list(anagrams))
            if i < len(anagram_list):
                combined_anagram.append(anagram_list[i])
            else:
                combined_anagram.append(anagram_list[0])
        if all(is_valid_word(word) for word in combined_anagram):
            print(f"{i + 1}. {' '.join(combined_anagram)}")
        else:
            print(f"Anagrama inválido: {' '.join(combined_anagram)}")


# Função principal para processar a entrada do usuário
def process_input(input_text):
    words = input_text.split()
    all_anagrams = []

    for word in words:
        anagrams = generate_anagrams(word)
        anagrams.discard(word)
        all_anagrams.append(anagrams)

    # Primeiro, imprime os anagramas válidos com seus significados
    for anagrams in all_anagrams:
        valid_words = filter_valid_words(anagrams)
        if valid_words:
            print("Anagramas válidos e seus significados:")
            for word, meaning in valid_words.items():
                print(f"{word}: {meaning}")
        else:
            print("Nenhum anagrama válido encontrado.")

    # Em seguida, imprime todos os anagramas
    print("Todos os anagramas:")
    print_anagrams(all_anagrams)


# Loop principal do programa
def main():
    while True:
        input_text = input("Digite uma palavra ou frase (ou '000' para terminar): ")

        if input_text == '000':
            print("Encerrando o programa...")
            break

        process_input(input_text)
        print()

    print("Processamento concluído em", time.strftime("%H:%M:%S"))


if __name__ == "__main__":
    main()