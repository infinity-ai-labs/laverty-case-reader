from case_reader.marks import clean_marks, iou, parse_sam_output

DOC_SAMPLE = "<0f>0<|box;x1=181;y1=365;x2=556;y2=486;w=1516;h=1600|><|mask;x=0;y=0;data=122,376,~abc|>"


def test_parses_the_documented_record():
    boxes, problems = parse_sam_output(DOC_SAMPLE)
    assert problems == []
    assert len(boxes) == 1
    b = boxes[0]
    assert (b.object_id, b.x1, b.y1, b.x2, b.y2, b.width, b.height) == (0, 181, 365, 556, 486, 1516, 1600)
    assert b.confidence is None
    assert b.fraction() == [round(181 / 1516, 5), round(365 / 1600, 5), round(557 / 1516, 5), round(487 / 1600, 5)]


def test_several_records_confidence_and_token_order():
    text = (
        "<0f>0<|box;x1=10;y1=20;x2=110;y2=60;w=200;h=100;c=0.91|><|mask;x=0;y=0;data=4,4,!AA;c=0.9|>"
        ",1<|mask;x=0;y=0;data=2,2,~Z|><|box;x1=0;y1=0;x2=9;y2=9;w=200;h=100|>\n"
        "<1f;foo=bar>2<|box;x1=5;y1=5;x2=6;y2=6;w=200;h=100;c=0.5|><|mask;x=0;y=0;data=1,1,!A|>"
    )
    boxes, problems = parse_sam_output(text)
    assert problems == []
    assert [b.object_id for b in boxes] == [0, 1, 2]
    assert boxes[0].confidence == 0.91
    assert boxes[1].confidence is None
    assert boxes[2].confidence == 0.5


def test_empty_output_means_no_matches():
    assert parse_sam_output("") == ([], [])


def test_box_outside_the_image_is_reported_not_kept():
    boxes, problems = parse_sam_output("<0f>0<|box;x1=10;y1=10;x2=300;y2=20;w=200;h=100|><|mask;x=0;y=0;data=1,1,!A|>")
    assert boxes == []
    assert len(problems) == 1


def test_iou():
    assert iou([0, 0, 1, 1], [0, 0, 1, 1]) == 1.0
    assert iou([0, 0, 1, 1], [2, 2, 3, 3]) == 0.0
    assert round(iou([0, 0, 2, 1], [1, 0, 3, 1]), 3) == round(1 / 3, 3)


def test_clean_marks_drops_duplicates_weak_and_huge_boxes_and_numbers_in_reading_order():
    found = [
        {"page": 1, "type": "stamp", "found_as": "rubber stamp", "box": [0.1, 0.1, 0.3, 0.2], "confidence": 0.9},
        {"page": 1, "type": "stamp", "found_as": "seal", "box": [0.1, 0.1, 0.31, 0.2], "confidence": 0.8},  # duplicate
        {"page": 1, "type": "handwriting", "found_as": "handwritten text", "box": [0.6, 0.5, 0.8, 0.55], "confidence": 0.7},
        {"page": 1, "type": "signature", "found_as": "signature", "box": [0.6, 0.5, 0.8, 0.56], "confidence": 0.6},
        {"page": 1, "type": "handwriting", "found_as": "handwritten text", "box": [0.0, 0.0, 1.0, 1.0], "confidence": 0.9},  # huge
        {"page": 1, "type": "stamp", "found_as": "rubber stamp", "box": [0.5, 0.8, 0.7, 0.9], "confidence": 0.1},  # weak
        {"page": 2, "type": "signature", "found_as": "signature", "box": [0.2, 0.7, 0.4, 0.75], "confidence": None},
        {"page": 1, "type": "stamp", "problem": "unreadable"},
    ]
    kept = clean_marks(found)
    assert [(m["mark_id"], m["page"], m["type"]) for m in kept] == [
        ("M1", 1, "stamp"), ("M2", 1, "signature"), ("M3", 2, "signature"),
    ]


def test_unreadable_output_is_reported():
    boxes, problems = parse_sam_output("<0f>garbage without records")
    assert boxes == [] and len(problems) == 1


def test_reading_order_is_right_to_left_within_a_line():
    found = [
        # one line: a judge's signature on the left, a clerk's on the right (slightly higher)
        {"page": 3, "type": "signature", "found_as": "signature", "box": [0.18, 0.39, 0.37, 0.45], "confidence": 0.9},
        {"page": 3, "type": "signature", "found_as": "signature", "box": [0.61, 0.38, 0.79, 0.43], "confidence": 0.9},
        # a stamp lower down
        {"page": 3, "type": "stamp", "found_as": "rubber stamp", "box": [0.37, 0.44, 0.58, 0.53], "confidence": 0.9},
    ]
    kept = clean_marks(found)
    assert [(m["mark_id"], m["box"][0]) for m in kept] == [("M1", 0.61), ("M2", 0.18), ("M3", 0.37)]


def test_a_signature_across_a_stamp_keeps_both():
    found = [
        {"page": 1, "type": "stamp", "found_as": "rubber stamp", "box": [0.30, 0.50, 0.60, 0.65], "confidence": 0.9},
        {"page": 1, "type": "signature", "found_as": "signature", "box": [0.33, 0.52, 0.58, 0.62], "confidence": 0.8},
    ]
    assert len(clean_marks(found)) == 2


class _FailingSam:
    def segment(self, concept, image_url, **kwargs):
        from case_reader.meta_api import MetaAPIError
        raise MetaAPIError(500, "server error")


def test_a_failed_sam_call_is_recorded_not_fatal(tmp_path):
    from PIL import Image
    from case_reader.marks import find_marks_on_page
    from case_reader.pages import Page
    path = tmp_path / "page-1.jpg"
    Image.new("RGB", (200, 280), "white").save(path)
    found = find_marks_on_page(_FailingSam(), Page(1, path, 200, 280), {"stamp": ["rubber stamp"]})
    assert found and "problem" in found[0] and "failed" in found[0]["problem"]
