from case_reader.citations import LawIndex, article_key, check_citation

INDEX = LawIndex()


def cite(number, year, article, kind="federal_decree_law", emirate="", quote=""):
    return {"law_number": number, "law_year": year, "article": article, "law_kind": kind,
            "emirate": emirate, "quoted_text_ar": quote, "text_ar": "", "page": 1}


def test_article_key():
    assert article_key("المادة (٤٧)") == "47"
    assert article_key("25/1/أ") == "25"
    assert article_key("12 مكرر") == "12 bis"
    assert article_key("") == ""


def test_valid_article_comes_with_official_text():
    result = check_citation(cite("33", 2021, "54"), INDEX)
    assert result["status"] == "valid"
    assert result["official_text_ar"]
    assert result["source_url_en"].startswith("https://")


def test_article_beyond_the_end_of_the_law_is_invalid():
    labour = check_citation(cite("33", 2021, "145"), INDEX)
    commercial = check_citation(cite("٥٠", "٢٠٢٢", "712"), INDEX)
    assert labour["status"] == "invalid" and "74 articles" in labour["label_en"]
    assert commercial["status"] == "invalid" and "684 articles" in commercial["label_en"]


def test_law_outside_the_index_is_never_passed_quietly():
    result = check_citation(cite("5", 1985, "1", kind="federal_law"), INDEX)
    assert result["status"] == "not_checked"


def test_local_law():
    assert check_citation(cite("26", 2007, "25", kind="local_law", emirate="Dubai"), INDEX)["status"] == "valid"
    assert check_citation(cite("26", 2007, "38", kind="local_law", emirate="Dubai"), INDEX)["status"] == "invalid"


def test_quote_check():
    law = next(l for l in INDEX.laws if l["number"] == "50")
    official = law["texts"]["73"]["ar"]
    same = check_citation(cite("50", 2022, "73", quote=official), INDEX)
    assert same["quote"]["status"] == "matches"
    changed = official.replace("المتفق عليه", "القانوني")
    differs = check_citation(cite("50", 2022, "73", quote=changed), INDEX)["quote"]
    assert differs["status"] == "differs"
    assert differs["differences"] == [{"in_file": "القانوني", "official": "المتفق عليه"}]
    assert "القانوني" in differs["label_en"]
    unrelated = "يجب على المستأجر أن يسلم العقار عند انتهاء العقد بالحالة التي تسلمه عليها"
    assert check_citation(cite("50", 2022, "73", quote=unrelated), INDEX)["quote"]["status"] == "does_not_match"
