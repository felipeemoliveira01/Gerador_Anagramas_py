import itertools
from dicio import Dicio
import time

dicio = Dicio()
def is_valid_word(word):
    try:
        response = dicio.search(word)
        return response is not None
    except Exception as e:
        print(f"Erro ao verificar palavra '{word}': {e}")
        return False

def generate_anagrams(word):
    permutations = itertools.permutations(word)
    anagrams = [''.join(perm) for perm in permutations]
    return set(anagrams)

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

def process_input(input_text):
    words = input_text.split()
    all_anagrams = []

    for word in words:
        anagrams = generate_anagrams(word)
        anagrams.discard(word)
        all_anagrams.append(anagrams)

    print_anagrams(all_anagrams)


while True:
    input_text = input("Digite uma palavra ou frase (ou '000' para terminar): ")

    if input_text == '000':
        print("Encerrando o programa...")
        break

    process_input(input_text)
    print()

print("Processamento concluído em", time.strftime("%H:%M:%S"))