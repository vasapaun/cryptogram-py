import requests
import argostranslate.package as ap
import argostranslate.translate as at
import unidecode as uc


def print_encrypted_quote(translated_quote_ascii, translated_quote_unicode, solved_set, translated_quote_dict):

    encrypted_quote = ""

    for ascii, unicode in zip(translated_quote_ascii, translated_quote_unicode):
        if not unicode.isalpha():
            encrypted_quote += unicode
            continue
        if unicode in solved_set:
            if encrypted_quote[-1] == "|":
                encrypted_quote = encrypted_quote[:-1] + unicode
            else:
                encrypted_quote += unicode
        else:
            for key, value in translated_quote_dict.items():
                if value == unicode.lower():
                    encrypted_quote += str(key) + '|'

    print(encrypted_quote)


# Fetch quote from http://api.quotable.io
quote_request = 'http://api.quotable.io/random'
print("Fetching a quote from Quoatable...")
r = requests.get(quote_request)
quote_in_english = r.json()['content']
author = r.json()['author']
print("Quote: " + quote_in_english + '\n' + "Author: " + author + '\n')

# TODO: uncomment for French quotes
# r = requests.get('https://fraze.it/api/famous/a/fr/1/no/ed03a4fa-a92d-404e-a16e-9e2a19c9526e')
# print(r.json())


from_code = "en"
to_code = "fr"

# Download and install Argos Translate package
print("Downloading translation packages...")
ap.update_package_index()
available_packages = ap.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
ap.install_from_path(package_to_install.download())

# Translate quote
print("Translating quote...")
translated_quote_unicode = at.translate(quote_in_english, from_code, to_code)
translated_quote_ascii = uc.unidecode(translated_quote_unicode).lower()
print("Translation: " + translated_quote_unicode)

# Encrypt quote
translated_quote_set = set()
for char in translated_quote_unicode:
    if char.isalpha():
        translated_quote_set.add(char.lower())

translated_quote_dict = dict(enumerate(list(translated_quote_set), start=1))
print("Dictionary: " + str(translated_quote_dict))

solved_set = set()
unsolved_set = translated_quote_set
solved_set.add(list(translated_quote_dict.values())[0])
solved_set.add(list(translated_quote_dict.values())[1])
solved_set.add(list(translated_quote_dict.values())[2])
unsolved_set.remove(list(translated_quote_dict.values())[0])
unsolved_set.remove(list(translated_quote_dict.values())[1])
unsolved_set.remove(list(translated_quote_dict.values())[2])

print("Unsolved set: " + str(unsolved_set))
print("Solved set: " + str(solved_set))

print_encrypted_quote(translated_quote_ascii, translated_quote_unicode, solved_set, translated_quote_dict)

while len(unsolved_set) != 0:
    print("Unsolved set: " + str(unsolved_set))
    print("Solved set: " + str(solved_set))
    # TODO: Handle input.
    cmd = input().split(' ')
    if cmd[0] == "solve":
        # Solve logic
        pass

    else:
        if cmd[0].isnumeric() and cmd[1].isalpha():
            print("numeric")
            if int(cmd[0]) in translated_quote_dict.keys() and cmd[1] in unsolved_set:
                print("2")
                if translated_quote_dict[int(cmd[0])] == cmd[1]:
                    # Correct guess
                    print("Correct! The new encrypted quote is:")
                    unsolved_set.remove(cmd[1])
                    solved_set.add(cmd[1])
                else:
                    print("Wrong! The encrypted quote is still:")

    print_encrypted_quote(translated_quote_ascii, translated_quote_unicode, solved_set, translated_quote_dict)

print("Good game! The full quote is: " + translated_quote_unicode + " Translated, this is: " + quote_in_english)





















