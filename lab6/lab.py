# NO ADDITIONAL IMPORTS!
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self, type_=None):
        self.value = None
        self.children = {}
        self.type = None

    def itertrie(self,key):
        """ Helper function: returns last node of key, if it exists.
        """

        node = self
        ind = 0
        while ind < len(key): #Looping through characters in key to find end node
            if key[ind:ind+1] in node.children:
                node = node.children[key[ind:ind+1]]
                ind += 1
            else:
                raise KeyError
        return node

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.
        """
        if self.type != None and not isinstance(key,self.type):
            raise TypeError

        if len(key) > 0:
            if self.children == {}:
                self.type = type(key)
            node = self
            ind = 0
            while ind < len(key): #While still not at the end of key
                if key[ind:ind+1] not in node.children: #If current node does not already exist, create new node
                    node.children[key[ind:ind+1]] = Trie()
                node = node.children[key[ind:ind+1]] #Current node set to new child node
                ind += 1 #Key shortened
            node.value = value #At the end of the key, the current node's value is set to value


    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.
        """
        if self.type == None: #Empty Trie?
            raise KeyError

        if not isinstance(key,self.type): #Wrong key type
            raise TypeError

        node = self.itertrie(key)

        if node.value == None:
            raise KeyError

        return node.value #Returning value of final node

    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists.
        """
        self.itertrie(key).value = None

    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        """
        try:
            node = self.itertrie(key)
            if node.value != None:
                return True
            else:
                return False
        except:
            return False

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        """
        def generate_pairs(trie, key):
            if trie.value != None:
                yield (key, trie.value)
            for temp_key in trie.children:
                yield from generate_pairs(trie.children[temp_key], key + temp_key)
        if self.type == type(""):
            return generate_pairs(self,"")
        return generate_pairs(self,tuple())

t = Trie()
t['bat'] = 2
t['bar'] = True
t['bark'] = False

# #Set Item Tests
# print(t.children['b'].children['a'].children['r'].value)

# #Get Item Tests
# print(t['bat'])
# print(t['bark'])
#print(t['ba'])
#print(t[1])

# #Delete Tests
# print(t['bat'])
# del t['bat']
# print(t['bat'])

# #Contains tests
# print("ba" in t)
# print("bar" in t)
# print("barking" in t)

# #Iter tests
# print(list(t))
# for key, val in t:
#     print(key)


def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """
    sentences = tokenize_sentences(text)
    t = Trie()
    for sentence in sentences:
        words = sentence.split(" ")
        for word in words:
            if word in t:
                t[word] += 1
            else:
                t[word] = 1
    return t

# t = make_word_trie("bat bat bark bar")
# print(list(t))

def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    sentences = tokenize_sentences(text)
    t = Trie()
    for sentence in sentences:
        sentence = tuple(sentence.split(" "))
        if sentence in t:
            t[sentence] += 1
        else:
            t[sentence] = 1
    return t


def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring words that start with
    prefix.  Include only the top max_count elements if max_count is specified,
    otherwise return all.
    """
    words = []
    for key,value in trie:
        if key[0:len(prefix)] == prefix: #Checking if each key has prefix as its prefix
            words.append((key,value))

    if max_count == None:
        words = [key for key,value in words] #If no limit on words, return all
        return(list(set(words)))

    finalwords = set()
    auto = sorted(words,key=lambda tup: tup[1],reverse=True) #Sorting words by value (=frequency)
    autoind = 0
    while autoind < len(auto) and len(finalwords) < max_count:
        finalwords.add(auto[autoind][0])
        autoind += 1

    return list(finalwords)

def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.
    """
    words = autocomplete(trie,prefix,max_count)
    if len(words) == max_count: #Checking if regular autocomplete satisfies max_count
        return words

    new_words = []
    for index in range(len(prefix)+1):
        for letter in "abcdefghijklmnopqrstuvwxyz": #Trying to add/replace letters
            new_word_add = letter + prefix[index:]
            if index != 0:
                new_word_add = prefix[0:index] + new_word_add
            if new_word_add in trie:
                new_words.append((new_word_add,trie[new_word_add]))

            if index < len(prefix):
                new_word_repl = prefix[0:index] + letter
                if index != len(prefix) -1 :
                    new_word_repl += prefix[index+1:]
            if new_word_repl in trie:
                new_words.append((new_word_repl,trie[new_word_repl]))

        if index < len(prefix): #Trying to delete letters
            new_word_del = prefix[0:index]
            if index != len(prefix) -1 :
                new_word_del += prefix[index+1:]
            if new_word_del in trie:
                new_words.append((new_word_del,trie[new_word_del]))

            if index > 0: #Trying to swap letters
                new_word_swap = prefix[0:index-1] + prefix[index] + prefix[index-1]
                if index != len(prefix) -1 :
                    new_word_swap += prefix[index+1:]
                if new_word_swap in trie:
                    new_words.append((new_word_swap,trie[new_word_swap]))

    if max_count == None:
        new_words = [key for key,value in new_words]
        return list(set(words+new_words))

    auto = sorted(new_words,key=lambda tup: tup[1],reverse=True) #Sorting words by value (=frequency)
    allwords = set(words)

    autoind = 0 #Keeping track of location in auto list
    while autoind < len(auto) and len(allwords) < max_count:
        allwords.add(auto[autoind][0])
        autoind += 1
    return list(allwords)

def strip_stars(word):
    while len(word) > 0 and word[0]=="*":
        word = word[1:]
    while len(word) > 0 and word[-1]=="*":
        word = word[0:-1]
    return word

def word_filter(trie, pattern, word=""):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    if len(pattern)==0 and trie.value != None:
        return [(word,trie.value)]

    if len(pattern) == 0:
        return []

    ques_mark = 0
    ques_mark_end = 0
    stars = 0
    last_star = 0
    for i in range(len(pattern)):
        if pattern[i] == "?":
            ques_mark += 1
            ques_mark_end += 1
        else:
            ques_mark_end = 0
        if pattern[i] == "*":
            stars += 1
            last_star = i

    all_ques = False
    if len(strip_stars(pattern)) > 0:
        all_ques = True
        for letter in strip_stars(pattern):
            if letter != "?":
                all_ques = False

    matches = []

    if (stars == len(pattern) or (pattern[0] == "*" and ques_mark_end > 0 and stars+ques_mark_end==len(pattern) and len(word) > ques_mark)) and trie.value != None:
        matches += [(word,trie.value)]

    elif all_ques and len(word) >= ques_mark and trie.value != None:
        matches += [(word,trie.value)]

    elif (pattern[-1] == "*" and pattern[0] == "*") and strip_stars(pattern) in word and trie.value != None:
        matches += [(word,trie.value)]

    if pattern[0] in trie.children: #Checking if char in pattern matches char in word
        matches = matches + word_filter(trie.children[pattern[0]],pattern[1:],word + pattern[0])
        return matches

    if pattern[0] == "?":
        for child in trie.children:
            matches = matches + word_filter(trie.children[child],pattern[1:],word + child)
        return matches

    if pattern[0] == "*":
        if len(pattern) > last_star + 1 and pattern[last_star + 1] in trie.children:
            # print(trie.children)
            # print(word)
            matches = matches + word_filter(trie.children[pattern[last_star + 1]],pattern[(last_star + 2):],word+pattern[last_star + 1])
        for child in trie.children:
            matches = matches + word_filter(trie.children[child],pattern,word + child)
        return matches

    else:
        return []

#
t = make_word_trie("man mat mattress map me met a man a a a map man met")
print(word_filter(t,"???"))

# you can include test cases of your own in the block below.
if __name__ == '__main__':
    # pass
    books = ["alice_in_wonderland","a_tale_of_two_cities","dracula","metamorphosis","pride_and_prejudice"]
    texts = {}
    for book in books:
        with open(book + ".txt", encoding="utf-8") as f:
            texts[book] = f.read()

    #Alice in Wonderland: Six most common phrases
    alice_phrase = list(make_phrase_trie(texts["alice_in_wonderland"]))
    alice_sorted = sorted(alice_phrase, key = lambda tup:tup[1],reverse=True)
    print([key for key,value in alice_sorted[:6]])

    #Metamorphosis: Six mot common gre- words
    meta_words = make_word_trie(texts["metamorphosis"])
    print(autocomplete(meta_words,"gre",6))

    #Metamorphosis: c*h filter
    meta_words = make_word_trie(texts["metamorphosis"])
    print(word_filter(meta_words,"c*h"))

    #Tale of Two Cities: r?c*t filter
    tale_words = make_word_trie(texts["a_tale_of_two_cities"])
    print(word_filter(tale_words,"r?c*t"))

    #Alice in Wonderland: 12 'hear' autocorrections
    alice_words = make_word_trie(texts["alice_in_wonderland"])
    print(autocorrect(alice_words,"hear",12))

    #Pride and Prejudice: All 'hear' autocorrections
    pride_words = make_word_trie(texts["pride_and_prejudice"])
    print(autocorrect(pride_words,"hear"))

    #Dracula: Unique Words // Total Words
    dracula_words = make_word_trie(texts["dracula"])
    print(len(list(dracula_words)))
    wordnum = 0
    for key,value in dracula_words:
        wordnum += value
    print(wordnum)

    #Alice in Wonderland: Unique Sentences // Total Sentences
    alice_phrases = make_phrase_trie(texts["alice_in_wonderland"])
    print(len(list(alice_phrases)))
    phrasenum = 0
    for key,value in alice_phrases:
        phrasenum += value
    print(phrasenum)
