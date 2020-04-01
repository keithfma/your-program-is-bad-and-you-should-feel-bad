import typing as T
import pytest
import insult_error


def validate_insult(
    exc: BaseException,
    rating: int = insult_error.InsultError.RATING,
    msg: T.Optional[str] = None
):
    """Check that the input exception instance is an InsultError allowed for given rating"""
    # check type
    assert isinstance(exc, insult_error.InsultError), 'Expect an InsultError'

    # check random defined name
    valid_names = {n.name for n in insult_error.names if n.rating <= rating}
    assert exc.__class__.__name__ in valid_names, 'Exception name is not right'

    if msg: # check user-specified message
        assert str(exc) == msg
    else: # check random defined messages
        valid_msgs = {m.msg for m in insult_error.messages if m.rating <= rating}
        assert str(exc) in valid_msgs, 'Exception message is not right'


@pytest.mark.parametrize('rating', range(1,11))
def test_insult_with_rating(rating: int):
    exc = insult_error.InsultError(rating=rating)
    validate_insult(exc, rating)


def test_insult_default_rating():
    exc = insult_error.InsultError()
    validate_insult(exc, insult_error.InsultError.RATING)


def test_insult_with_msg():
    rating = 5   # arbitrary
    msg = 'this is my message, which is boring'
    exc = insult_error.InsultError(msg)
    validate_insult(exc, rating ,msg)


def test_always_insult_me():

    # insult_error.always_insult_me()

    try:
        raise ValueError()
    except Exception as exc:
        print()

