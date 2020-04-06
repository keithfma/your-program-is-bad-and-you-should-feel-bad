import sys
import random
from collections import namedtuple


# the main event! ----------


class InsultError(Exception):
    """
    Randomized insulting error name and message

    Arguments:
        *args: positional arguments for anything you would normally pass when creating an
            Exception object, usually just a message string
        rating: optionally, set a limit on how offensive the error can be as a number between
            1 and 10 (1 being tamest, and 10 being meanest), defaults to 5
    """

    RATING = 5

    def __init__(self, *args, rating=None):
        if rating is None:
            rating = self.RATING
        # hack the error name to be a random insult rated <= rating
        name = random.choice([x.name for x in insult_names if x.rating <= rating])
        self.__class__.__name__ = name
        # hack the error module name so it pretends to be a built-in, yields a prettier traceback
        # see: traceback.format_exception_only method
        self.__class__.__module__ = 'builtins'
        # if no message is provided, select a random insult
        if not args:
            msg = random.choice([x.msg for x in insult_messages if x.rating <= rating])
            args = (msg,)
        self.args = args


# automatic insults ----------


def insulthook(rating=None, preserve_msg=False):
    """
    Return a sys.excepthook standin that injects InsultError, but leaves the traceback

    Arguments:
        rating: limit for how offensive you want the error and messages to be
            (1 being tamest and 10 being meanest)
        preserve_msg: set True to keep the message string from the original error,
            or False to replace it with an insult
    """
    def f(type, value, traceback):
        """sys.excepthook standin that injects an error but leaves the traceback"""
        if str(value) and preserve_msg:
            exc = InsultError(str(value), rating=rating)
        else:
            exc = InsultError(rating=rating)
        sys.__excepthook__(type(exc), exc, traceback)
    return f


def always_insult_me(rating=None, preserve_msg=False):
    """Replace uncaught exceptions with insults at or below rating"""
    sys.excepthook = insulthook(rating, preserve_msg)


def dont_always_insult_me():
    """Stop replacing uncaught exceptions with insults"""
    sys.excepthook = sys.__excepthook__


# insulting error names ----------


_Name = namedtuple('Name', ('name', 'rating'))

insult_names = [
    _Name(rating=5, name='FuckYouBuddy'),
    _Name(rating=5, name='FuckYouFriend'),
    _Name(rating=4, name='FrickYouPal'),
    _Name(rating=1, name='NotThisAgain'),
    _Name(rating=1, name='ForGodsSake'),
    _Name(rating=1, name='AreYouSerious'),
]


# insulting error messages ----------


_Message = namedtuple('Message', ('msg', 'rating'))

insult_messages = [
    _Message(rating=1, msg="Your program is bad and you should feel bad"),
    _Message(rating=1, msg="I envy people who have never met you"),
    _Message(rating=1, msg="You're impossible to underestimate"),
    _Message(rating=1, msg="I don't have the time or the crayons to explain this to you"),
    _Message(rating=1, msg="Don't believe everything you think"),
    _Message(rating=1, msg="I hope this isn't your day job"),
    _Message(rating=1, msg="You're killing your mother right now"),
    _Message(rating=1, msg="I hear that fast food place is still hiring"),
    _Message(rating=1, msg="If you were on fire and I had water, I'd drink it."),
    _Message(rating=1, msg="You messed up - don't try again for your own good"),
    _Message(rating=1, msg=(
        "This is like being in a house built by a child using nothing but a "
        "hatchet and a picture of a house [xkcd.com/1513]")),
    _Message(rating=1, msg=(
        "It's like a salad recipe written by a corporate lawyer using a phone "
        "autocorrect that only knew excel formulas [xkcd.com/1513]")),
    _Message(rating=1, msg=(
        "It's like someone took a transcript of a couple arguing at Ikea and "
        "made random edits until it compiled without errors [xkcd.com/1513]")),
    # Message(rating=1, msg=(
    #     "It's like you ran OCR on a photo of a scrabble game board from a game "
    #     "where Javascript reserved words counted for triple points "
    #     "[xkcd.com/1695]")),
    # Message(rating=1, msg=(
    #     "It looks like someone transcribed a naval weather forecast while "
    #     "woodpeckers hammered thier shift keys, then randomely indented it"
    #     "[xkcd.com/1695]")),
    # Message(rating=1, msg=(
    #     "It's like an E.E. Cummings poem written using only the usernames a "
    #     "website suggests when the one you want is taken [xkcd.com/1695]")), 
    # Message(rating=1, msg=(
    #     "This looks like the output of a Markov bot that's been fed bus "
    #     "timetables from a city where the buses crash constantly [xkcd.com/1695]")),
    # Message(rating=1, msg=(
    #     "Your code looks like song lyrics written using only the stuff that "
    #     "comes after the question mark in a URL [xkcd.com/1833]")),
    # Message(rating=1, msg=(
    #     "It's like a JSON table of model numbers for flashlights with "
    #     "'tactical' in thier names [xkcd.com/1833]")),
    # Message(rating=1, msg=(
    #     "Your code looks like you read Turing's 1936 paper on computing and a "
    #     "page of Javascipt example code and guessed at everything in between "
    #     "[xkcd.com/1833]")), 
    _Message(rating=1, msg=(
        "It's like a leet-speak translation of a manifesto by a survivalist"
        "cult leader who's for some reason obsessed with memory allocation"
        "[xkcd.com/1833]")),
] 

