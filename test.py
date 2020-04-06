import typing as T
import sys

import pytest

from insult_error import InsultError, insult_names, insult_messages, insulthook


def valid_names(rating):
    return {n.name for n in insult_names if n.rating <= rating}


def valid_msgs(rating):
    return {m.msg for m in insult_messages if m.rating <= rating}


def validate_insult(
    exc: BaseException,
    rating: int = InsultError.RATING,
    msg: T.Optional[str] = None
):
    """Check that the input exception instance is an InsultError allowed for given rating"""
    # check type
    assert isinstance(exc, InsultError), 'Expect an InsultError'

    # check random defined name
    assert exc.__class__.__name__ in valid_names(rating), 'Exception name is not right'

    if msg: # check user-specified message
        assert str(exc) == msg
    else: # check random defined messages
        assert str(exc) in valid_msgs(rating), 'Exception message is not right'


@pytest.mark.parametrize('rating', range(1, 11))
def test_insult_with_rating(rating: int):
    exc = InsultError(rating=rating)
    validate_insult(exc, rating)


def test_insult_default_rating():
    exc = InsultError()
    validate_insult(exc, InsultError.RATING)


def test_insult_with_msg():
    rating = 5   # arbitrary
    msg = 'this is my message, which is boring'
    exc = InsultError(msg)
    validate_insult(exc, rating, msg)


def get_exc_info(cls, message=None):
    """Return the (type, value, traceback) arguments that sys.excepthook consumes"""
    try:
        if message:
            raise cls(message)
        else:
            raise cls
    except cls:
        return sys.exc_info()


def parse_exc_text(cap):
    """Chop up stderr output from excepthook into testable bits"""
    txt = cap.readouterr().err
    tb_txt, exc_txt = txt.strip().rsplit('\n', maxsplit=1)
    try:
        exc_name, exc_msg = exc_txt.split(':', maxsplit=1)
        exc_msg = exc_msg.lstrip()
    except ValueError:
        exc_name = exc_txt
        exc_msg = None
    return exc_name, exc_msg, tb_txt


# note: capsys is pytest magic for capturing stdout/stderr
#   see: https://docs.pytest.org/en/latest/capture.html


@pytest.mark.parametrize('preserve', (True, False))  # expect result to be independent of this param
@pytest.mark.parametrize('rating', [1, 5, 10])  # try a few
def test_insulthook_without_message(preserve, rating, capsys):

    rating = 5
    ref_info = get_exc_info(ValueError)
    sys.excepthook(*ref_info)  # FIXME: bug in pycharm debugger, calls exit in excepthook
    ref_name, _, ref_tb = parse_exc_text(capsys)

    insulthook(rating=rating, preserve_msg=preserve)(*ref_info)
    obs_name, obs_msg, obs_tb = parse_exc_text(capsys)
    assert obs_name in valid_names(rating)
    assert obs_msg in valid_msgs(rating)
    assert obs_tb == ref_tb


@pytest.mark.parametrize('rating', [1, 5, 10])  # try a few
def test_insulthook_with_message(rating, capsys):

    ref_msg = 'a message'
    ref_info = get_exc_info(ValueError, ref_msg)
    sys.excepthook(*ref_info)  # FIXME: bug in pycharm debugger, calls exit in excepthook
    ref_name, _, ref_tb = parse_exc_text(capsys)

    # ignore (overwrite) existing message
    insulthook(rating=rating, preserve_msg=False)(*ref_info)
    obs_name, obs_msg, obs_tb = parse_exc_text(capsys)
    assert obs_name.lstrip('insult_error.') in valid_names(rating)
    assert obs_msg in valid_msgs(rating)
    assert obs_tb == ref_tb

    # preserve existing message
    insulthook(rating=rating, preserve_msg=True)(*ref_info)
    obs_name, obs_msg, obs_tb = parse_exc_text(capsys)
    assert obs_name.lstrip('insult_error.') in valid_names(rating)
    assert obs_msg == ref_msg
    assert obs_tb == ref_tb


# note: it would be nice to test [dont_]always_insult_me, but it is quite
#   awkward to do so because sys.excepthook is not called until just before
#   the process is terminated due to an uncaught exception. For now, consider
#   this not worth it.
