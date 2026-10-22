import pytest

from ml.preprocessing import clean_merchant


@pytest.mark.parametrize(
    "description, expected",
    [
        ("Spotify #2659 Store Strip Mall", "spotify"),                # number + several suffix words
        ("Target - INDIA - Dinner Time", "target"),                   # everything after " - " removed
        ("UCSF Medical #2190 (App)", "ucsf medical"),                 # brackets removed
        ("UCLA Medical #7731 - UK Center TXN176162", "ucla medical"), # all patterns at once
        ("Pure Barre Store Center Airport", "pure barre"),            # suffix words removed repeatedly
        ("Payroll #12 Hospital", "payroll"),                          # no double space left behind
    ],
)
def test_clean_merchant_removes_templates(description, expected):
    assert clean_merchant(description) == expected


@pytest.mark.parametrize(
    "description, expected",
    [
        ("Walmart Supercenter Shopping Center", "walmart supercenter"),  # "center" inside a word is kept
        ("Safeway Pharmacy", "safeway pharmacy"),                         # real words in the name are kept
        ("Chick-fil-A Store", "chick-fil-a"),                             # hyphens without spaces are not cut
        ("Dinner at Italian Restaurant", "dinner at italian restaurant"), # plain phrases stay as they are
    ],
)
def test_clean_merchant_keeps_real_names(description, expected):
    assert clean_merchant(description) == expected


def test_clean_merchant_is_lowercase():
    assert clean_merchant("KFC") == "kfc"