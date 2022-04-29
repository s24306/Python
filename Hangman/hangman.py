import random
import string

word_list = ['python', 'java', 'kotlin', 'javascript']
the_word = random.choice(word_list)
print('H A N G M A N')
secret_word = '-' * len(the_word)
letters = set(the_word)
attempts = 8
used_letters = []
alphabet = list(string.ascii_lowercase)
while attempts > 0 and len(letters) > 0:
    print()
    print(secret_word)
    answer = input('Input a letter:').strip()
    if len(answer) > 1:
        print("You should input a single letter")
        continue
    elif answer not in alphabet:
        print("It is not an ASCII lowercase letter")
        continue
    elif answer in used_letters:
        print("You already typed this letter")
        continue
    elif answer not in letters and answer in the_word:
        attempts -= 1
        print('No improvements')
        used_letters.append(answer)
    elif answer not in letters:
        attempts -= 1
        print('No such letter in the word')
        used_letters.append(answer)
    else:
        letters.discard(answer)
        secret_word = ''
        for i in the_word:
            if i in letters:
                secret_word += '-'
            else:
                secret_word += i
        used_letters.append(answer)
if len(letters) == 0:
    print(the_word)
    print('''You guessed the word!
    You survived!''')
else:
    print('You are hanged!')
