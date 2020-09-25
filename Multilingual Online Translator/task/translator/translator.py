import requests
from bs4 import BeautifulSoup
from sys import argv

languages_dict = {
    1: "Arabic",
    2: "German",
    3: "English",
    4: "Spanish",
    5: "French",
    6: "Hebrew",
    7: "Japanese",
    8: "Dutch",
    9: "Polish",
    10: "Portuguese",
    11: "Romanian",
    12: "Russian",
    13: "Turkish",
}


def get_translation(lang_input, lang_output, word):
    url = f"https://context.reverso.net/translation/{lang_input.lower()}-{lang_output.lower()}/{word}"
    try:
        my_request = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    except requests.exceptions.ConnectionError:
        print("Something wrong with your internet connection")
    if not my_request:
        print(f"Sorry, unable to find {word.lower()}")
        exit()
    soup_object = BeautifulSoup(my_request.text, "lxml")
    sentence_examples = []
    for sentence in soup_object.find(id="examples-content").select("span"):
        sentence_examples.append(sentence.text.strip())
    word_examples = []
    for word_translated in soup_object.find(id="translations-content").select("a"):
        word_examples.append(word_translated.text.strip())
    with open("hello.txt", "a", encoding="utf-8") as f:
        print(f"{lang_output} Translations:")
        f.write(f"{lang_output} Translations:\n")
        for word in word_examples[:5]:
            print(word)
            f.write(word + "\n")
        print(f"\n{lang_output} Examples:")
        f.write(f"\n{lang_output} Examples:\n")
        for i in range(0, 15, 3):
            print(sentence_examples[i] + ":")
            f.write(sentence_examples[i] + ":\n")
            print(sentence_examples[i + 2] + "\n")
            f.write(sentence_examples[i + 2] + "\n\n")


def main():
    input_lang, output_lang, word = map(str.capitalize, argv[1:])
    if input_lang not in languages_dict.values():
        print(f"Sorry, the program doesn't support {input_lang}")
        exit()
    elif output_lang not in languages_dict.values() and output_lang != "All":
        print(f"Sorry, the program doesn't support {output_lang}")
        exit()
    if output_lang != "All":
        get_translation(input_lang, output_lang, word)
    else:
        for language in languages_dict.values():
            if language != input_lang:
                get_translation(input_lang, language, word)


if __name__ == "__main__":
    main()
