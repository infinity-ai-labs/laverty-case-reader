from case_reader.citations import LawIndex, article_key, article_numbers, check_citation, split_multi_article

INDEX = LawIndex()


def cite(number, year, article, kind="federal_decree_law", emirate="", quote="", text_ar=""):
    return {"law_number": number, "law_year": year, "article": article, "law_kind": kind,
            "emirate": emirate, "quoted_text_ar": quote, "text_ar": text_ar, "page": 1}


def test_article_key():
    assert article_key("47") == "47"
    assert article_key("المادة (٤٧)") == "47"
    assert article_key("25/1/أ") == "25"
    assert article_key("12 مكرر") == "12 bis"
    assert article_key("") == ""
    assert article_key("البند (1)") == ""          # a clause number is not an article
    assert article_key("المادتين 43 و145") == ""   # two articles: no single key


def test_article_numbers_follow_the_article_word():
    assert article_numbers("البند (1) من المادة (145) من المرسوم بقانون ذاته") == ["145"]
    assert article_numbers("المادتين (43) و(145)") == ["43", "145"]
    assert article_numbers("المادة (54) من المرسوم بقانون اتحادي رقم (33) لسنة 2021") == ["54"]
    assert article_numbers("البند (1) والبند (2) من المادة (47)") == ["47"]


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


def test_the_citation_as_written_wins_over_a_clause_number_in_the_field():
    result = check_citation(cite("33", 2021, "1", text_ar="البند (1) من المادة (145) من المرسوم بقانون ذاته"), INDEX)
    assert result["status"] == "invalid" and result["article"] == "145"


def test_two_articles_in_one_citation_are_both_checked():
    entries = split_multi_article([cite("33", 2021, "43", text_ar="المادتين (43) و(145)")])
    assert [e["article_checked"] for e in entries] == ["43", "145"]
    assert [check_citation(e, INDEX)["status"] for e in entries] == ["valid", "invalid"]
    split = split_multi_article([cite("33", 2021, "43 و 145", text_ar="المادتين (43) و(145)")])
    assert [e["article_checked"] for e in split] == ["43", "145"]


def test_law_outside_the_index_is_never_passed_quietly():
    # The Crimes and Penalties Law is a real law the test files don't cite, so it isn't in the index.
    assert check_citation(cite("31", 2021, "1"), INDEX)["status"] == "not_checked"


def test_the_law_must_be_the_same_kind_and_emirate():
    # Same number and year as an indexed law, but a different law.
    assert check_citation(cite("26", 2007, "25", kind="federal_law"), INDEX)["status"] == "not_checked"
    assert check_citation(cite("26", 2007, "25", kind="local_law", emirate="Abu Dhabi"), INDEX)["status"] == "not_checked"
    assert check_citation(cite("50", 2022, "3", kind="cabinet_resolution"), INDEX)["status"] == "not_checked"
    assert check_citation(cite("33", 2021, "5", kind="local_law", emirate="Dubai"), INDEX)["status"] == "not_checked"
    assert check_citation(cite("26", 2007, "25", kind="local_law", emirate=""), INDEX)["reason"] == "local_without_emirate"


def test_local_law():
    assert check_citation(cite("26", 2007, "25", kind="local_law", emirate="Dubai"), INDEX)["status"] == "valid"
    assert check_citation(cite("26", 2007, "25", kind="local_law", emirate="دبي"), INDEX)["status"] == "valid"
    assert check_citation(cite("26", 2007, "38", kind="local_law", emirate="Dubai"), INDEX)["status"] == "invalid"
    # A federal decree-law cited as a "federal law" is still the federal law with that number and year.
    assert check_citation(cite("33", 2021, "54", kind="federal_law"), INDEX)["status"] == "valid"


def test_quote_check():
    law = next(l for l in INDEX.laws if l["number"] == "50")
    official = law["texts"]["73"]["ar"]
    same = check_citation(cite("50", 2022, "73", quote=official), INDEX)
    assert same["quote"]["status"] == "matches"

    changed = official.replace("المتفق عليه", "القانوني")
    differs = check_citation(cite("50", 2022, "73", quote=changed), INDEX)["quote"]
    assert differs["status"] == "differs" and not differs["slight"]
    assert differs["differences"] == [{"in_file": "القانوني", "official": "المتفق عليه", "kind": "wording"}]
    assert "القانوني" in differs["label_en"]

    # A one-word swap that looks like a misreading is still reported, never passed as a match.
    for a, b in (("المدين", "الدائن"), ("احتسبت", "احتسبب")):
        quote = check_citation(cite("50", 2022, "73", quote=official.replace(a, b)), INDEX)["quote"]
        assert quote["status"] == "differs" and quote["slight"]

    unrelated = "يجب على المستأجر أن يسلم العقار عند انتهاء العقد بالحالة التي تسلمه عليها"
    assert check_citation(cite("50", 2022, "73", quote=unrelated), INDEX)["quote"]["status"] == "does_not_match"


def test_quote_of_an_article_without_stored_text_is_not_checked():
    result = check_citation(cite("50", 2022, "5", quote="نص مقتبس"), INDEX)
    assert result["status"] == "valid" and result["quote"]["status"] == "not_checked"


def test_flags_for_quotes_that_differ_or_were_not_compared():
    from case_reader.assemble import _auto_flags
    law = next(l for l in INDEX.laws if l["number"] == "50")
    official = law["texts"]["73"]["ar"]
    citations = [
        {**cite("50", 2022, "73", quote=official.replace("المتفق عليه", "القانوني")), "text_ar": "المادة (73)"},
        {**cite("50", 2022, "73", quote=official.replace("المدين", "الدائن")), "text_ar": "المادة (73)"},
        {**cite("50", 2022, "5", quote="نص مقتبس"), "text_ar": "المادة (5)"},
    ]
    summary = {"citations": [{**c, "check": check_citation(c, INDEX)} for c in citations],
               "dates": [], "deadlines": [], "marks": []}
    assert [f["severity"] for f in _auto_flags(summary)] == ["high", "high", "medium"]


def test_article_written_with_raqm_ranges_and_bis():
    assert article_numbers("المادة رقم (145)") == ["145"]
    assert article_numbers("المواد (73-76)") == ["73", "74", "75", "76"]
    assert article_numbers("من المادة (73) إلى المادة (76)") == ["73", "74", "75", "76"]
    assert article_numbers("المادة (12) مكرراً") == ["12 bis"]
    entries = split_multi_article([cite("50", 2022, "73", text_ar="المواد (73-76) من قانون المعاملات التجارية")])
    assert [e["article_checked"] for e in entries] == ["73", "74", "75", "76"]


def test_clause_number_in_the_field_is_not_checked_twice():
    entries = split_multi_article([cite("33", 2021, "1", text_ar="البند (1) من المادة (145) من المرسوم بقانون ذاته")])
    assert [e["article_checked"] for e in entries] == ["145"]


def test_a_field_that_disagrees_with_the_words_gets_both_checked():
    entries = split_multi_article([cite("33", 2021, "145", text_ar="المادة (43)")])
    assert sorted(e["article_checked"] for e in entries) == ["145", "43"]
    assert sorted(check_citation(e, INDEX)["status"] for e in entries) == ["invalid", "valid"]


def test_words_naming_two_laws_do_not_lend_articles_across_laws():
    text = "المادة (54) من المرسوم بقانون رقم (33) لسنة 2021 والمادة (712) من المرسوم بقانون رقم (50) لسنة 2022"
    entries = split_multi_article([cite("33", 2021, "54", text_ar=text), cite("50", 2022, "712", text_ar=text)])
    results = [(e["law_number"], e["article_checked"], check_citation(e, INDEX)["status"]) for e in entries]
    assert results == [("33", "54", "valid"), ("50", "712", "invalid")]


def test_emirate_written_in_full():
    for emirate in ("إمارة دبي", "Emirate of Dubai", "Dubai"):
        assert check_citation(cite("26", 2007, "25", kind="local_law", emirate=emirate), INDEX)["status"] == "valid"


def test_duplicate_entries_are_merged():
    c = cite("33", 2021, "145", text_ar="المادة (145) من المرسوم بقانون ذاته")
    assert len(split_multi_article([c, dict(c)])) == 1


def test_a_repealed_law_is_flagged_even_when_the_article_exists():
    from case_reader.assemble import _auto_flags
    c = cite("5", 1985, "885", kind="federal_law", text_ar="المادة (885)")
    check = check_citation(c, INDEX)
    assert check["status"] == "valid" and check["law_status"]["state"] == "repealed"
    flags = _auto_flags({"citations": [{**c, "check": check}], "dates": [], "deadlines": [], "marks": []})
    assert [f["severity"] for f in flags] == ["medium"] and "repealed" in flags[0]["flag_en"]


def test_quote_left_in_citation_text_is_still_checked():
    """Muse Spark sometimes leaves the quote inside text_ar; the check must still compare it."""
    from case_reader.citations import quote_in_text
    text = ('وتلزم المادة (246) منه فاعل الإضرار بالغير بضمان الضرر، وتنص المادة (255) على أنه: '
            '"يُقدَّر التعويض في جميع الأحوال بقدر ما لحق المضرور من ضرر وما فاته من كسب، '
            'بشرط أن يكون ذلك نتيجة محتملة للفعل الضار".')
    assert quote_in_text(text, "255").startswith("يُقدَّر التعويض")
    assert quote_in_text(text, "246") == ""  # the quote belongs to the next article, not this one
    assert quote_in_text("المادة (12) من القانون", "12") == ""
    assert quote_in_text('المادة (١٢) تنص على «لا يجوز للمؤجر زيادة الأجرة»', "12") == "لا يجوز للمؤجر زيادة الأجرة"
