def reverseOnlyLetters(text):

    if not isinstance(text, str):
        raise TypeError(f'Passed variable should be text, got {type(text)}')


    new_words = []
    for word in text.split():
        letters = []
        nonletters = []
        for index, character in enumerate(word):
            if not character.isalpha():
                nonletters.append((index, character))
                continue
            letters.append(character)
        letters.reverse()
        for item in nonletters:
            letters.insert(*item)
        new_words.append(''.join(letters))
    return ' '.join(new_words)

if __name__ == '__main__':
    cases = [
        ("abcd efgh", "dcba hgfe"),
        ("a1bcd efg!h", "d1cba hgf!e"),
        ("", ""),
    ]
    for text, new_words in cases:
        assert reverseOnlyLetters(text) == new_words
