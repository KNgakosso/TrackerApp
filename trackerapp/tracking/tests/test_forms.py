from tracking.forms import SearchForm, SectionNumberForm, WatchlistSelectionForm
from tracking.models.watchlist_model import WatchlistModel


def test_section_number_form_ok():
    form = SectionNumberForm(max_value=52, data={"section_number": "10"})
    assert len(form["section_number"].field.choices) == 53
    assert form.is_valid()


def test_section_number_form_higher():
    form = SectionNumberForm(max_value=15, data={"section_number": "108"})
    assert not form.is_valid()


def test_section_number_form_max_value():
    form = SectionNumberForm(max_value=45, data={"section_number": "45"})
    assert form.is_valid()


def test_section_number_form_default_value():
    form = SectionNumberForm(data={"section_number": "0"})
    assert len(form["section_number"].field.choices) == 1
    assert form.is_valid()


def test_watchlist_selection_form(db):
    watchlist_model_1 = WatchlistModel.objects.create(name="Liste A")
    watchlist_model_2 = WatchlistModel.objects.create(name="Liste B")

    form = WatchlistSelectionForm(data={"name": watchlist_model_1})
    assert form.is_valid()


def test_search_form_clean_score_not_ok():
    form = SearchForm(data={"min_score": 9, "max_score": 4, "type": ["anime"]})

    assert not form.is_valid()


def test_search_form_clean_score_ok():
    form = SearchForm(data={"min_score": 1, "max_score": 2, "type": ["manga"]})

    assert form.is_valid()


def test_search_form_clean_score_equal():
    form = SearchForm(data={"min_score": 6, "max_score": 6, "type": ["manga", "anime"]})
    assert form.is_valid()
