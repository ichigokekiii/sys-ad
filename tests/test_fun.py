"""Roast, quiz, and map URL results a caller can see."""

from fun import grade, map_embed, quiz_for, roast

PLDT_ROAST = (
    "PLDT brought you here the long way around. "
    "The pin is probably a building you have never visited."
)


def test_pldt_roast_is_about_the_network():
    line = roast("PLDT", "PH")
    assert line == PLDT_ROAST
    lowered = line.lower()
    for insult in ("stupid", "idiot", "ugly", "dumb", "loser"):
        assert insult not in lowered


def test_roast_without_an_isp_still_says_something():
    assert roast(None, "PH").strip()


def test_quiz_for_pldt_is_stable():
    first = quiz_for("PLDT")
    second = quiz_for("PLDT")
    assert len(first.choices) == 3
    assert "PLDT" in first.choices
    assert second.choices == first.choices


def test_quiz_without_an_isp_has_no_choices():
    assert len(quiz_for(None).choices) == 0


def test_grade_names_the_right_and_wrong_outcome():
    quiz = quiz_for("PLDT")
    assert grade(quiz, "PLDT") == "That's the one."
    wrong = next(choice for choice in quiz.choices if choice != "PLDT")
    assert grade(quiz, wrong) == "Close. This network is PLDT."


def test_map_embed_is_an_openstreetmap_url_or_none():
    url = map_embed(14.5995, 120.9842)
    assert url is not None
    assert url.startswith("https://www.openstreetmap.org/")
    assert map_embed(None, 120.9842) is None
    assert map_embed(14.5995, None) is None
