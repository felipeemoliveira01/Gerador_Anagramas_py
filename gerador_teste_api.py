import requests
import xml.etree.ElementTree as ET
from itertools import permutations


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


def generate_anagrams(word):
    perms = [''.join(p) for p in permutations(word)]
    return set(perms)


def filter_valid_words(anagrams):
    valid_words = {}
    for word in anagrams:
        meaning = check_word_meaning(word)
        if meaning != "Erro na resposta da API ou palavra não encontrada" and meaning != "Significado não encontrado":
            valid_words[word] = meaning
    return valid_words


def main():
    input_word = ("puya")  # Palavra para gerar anagramas
    anagrams = generate_anagrams(input_word)
    valid_words = filter_valid_words(anagrams)

    print(f"Anagramas válidos de '{input_word}':")
    for word, meaning in valid_words.items():
        print(f"{word}: {meaning}")


if __name__ == "__main__":
    main()