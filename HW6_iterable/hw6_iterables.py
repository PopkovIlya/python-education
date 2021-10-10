"""Home work 6 - iterables"""

import re


class MultipleSentencesError(Exception):
    """Class for error implementation MultipleSentencesError"""
    def __init__(self, text="There should only be one sentence"):
        """
        Parameters
        ----------
        text : str, optional
            The error message (default is 'There should only
            be one sentence').
        """
        self.txt = text
        super().__init__(self.txt)


class Sentence:
    """A class that contains one sentence and supports iteration over its words"""

    def __init__(self, text: str):
        """
        Parameters
        -----------
            text : str
                The text should be one complete sentence."""
        if self.check_type(text) and self.check_end(text) and \
                self.check_multiple_sentences(text):
            self.string = text

    @staticmethod
    def check_type(check_string: str):
        """Checks the type of incoming data.

        Parameters
        ----------
        check_string : str
            Input data, expected string.

        Raises
        ------
        TypeError
            If the input data is not a string.
        """

        if isinstance(check_string, str):
            return True
        raise TypeError

    @staticmethod
    def check_end(check_string: str):
        """Checks if a sentence is complete (has a an end-of-sentence
        sign at the end of the sentence).

         Parameters
         ----------
         check_string : str
             Input data, expected string.

         Raises
         ------
         ValueError
             If the input data does not have an end-of-sentence
             sign at the end of the sentence.
         """

        if check_string[len(check_string)-1] in "!.?":
            return True
        raise ValueError

    @staticmethod
    def __second_block(check_string, i):
        """Helper for the "Multi Check" function,
        introduced to improve readability."""
        if check_string[i + 2] in ".!?":
            if (i + 2) != len(check_string) - 1:
                raise MultipleSentencesError
            return True
        raise MultipleSentencesError

    @staticmethod
    def check_multiple_sentences(check_string: str):
        """Checks if there is one sentence per line.

         Parameters
         ----------
         check_string : str
             Input data, expected string.

         Raises
         ------
         MultipleSentencesError
             If the input string contains more than one sentence.
         """
        len_string = len(check_string)
        for i in range(len_string):
            if check_string[i] in ".!?" and i < len_string - 1:
                if check_string[i+1] in ".!?":
                    if (i + 1) < len_string - 1:
                        return Sentence.__second_block(check_string, i)
                    if (i + 1) == len_string - 1:
                        return True
                raise MultipleSentencesError
            if check_string[i] in ".!?" and i == len_string - 1:
                return True
        return False

        # for i in enumerate(check_string):
        #     if check_string[i[0]] in ".!?" and i[0] < len(check_string) - 1:






    @property
    def words(self):
        """Returns a list of words in the sentence that contains the class."""
        return re.findall(r"\w+", self.string)

    @property
    def other_chars(self):
        """Returns a list of non-word characters contained in a class clause."""

        return re.findall(r"\W", self.string)

    def _words(self):
        """Returns a lazy iterator (generator) that can iterate
         over the word list of the sentence contained in the class."""

        for word in self.words:
            yield word

    def __len__(self):
        return len(self.words)

    def __getitem__(self, item):
        return self.words[item]

    def __iter__(self):
        return SentenceIterator(self.words)

    def __repr__(self):
        return f"{self.__class__.__name__}(words={len(self.words)}," \
               f" other_chars={len(self.other_chars)})"

    def __next__(self):
        return SentenceIterator(self.words)


class SentenceIterator:
    """An iterator class of the 'Sentence' class.

    Parameters
    ----------
    list_words : list
        List of words contained in the 'Sentence' class."""

    def __init__(self, list_words):
        """Parameters
    ----------
    list_words : list
        List of words contained in the 'Sentence' class."""

        self.words = list_words
        self.len = len(list_words)
        self.index_iter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index_iter == self.len:
            raise StopIteration
        res = self.words[self.index_iter]
        self.index_iter += 1
        return res


if __name__ == "__main__":

    # print("1 - принимает только строки, иначе рейзит ошибку TypeError")
    # STRING = 123
    # sentence = Sentence(STRING)


    # print("2 - принимает только законченные предложения (. ... ! ?), иначе - ValueError")
    # string = "Hello world, we here"
    # sentence = Sentence(string)


    print("3 - - принимает только одно предложение, "
          "иначе - пользовательский MultipleSentencesError")
    S = "Hello world! We here..."
    sentence = Sentence(S)


    # print("4 - пример работы: __repr__() >>> <Sentence(words=13, other_chars=7)>")
    # string = "Hello world, we here!.."
    # sentence = Sentence(string)
    # print(sentence)


    # print("5 - метод Sentence()._words должен возвращать ленивый итератор. "
    #       "Cмысл тут в том, что мы не хотим хранить в объекте список слов, "
    #       "потому что предложения могут быть очень большими и занимать много памяти, "
    #       "о этому мы будем генерировать его по необходимости и отдавать пользователю "
    #       "пример работы: Sentence('Hello word!')._words() >>> "
    #       "<generator object Sentence._words at 0x7f4e8cb065f0> "
    #       "next(Sentence('Hello word!')._words()) >>> 'Hello'\n")

    # string = "Hello world, we here!.."
    # sentence = Sentence(string)
    # print(sentence._words())
    # print(next(sentence._words()))
    # print(next(sentence._words()))
    #
    # print("\nAs I understand it, it doesn't work without iter()\n")
    # i_sen = iter(sentence._words())
    # print(next(i_sen))
    # print(next(i_sen))
    # print(next(i_sen))
    # print(next(i_sen))
    # print(next(i_sen))


    # print("6 - имеет свойство Sentence().words, "
    #       "которое возвращает список всех слов в предложении "
    #       "(*напоминаю, что мы не хотим хранить все эти слова в нашем объекте)")
    #
    # string = "Hello world, we here!.."
    # sentence = Sentence(string)
    # print(sentence.words)


    # print("7 - имеет свойство Sentence().other_chars, которое возвращает
    # список всех не слов в предложении")
    # string = "Hello world, we here!.."
    # sentence = Sentence(string)
    # print(sentence.other_chars)


    # print("8 - умеет отдавать слово по индексу пример работы:
    # Sentence('Hello world!')[0] >>> 'Hello'")
    # string = "Hello world, we here!.."
    # sentence = Sentence(string)
    # print(sentence[0])
    # print(sentence[2])


    # print("9 - умеет отдавать срез по словам пример работы:
    # Sentence('Hello world!')[:] >>> 'Hello world'")
    # string = "Hello world, we here!.."
    # sentence = Sentence(string)
    # print(sentence[:])
    # print(sentence[1:3])


    # print("10 - может быть использован в цикле for "
    #       "пример работы:"
    #       "for word in Sentence('Hello world!'):"
    #       "    print(word)"
    #       "    >>> 'Hello'"
    #       "    >>> 'world'")
    # for word in Sentence("Hello world, we here!.."):
    #     print(word)


    # print("11 - при передаче в качестве аргумента в функцию iter()
    # возвращает SentenceIterator")
    # string = "Hello world, we here!.."
    # sentence = Sentence(string)
    # print(iter(sentence))


    # print("12 - при передаче в качестве аргумента в функцию next() "
    #       "по очереди возвращает слова из порождающего его объекта Sentence")
    # string = "Hello world, we here!.."
    # sentence = iter(Sentence(string))
    #
    # print(next(sentence))
    # print(next(sentence))
    # print(next(sentence))
    # print(next(sentence))
    # print(next(sentence))
