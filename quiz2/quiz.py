# NO IMPORTS ALLOWED!

##################################################
### Problem 1: efficiency
##################################################

def unique(input_list):
     output = []
     seen = set()
     for item in input_list:
         if item not in seen:
             seen.add(item)
             output.append(item)
     return output

##################################################
### Problem 2: phone words
##################################################

allwords = set(open('words2.txt').read().splitlines())

def is_word(i):
    return i.lower() in allwords

key_letters = {
    '2': 'ABC',
    '3': 'DEF',
    '4': 'GHI',
    '5': 'JKL',
    '6': 'MNO',
    '7': 'PQRS',
    '8': 'TUV',
    '9': 'WXYZ',
}


def phone_words(digits):
    digits = str(digits)
    def helper(digits, word):
        words = []
        if is_word(word):
            words.append(word)

        if len(digits) == 0:
            return words

        if digits[0] == "0" or digits[0] == "1":
            return words

        for letter in key_letters[digits[0]]:
            words = words + helper(digits[1:],word + letter)
        return words

    output = []
    for n in range(len(digits)):
        output = output + helper(digits[n:], "")
    return set(output)


##################################################
### Problem 3: radix trie
##################################################

from trie import Trie, RadixTrie

def make_word_trie(words):
    t = Trie()
    for word, val in words:
        t[word] = val
    return t

def dictify(t):
    """
    For debugging purposes.  Given a trie (or radix trie), return a dictionary
    representation of that structure, including the value and children
    associated with each node.
    """
    out = {'value': t.value, 'children': {}}
    for ch, child in t.children.items():
        out['children'][ch] = dictify(child)
    return out


def compress_trie(trie):
    def helper(trie, rtrie):
        rtrie.value = None

        if trie.value != None:
            rtrie.value = trie.value

        for key in trie.children:
            if len(trie.children[key].children) > 1:
                rtrie.children[key] = RadixTrie()
                rtrie.children[key] = helper(trie.children[key],rtrie.children[key])
            else:
                node = trie.children[key]
                new_key = key
                while len(node.children) == 1 and node.value == None:
                    for key in node.children:
                        new_key = new_key + key
                    node = node.children[new_key[-1]]
                rtrie.children[new_key] = RadixTrie()
                rtrie.children[new_key] = helper(node,rtrie.children[new_key])
        return rtrie
    return helper(trie,RadixTrie())
