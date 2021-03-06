import unittest

from neon_coref_plugin_corefiob import CorefIOBSolver

solver = CorefIOBSolver({"postagger": "neon-postag-plugin-spacy"})


class TestHeuristicParser(unittest.TestCase):
    def test_replace(self):
        self.assertEqual(solver.replace_corefs("The girl said she would take the trash out"),
                         "The girl said The girl would take the trash out")
        self.assertEqual(solver.replace_corefs("I have many friends. They are an important part of my life"),
                         "I have many friends. many friends are an important part of my life")
        self.assertEqual(
            solver.replace_corefs("George von Doomson is the best. His ideas are unique compared to Joe's"),
            "George von Doomson is the best. George von Doomson ideas are unique compared to Joe's")
        self.assertEqual(solver.replace_corefs("Korgoth of Barbaria is here, He is a savage!"),
                         "Korgoth of Barbaria is here, Korgoth of Barbaria is a savage!")
        self.assertEqual(
            solver.replace_corefs("This is Conan the Barbarian of Hyperborea! He is a savage but he is noble"),
            "This is Conan the Barbarian of Hyperborea! Conan the Barbarian of Hyperborea is a savage but Conan the Barbarian of Hyperborea is noble")
        self.assertEqual(solver.replace_corefs("Here is the book now take it"),
                         "Here is the book now take the book")
        self.assertEqual(solver.replace_corefs("Here is the awesome machine now take it"),
                         "Here is the awesome machine now take the awesome machine")
        self.assertEqual(solver.replace_corefs("Turn on the lights and make them blue"),
                         "Turn on the lights and make the lights blue")
        self.assertEqual(solver.replace_corefs("I have many dogs, I love them"),
                         "I have many dogs, I love many dogs")
        self.assertEqual(solver.replace_corefs("My neighbors have a cat. It has a bushy tail"),
                         "My neighbors have a cat. a cat has a bushy tail")
        self.assertEqual(solver.replace_corefs("The coin was too far away for the woman to reach it"),
                         "The coin was too far away for the woman to reach The coin")
        self.assertEqual(solver.replace_corefs("The sign was too far away for the boy to read it"),
                         "The sign was too far away for the boy to read The sign")
        self.assertEqual(solver.replace_corefs("Dog is man's best friend. It is always loyal"),
                         "Dog is man's best friend. Dog is always loyal")
        self.assertEqual(solver.replace_corefs(
            "I voted for Bob because he is clear about his values. His ideas represent a majority of the nation. He is better than Alice"),
            "I voted for Bob because Bob is clear about Bob values. Bob ideas represent a majority of the nation. Bob is better than Alice")
        self.assertEqual(solver.replace_corefs(
            "Jack Glass is one of the top candidates in the elections. His ideas are unique compared to Joe's"),
            "Jack Glass is one of the top candidates in the elections. Jack Glass ideas are unique compared to Joe's")
        self.assertEqual(solver.replace_corefs("Leaders around the world say they stand for peace"),
                         "Leaders around the world say Leaders stand for peace")
        self.assertEqual(solver.replace_corefs("A majority of the nation said they are in favor of democracy"),
                         "A majority of the nation said A majority of the nation are in favor of democracy")
        self.assertEqual(solver.replace_corefs("My neighbours just adopted a puppy. They care for it like a baby"),
                         "My neighbours just adopted a puppy. My neighbours care for a puppy like a baby")
        self.assertEqual(solver.replace_corefs("Members voted for John because they see him as a good leader"),
                         "Members voted for John because Members see John as a good leader")

    def test_gender(self):
        # test implicit gender word list
        # girl/boy/woman...
        self.assertEqual(solver.iob_tag("The girl said she would take the trash out"),
                         [('The', 'DET', 'B-ENTITY-FEMALE'),
                          ('girl', 'NOUN', 'I-ENTITY-FEMALE'),
                          ('said', 'VERB', 'O'),
                          ('she', 'PRON', 'B-COREF-FEMALE'),
                          ('would', 'AUX', 'O'),
                          ('take', 'VERB', 'O'),
                          ('the', 'DET', 'O'),
                          ('trash', 'NOUN', 'O'),
                          ('out', 'ADP', 'O')])
        # plural word
        self.assertEqual(solver.iob_tag("I have many friends. They are an important part of my life"),
                         [('I', 'PRON', 'O'),
                          ('have', 'VERB', 'O'),
                          ('many', 'ADJ', 'B-ENTITY-PLURAL'),
                          ('friends', 'NOUN', 'I-ENTITY-PLURAL'),
                          ('.', 'PUNCT', 'O'),
                          ('They', 'PRON', 'B-COREF-PLURAL'),
                          ('are', 'AUX', 'O'),
                          ('an', 'DET', 'O'),
                          ('important', 'ADJ', 'O'),
                          ('part', 'NOUN', 'O'),
                          ('of', 'ADP', 'O'),
                          ('my', 'PRON', 'O'),
                          ('life', 'NOUN', 'O')])
        # test 3 noun words joined and cast to male (only present coref gender)
        self.assertEqual(solver.iob_tag(
            "George von Doomson is the best. His ideas are unique compared to Joe's"),
            [('George', 'PROPN', 'B-ENTITY-MALE'),
             ('von', 'PROPN', 'I-ENTITY-MALE'),
             ('Doomson', 'PROPN', 'I-ENTITY-MALE'),
             ('is', 'AUX', 'O'),
             ('the', 'DET', 'O'),
             ('best', 'ADJ', 'O'),
             ('.', 'PUNCT', 'O'),
             ('His', 'PRON', 'B-COREF-MALE'),
             ('ideas', 'NOUN', 'O'),
             ('are', 'AUX', 'O'),
             ('unique', 'ADJ', 'O'),
             ('compared', 'VERB', 'O'),
             ('to', 'ADP', 'O'),
             ('Joe', 'PROPN', 'O'),
             ("'s", 'PART', 'O')]
        )

    def test_of(self):
        # NOUN of NOUN
        self.assertEqual(solver.iob_tag("Korgoth of Barbaria is here, He is a savage!"),
                         [('Korgoth', 'PROPN', 'B-ENTITY-MALE'),
                          ('of', 'ADP', 'I-ENTITY-MALE'),
                          ('Barbaria', 'PROPN', 'I-ENTITY-MALE'),
                          ('is', 'AUX', 'O'),
                          ('here', 'ADV', 'O'),
                          (',', 'PUNCT', 'O'),
                          ('He', 'PRON', 'B-COREF-MALE'),
                          ('is', 'AUX', 'O'),
                          ('a', 'DET', 'O'),
                          ('savage', 'NOUN', 'O'),
                          ('!', 'PUNCT', 'O')])

        # NOUN the NOUN of NOUN
        self.assertEqual(solver.iob_tag("This is Conan the Barbarian of Hyperborea! He is a savage but he is noble"),
                         [('This', 'DET', 'O'),
                          ('is', 'AUX', 'O'),
                          ('Conan', 'PROPN', 'B-ENTITY-MALE'),
                          ('the', 'DET', 'I-ENTITY-MALE'),
                          ('Barbarian', 'PROPN', 'I-ENTITY-MALE'),
                          ('of', 'ADP', 'I-ENTITY-MALE'),
                          ('Hyperborea', 'PROPN', 'I-ENTITY-MALE'),
                          ('!', 'PUNCT', 'O'),
                          ('He', 'PRON', 'B-COREF-MALE'),
                          ('is', 'AUX', 'O'),
                          ('a', 'DET', 'O'),
                          ('savage', 'NOUN', 'O'),
                          ('but', 'CCONJ', 'O'),
                          ('he', 'PRON', 'B-COREF-MALE'),
                          ('is', 'VERB', 'O'),
                          ('noble', 'ADJ', 'O')])

    def test_neutral2inanimate(self):
        # "it" makes entities inanimate instead of neutral
        # test 2word - DET included
        self.assertEqual(solver.iob_tag("Here is the book now take it"),
                         [('Here', 'ADV', 'O'),
                          ('is', 'AUX', 'O'),
                          ('the', 'DET', 'B-ENTITY-INANIMATE'),
                          ('book', 'NOUN', 'I-ENTITY-INANIMATE'),
                          ('now', 'ADV', 'O'),
                          ('take', 'VERB', 'O'),
                          ('it', 'PRON', 'B-COREF-INANIMATE')])
        # test 3 words - DET + ADJ included
        self.assertEqual(solver.iob_tag("Here is the awesome machine now take it"),
                         [('Here', 'ADV', 'O'),
                          ('is', 'AUX', 'O'),
                          ('the', 'DET', 'B-ENTITY-INANIMATE'),
                          ('awesome', 'ADJ', 'I-ENTITY-INANIMATE'),
                          ('machine', 'NOUN', 'I-ENTITY-INANIMATE'),
                          ('now', 'ADV', 'O'),
                          ('take', 'VERB', 'O'),
                          ('it', 'PRON', 'B-COREF-INANIMATE')])

    def test_plural2inanimate(self):
        # "them" could also be a neutral or plural coref
        # some words are known to be inanimate, eg, iot stuff (lights) and animals (dog)
        self.assertEqual(solver.iob_tag("Turn on the lights and make them blue"),
                         [('Turn', 'VERB', 'O'),
                          ('on', 'ADP', 'O'),
                          ('the', 'DET', 'B-ENTITY-INANIMATE'),
                          ('lights', 'NOUN', 'I-ENTITY-INANIMATE'),
                          ('and', 'CCONJ', 'O'),
                          ('make', 'VERB', 'O'),
                          ('them', 'PRON', 'B-COREF-INANIMATE'),
                          ('blue', 'ADJ', 'O')])
        self.assertEqual(solver.iob_tag("I have many dogs, I love them"),
                         [('I', 'PRON', 'O'),
                          ('have', 'VERB', 'O'),
                          ('many', 'ADJ', 'B-ENTITY-INANIMATE'),
                          ('dogs', 'NOUN', 'I-ENTITY-INANIMATE'),
                          (',', 'PUNCT', 'O'),
                          ('I', 'PRON', 'O'),
                          ('love', 'VERB', 'O'),
                          ('them', 'PRON', 'B-COREF-INANIMATE')])

    def test_ignore_gender_mismatch(self):
        # coref is inanimate, ignore plural "neighbors"
        self.assertEqual(solver.iob_tag("My neighbors have a cat. It has a bushy tail"),
                         [('My', 'PRON', 'O'),
                          ('neighbors', 'NOUN', 'O'),
                          ('have', 'VERB', 'O'),
                          ('a', 'DET', 'B-ENTITY-INANIMATE'),
                          ('cat', 'NOUN', 'I-ENTITY-INANIMATE'),
                          ('.', 'PUNCT', 'O'),
                          ('It', 'PRON', 'B-COREF-INANIMATE'),
                          ('has', 'VERB', 'O'),
                          ('a', 'DET', 'O'),
                          ('bushy', 'ADJ', 'O'),
                          ('tail', 'NOUN', 'O')])
        # coref is inanimate, ignore female "the woman"
        self.assertEqual(solver.iob_tag("The coin was too far away for the woman to reach it"),
                         [('The', 'DET', 'B-ENTITY-INANIMATE'),
                          ('coin', 'NOUN', 'I-ENTITY-INANIMATE'),
                          ('was', 'AUX', 'O'),
                          ('too', 'ADV', 'O'),
                          ('far', 'ADV', 'O'),
                          ('away', 'ADV', 'O'),
                          ('for', 'ADP', 'O'),
                          ('the', 'DET', 'O'),
                          ('woman', 'NOUN', 'O'),
                          ('to', 'PART', 'O'),
                          ('reach', 'VERB', 'O'),
                          ('it', 'PRON', 'B-COREF-INANIMATE')])
        # coref is inanimate, ignore male "the boy"
        self.assertEqual(solver.iob_tag("The sign was too far away for the boy to read it"),
                         [('The', 'DET', 'B-ENTITY-INANIMATE'),
                          ('sign', 'NOUN', 'I-ENTITY-INANIMATE'),
                          ('was', 'AUX', 'O'),
                          ('too', 'ADV', 'O'),
                          ('far', 'ADV', 'O'),
                          ('away', 'ADV', 'O'),
                          ('for', 'ADP', 'O'),
                          ('the', 'DET', 'O'),
                          ('boy', 'NOUN', 'O'),
                          ('to', 'PART', 'O'),
                          ('read', 'VERB', 'O'),
                          ('it', 'PRON', 'B-COREF-INANIMATE')])
        # coref is inanimate, ignore neutral "best friend" and male "man"
        self.assertEqual(solver.iob_tag("Dog is man's best friend. It is always loyal"),
                         [('Dog', 'PROPN', 'B-ENTITY-INANIMATE'),
                          ('is', 'AUX', 'O'),
                          ('man', 'NOUN', 'O'),
                          ("'s", 'PART', 'O'),
                          ('best', 'ADJ', 'O'),
                          ('friend', 'NOUN', 'O'),
                          ('.', 'PUNCT', 'O'),
                          ('It', 'PRON', 'B-COREF-INANIMATE'),
                          ('is', 'AUX', 'O'),
                          ('always', 'ADV', 'O'),
                          ('loyal', 'ADJ', 'O')])
        # corefs are male, ignore neutral "the nation" and "a majority"
        self.assertEqual(solver.iob_tag(
            "I voted for Bob because he is clear about his values. His ideas represent a majority of the nation. He is better than Alice"),
            [('I', 'PRON', 'O'),
             ('voted', 'VERB', 'O'),
             ('for', 'ADP', 'O'),
             ('Bob', 'PROPN', 'B-ENTITY-MALE'),
             ('because', 'SCONJ', 'O'),
             ('he', 'PRON', 'B-COREF-MALE'),
             ('is', 'VERB', 'O'),
             ('clear', 'ADJ', 'O'),
             ('about', 'ADP', 'O'),
             ('his', 'PRON', 'B-COREF-MALE'),
             ('values', 'NOUN', 'O'),
             ('.', 'PUNCT', 'O'),
             ('His', 'PRON', 'B-COREF-MALE'),
             ('ideas', 'NOUN', 'O'),
             ('represent', 'VERB', 'O'),
             ('a', 'DET', 'O'),
             ('majority', 'NOUN', 'O'),
             ('of', 'ADP', 'O'),
             ('the', 'DET', 'O'),
             ('nation', 'NOUN', 'O'),
             ('.', 'PUNCT', 'O'),
             ('He', 'PRON', 'B-COREF-MALE'),
             ('is', 'AUX', 'O'),
             ('better', 'ADJ', 'O'),
             ('than', 'SCONJ', 'O'),
             ('Alice', 'PROPN', 'O')])
        # coref is male, ignore "top candidates" and "the elections"
        self.assertEqual(solver.iob_tag(
            "Jack Glass is one of the top candidates in the elections. His ideas are unique compared to Joe's"),
            [('Jack', 'PROPN', 'B-ENTITY-MALE'),
             ('Glass', 'PROPN', 'I-ENTITY-MALE'),
             ('is', 'AUX', 'O'),
             ('one', 'NUM', 'O'),
             ('of', 'ADP', 'O'),
             ('the', 'DET', 'O'),
             ('top', 'ADJ', 'O'),
             ('candidates', 'NOUN', 'O'),
             ('in', 'ADP', 'O'),
             ('the', 'DET', 'O'),
             ('elections', 'NOUN', 'O'),
             ('.', 'PUNCT', 'O'),
             ('His', 'PRON', 'B-COREF-MALE'),
             ('ideas', 'NOUN', 'O'),
             ('are', 'AUX', 'O'),
             ('unique', 'ADJ', 'O'),
             ('compared', 'VERB', 'O'),
             ('to', 'ADP', 'O'),
             ('Joe', 'PROPN', 'O'),
             ("'s", 'PART', 'O')])
        # coref is plural, ignore neutral "the world"
        self.assertEqual(solver.iob_tag(
            "Leaders around the world say they stand for peace"),
            [('Leaders', 'NOUN', 'B-ENTITY-PLURAL'),
             ('around', 'ADP', 'O'),
             ('the', 'DET', 'O'),
             ('world', 'NOUN', 'O'),
             ('say', 'VERB', 'O'),
             ('they', 'PRON', 'B-COREF-PLURAL'),
             ('stand', 'VERB', 'O'),
             ('for', 'ADP', 'O'),
             ('peace', 'NOUN', 'O')])

    def test_neutral(self):
        self.assertEqual(solver.iob_tag(
            "A majority of the nation said they are in favor of democracy"),
            [('A', 'DET', 'B-ENTITY-NEUTRAL'),
             ('majority', 'NOUN', 'I-ENTITY-NEUTRAL'),
             ('of', 'ADP', 'I-ENTITY-NEUTRAL'),
             ('the', 'DET', 'I-ENTITY-NEUTRAL'),
             ('nation', 'NOUN', 'I-ENTITY-NEUTRAL'),
             ('said', 'VERB', 'O'),
             ('they', 'PRON', 'B-COREF-NEUTRAL'),
             ('are', 'AUX', 'O'),
             ('in', 'ADP', 'O'),
             ('favor', 'NOUN', 'O'),
             ('of', 'ADP', 'O'),
             ('democracy', 'NOUN', 'O')])

    def test_multiple_corefs(self):
        # plural + inanimate
        # they is cast neutral -> plural
        # puppy is cast neutral -> inanimate
        self.assertEqual(solver.iob_tag(
            "My neighbours just adopted a puppy. They care for it like a baby"),
            [('My', 'PRON', 'B-ENTITY-PLURAL'),
             ('neighbours', 'NOUN', 'I-ENTITY-PLURAL'),
             ('just', 'ADV', 'O'),
             ('adopted', 'VERB', 'O'),
             ('a', 'DET', 'B-ENTITY-INANIMATE'),
             ('puppy', 'NOUN', 'I-ENTITY-INANIMATE'),
             ('.', 'PUNCT', 'O'),
             ('They', 'PRON', 'B-COREF-PLURAL'),
             ('care', 'VERB', 'O'),
             ('for', 'ADP', 'O'),
             ('it', 'PRON', 'B-COREF-INANIMATE'),
             ('like', 'ADP', 'O'),
             ('a', 'DET', 'O'),
             ('baby', 'NOUN', 'O')])
        # plural + male
        # they is cast neutral -> plural
        self.assertEqual(solver.iob_tag(
            "Members voted for John because they see him as a good leader"),
            [('Members', 'NOUN', 'B-ENTITY-PLURAL'),
             ('voted', 'VERB', 'O'),
             ('for', 'ADP', 'O'),
             ('John', 'PROPN', 'B-ENTITY-MALE'),
             ('because', 'SCONJ', 'O'),
             ('they', 'PRON', 'B-COREF-PLURAL'),
             ('see', 'VERB', 'O'),
             ('him', 'PRON', 'B-COREF-MALE'),
             ('as', 'ADP', 'O'),
             ('a', 'DET', 'O'),
             ('good', 'ADJ', 'O'),
             ('leader', 'NOUN', 'O')])

    @unittest.skip(" this package does not aim to be SOTA or has illusions of handling some of these")
    def test_known_failures(self):
        # know how to handle one of these? send a PR!
        # this package does not aim to be SOTA or has illusions of handling some of these

        # failures to ignore
        self.assertEqual(solver.replace_corefs("John called him"), "John called him")  # John called John
        self.assertEqual(solver.replace_corefs("John sent him his tax forms"),
                         "John sent him John tax forms")  # John sent John John tax forms

        # difficulty level: HARD
        # "John yelled at Jeff because he said he went back on his promise to fix his machines before he went home"
        # "John yelled at Jeff because Jeff said John went back on John promise to fix Jeff machines before John went home"
        # "John yelled at Jeff because Jeff said John went back on John promise to fix Jeff machines before Jeff went home"
        # "John yelled at Jeff because Jeff said John went back on John promise to fix Jeff machines before John went home"
        # "John yelled at Jeff because Jeff said John went back on John promise to fix John machines before Jeff went home"
        # "John yelled at Jeff because Jeff said John went back on John promise to fix John machines before John went home"
        self.assertEqual(
            solver.replace_corefs(
                "John yelled at Jeff because he said he went back on his promise to fix his machines before he went home"),
            "John yelled at Jeff because Jeff said John went back on John promise to fix Jeff machines before John went home")  # Jeff Jeff Jeff Jeff Jeff Jeff ...
