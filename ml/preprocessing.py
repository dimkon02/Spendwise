import re

SUFFIX_WORDS = (
    r"(store|online|branch|strip mall|shopping center|mall|center|airport|station|"
    r"downtown|hospital|campus|residential|business district)"
)

def clean_merchant(desc: str) -> str:
    """
    Extract the merchant name from a raw transaction description.

    Args:
        desc: The raw transaction description,
            e.g. "Spotify #2659 Store Strip Mall - UK".

    Returns:
        The cleaned merchant name, e.g. "spotify".
    """
    s = desc.lower()
    s = s.split(" - ")[0]                     # cuts text at every '-' gives a list of strings, keeps only first element
    s = re.sub(r"\(.*?\)", "", s)             # deletes anything inside brackets
    s = re.sub(r"#\d+", "", s)                # deletes # followed by number
    s = re.sub(r"txn\d+", "", s)              # deletes txt followed by numbers
    s = re.sub(r"\s+", " ", s).strip()        # "payroll  hospital" -> "payroll hospital"
    # remove suffix words at the end, repeatedly ("store center airport")
    while True:
        new = re.sub(rf"\s+{SUFFIX_WORDS}$", "", s).strip()
        if new == s:
            break
        s = new
    return s