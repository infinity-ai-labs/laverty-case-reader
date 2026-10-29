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
