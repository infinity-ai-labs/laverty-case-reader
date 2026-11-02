from case_reader.arabic import best_window_ratio, normalize, similarity, to_ascii_digits


def test_digits():
    assert to_ascii_digits("٢٠٢٦/١٠/٠٥ ۱۲") == "2026/10/05 12"


def test_normalize_letter_forms_and_diacritics():
    assert normalize("إِخْلاءُ المأجورِ") == normalize("اخلاء الماجور")
    assert normalize("مؤسسة الصقر الذهبي") == normalize("موسسه الصقر الذهبي")
    assert normalize("شركة   (نجمة)  ذ.م.م") == "شركه نجمه ذ م م"


def test_similarity_of_names():
    assert similarity("سامر خليل الحداد", "سامر خليل الحدّاد") == 1.0
    assert similarity("شركة نجمة الخليج للمقاولات العامة ذ.م.م", "نجمة الخليج للمقاولات العامة ذ م م شركة") > 0.85
    assert similarity("سامر خليل الحداد", "هند سعيد الكعبي") < 0.6


def test_best_window_ratio():
    text = "إذا تضمن العقد اتفاقاً على سعر الفائدة، وتأخر المدين في الوفاء، احتسبت الفائدة التأخيرية"
    assert best_window_ratio("وتأخر المدين في الوفاء", text) == 1.0
    assert best_window_ratio("وتأخر الدائن في الوفاء", text) < 1.0
