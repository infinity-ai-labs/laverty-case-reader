# -*- coding: utf-8 -*-
"""Case 10 (fictional): application to ratify and enforce a domestic arbitral award.

A dispute over a construction supply contract (ready-mix concrete and precast elements) was decided
by a three-member tribunal at a fictional arbitration centre; the award creditor asks the Court of
Appeal to ratify the award and order its enforcement. Control case: every citation is valid
(checked against the official texts on 29 Oct 2026). It plants two things only:
  - page 1: one sentence cites two laws (Arbitration Law Art. 52 and Civil Procedure Law Art. 212);
  - page 3: the execution file number and date exist only as a handwritten note.
"""
from cases import BLUE, PURPLE, INK, BLACK_INK, RED  # noqa: F401

CASE = {
    "id": "case-10",
    "slug": "arbitral-award",
    "title_en": "Arbitration: application to ratify and enforce a domestic arbitral award (construction supply)",
    "pages": [
        # ------------------------------------------------------------------ page 1: the application
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مكتب درة الساحل للمحاماة والاستشارات القانونية</div>
    <div class="ent-sub">Durrat Al Sahel Advocates &amp; Legal Consultants</div>
    <div class="ent-sub">دبي — ص.ب: 00000</div>
  </div>
  <div class="meta">
    <div>التاريخ: 20/10/2026</div>
    <div>المرجع: DS/ARB/2026/63</div>
  </div>
</div>
<h1 class="title">طلب المصادقة على حكم التحكيم والأمر بتنفيذه</h1>
<p class="center">مقدم إلى: السيد القاضي/ رئيس محكمة الاستئناف — محاكم دبي</p>
<table class="parties">
  <tr><th>الطالبة</th><td>شركة نسيم الجبل للخرسانة الجاهزة ذ.م.م (المحتكمة)، رخصة تجارية رقم 000000، دبي — القوز الصناعية الرابعة. وكيلتها: المحامية/ ريم ماجد الشحي.</td></tr>
  <tr><th>المطلوب ضدها</th><td>شركة القوس العالي للمقاولات الإنشائية ذ.م.م (المحتكم ضدها)، رخصة تجارية رقم 000000، دبي.</td></tr>
</table>
<h2>الوقائع</h2>
<ol>
  <li>بموجب عقد توريد مؤرخ 12/01/2026 تورد الطالبة الخرسانة الجاهزة والعناصر مسبقة الصب لمشروع تنفذه المطلوب ضدها بدبي، ونص البند (18) منه على حسم أي نزاع بالتحكيم لدى مركز الشراع الأبيض للتحكيم التجاري.</li>
  <li>امتنعت المطلوب ضدها عن سداد باقي قيمة التوريدات، فتقدمت الطالبة بطلب التحكيم بتاريخ 06/04/2026.</li>
  <li>بتاريخ 10/09/2026 أصدرت هيئة التحكيم في القضية رقم (47) لسنة 2026 حكمها بالإجماع بإلزام المطلوب ضدها بأن تؤدي إلى الطالبة (846,300) درهم قيمة التوريدات، و(96,400) درهم مصروفات التحكيم، و(40,000) درهم أتعاب المحاماة، بإجمالي (982,700) درهم، وفائدة (5%) سنوياً على المبلغ الأول من تاريخ طلب التحكيم حتى السداد.</li>
  <li>أُعلن الحكم إلى المطلوب ضدها بتاريخ 15/09/2026، وانقضى في 15/10/2026 ميعاد الثلاثين يوماً المقرر لرفع دعوى البطلان في البند (2) من المادة (54) من القانون الاتحادي رقم (6) لسنة 2018 في شأن التحكيم، دون أن ترفعها.</li>
</ol>
<h2>الأسانيد</h2>
<ol>
  <li>أرفقت الطالبة أصل الحكم وصورة اتفاق التحكيم وصورة محضر إيداع الحكم في المحكمة، وهي المستندات التي يتطلبها البند (1) من المادة (55) من قانون التحكيم.</li>
  <li>ولما كان حكم التحكيم ملزماً للأطراف ويشترط لتنفيذه الحصول على قرار بالمصادقة عليه وفقاً للمادة (52) من القانون الاتحادي رقم (6) لسنة 2018 في شأن التحكيم، وكان التنفيذ الجبري لا يجوز إلا بسند تنفيذي وفقاً للمادة (212) من المرسوم بقانون اتحادي رقم (42) لسنة 2022 بإصدار قانون الإجراءات المدنية، فإن الطالبة تتقدم بهذا الطلب.</li>
</ol>
<h2>الطلبات</h2>
<p>المصادقة على حكم التحكيم المشار إليه والأمر بتنفيذه، مع إلزام المطلوب ضدها بالرسوم والمصروفات.</p>
<div class="sigline">وكيلة الطالبة — المحامية/ ريم ماجد الشحي</div>
""",
            "marks": [
                {"id": "c10-p1-signature-lawyer", "type": "signature", "color": INK, "top": 970, "left": 110,
                 "width": 180, "height": 66, "rotate": -4, "seed": 103,
                 "label_en": "Signature of the applicant's lawyer"},
                {"id": "c10-p1-stamp-lawfirm", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["مكتب درة الساحل للمحاماة", "Durrat Al Sahel Advocates", "دبي — الإمارات"],
                 "top": 968, "left": 316, "width": 220, "height": 84, "rotate": 6, "seed": 107,
                 "label_en": "Law firm stamp", "text_ar": "مكتب درة الساحل للمحاماة — دبي"},
                {"id": "c10-p1-stamp-registry", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["قلم القيد", "نموذج تدريبي", "20/10/2026"], "top": 940, "left": 575, "width": 150,
                 "height": 92, "rotate": -9, "seed": 101,
                 "label_en": "Court of Appeal registry date stamp (training sample)",
                 "text_ar": "قلم القيد — نموذج تدريبي — 20/10/2026"},
            ],
        },
        # ------------------------------------------------------------------ page 2: the award's operative part
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مركز الشراع الأبيض للتحكيم التجاري</div>
    <div class="ent-sub">White Sail Commercial Arbitration Centre</div>
    <div class="ent-sub">دبي — ص.ب: 00000</div>
  </div>
  <div class="meta">
    <div>قضية التحكيم رقم: 47 لسنة 2026</div>
    <div>تاريخ الحكم: 10/09/2026</div>
  </div>
</div>
<h1 class="title">منطوق حكم التحكيم</h1>
<p class="center">حكم نهائي منهٍ للخصومة — صادر بالإجماع</p>
<table class="parties">
  <tr><th>المحتكمة</th><td>شركة نسيم الجبل للخرسانة الجاهزة ذ.م.م، دبي.</td></tr>
  <tr><th>المحتكم ضدها</th><td>شركة القوس العالي للمقاولات الإنشائية ذ.م.م، دبي.</td></tr>
  <tr><th>هيئة التحكيم</th><td>د. عادل منصور الحوسني (رئيساً)، والمهندس/ كريم وليد السعدي (عضواً)، والمحامي/ ناصر عيسى البلوشي (عضواً).</td></tr>
  <tr><th>اتفاق التحكيم</th><td>البند (18) من عقد التوريد المؤرخ 12/01/2026 — مكان التحكيم: دبي — لغة التحكيم: العربية.</td></tr>
</table>
<p>بعد الاطلاع على طلب التحكيم المقدم بتاريخ 06/04/2026، وعلى بيان الدعوى ومذكرات الدفاع والطلب المقابل والمستندات وتقرير الخبير الهندسي، وبعد سماع المرافعة والمداولة، قررت هيئة التحكيم بالإجماع:</p>
<ol>
  <li>إلزام المحتكم ضدها بأن تؤدي إلى المحتكمة مبلغ (846,300) درهم، قيمة الخرسانة الجاهزة والعناصر مسبقة الصب الموردة وغير المسددة.</li>
  <li>إلزام المحتكم ضدها بفائدة تأخيرية بواقع (5%) سنوياً على المبلغ المقضي به في البند (1) من تاريخ طلب التحكيم في 06/04/2026 حتى تمام السداد.</li>
  <li>إلزام المحتكم ضدها بمصروفات التحكيم، بما فيها رسوم المركز وأتعاب هيئة التحكيم والخبير، وبأن تؤدي إلى المحتكمة ما سددته منها وقدره (96,400) درهم.</li>
  <li>إلزام المحتكم ضدها بأن تؤدي إلى المحتكمة مبلغ (40,000) درهم مقابل أتعاب المحاماة.</li>
  <li>رفض الطلب المقابل بغرامات التأخير في التوريد، ورفض ما عدا ذلك من طلبات.</li>
</ol>
<p>صدر هذا الحكم في دبي، مكان التحكيم، بتاريخ 10/09/2026، ووقعه أعضاء هيئة التحكيم:</p>
<table class="grid">
  <tr><th>رئيس هيئة التحكيم</th><th>عضو الهيئة</th><th>عضو الهيئة</th></tr>
  <tr><td>د. عادل منصور الحوسني</td><td>المهندس/ كريم وليد السعدي</td><td>المحامي/ ناصر عيسى البلوشي</td></tr>
  <tr><td><br><br><br></td><td><br><br><br></td><td><br><br><br></td></tr>
</table>
""",
            "marks": [
                {"id": "c10-p2-signature-presiding", "type": "signature", "color": INK, "top": 854, "left": 556,
                 "width": 150, "height": 60, "rotate": -3, "seed": 109,
                 "label_en": "Presiding arbitrator's signature"},
                {"id": "c10-p2-signature-arbitrator-2", "type": "signature", "color": BLACK_INK, "top": 854, "left": 331,
                 "width": 150, "height": 60, "rotate": 4, "seed": 113,
                 "label_en": "Co-arbitrator's signature (engineer)"},
                {"id": "c10-p2-signature-arbitrator-3", "type": "signature", "color": INK, "top": 854, "left": 97,
                 "width": 150, "height": 60, "rotate": -5, "seed": 127,
                 "label_en": "Co-arbitrator's signature (lawyer)"},
                {"id": "c10-p2-stamp-centre", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["مركز الشراع الأبيض للتحكيم", "نموذج تدريبي", "دبي"], "top": 890, "left": 321,
                 "width": 170, "height": 92, "rotate": 8, "seed": 131,
                 "label_en": "Arbitration centre stamp (training sample)",
                 "text_ar": "مركز الشراع الأبيض للتحكيم — نموذج تدريبي — دبي"},
            ],
        },
        # ------------------------------------------------------------------ page 3: the court's order
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">محاكم دبي — محكمة الاستئناف</div>
    <div class="ent-sub">طلبات المصادقة على أحكام التحكيم وتنفيذها</div>
  </div>
  <div class="meta">
    <div>الطلب رقم: 318 لسنة 2026 تحكيم</div>
    <div>تاريخ الأمر: 26/10/2026</div>
  </div>
</div>
<h1 class="title">أمر بالمصادقة على حكم تحكيم وتنفيذه</h1>
<p>إنه في يوم الاثنين الموافق 26/10/2026، وبعد الاطلاع على الطلب المقدم بتاريخ 20/10/2026 من شركة نسيم الجبل للخرسانة الجاهزة ذ.م.م ضد شركة القوس العالي للمقاولات الإنشائية ذ.م.م، وعلى أصل حكم التحكيم الصادر بتاريخ 10/09/2026 في قضية التحكيم رقم (47) لسنة 2026 لدى مركز الشراع الأبيض للتحكيم التجاري، وعلى صورة اتفاق التحكيم ومحضر إيداع الحكم؛</p>
<p>وحيث إن المادة (52) من القانون الاتحادي رقم (6) لسنة 2018 في شأن التحكيم تنص على أن: "يعتبر حكم التحكيم الصادر وفقاً لأحكام هذا القانون ملزماً للأطراف، ويحوز حجية الأمر المقضي، ويكون له ذات القوة التنفيذية كما لو كان حكماً قضائياً، إلا أنه يشترط لتنفيذه الحصول على قرار للمصادقة عليه من المحكمة"؛</p>
<p>وحيث إن الطلب قُدِّم مستوفياً المستندات التي يتطلبها البند (1) من المادة (55) من القانون ذاته، ولم يثبت للمحكمة قيام أي سبب من أسباب البطلان الواردة في المادة (53) من القانون ذاته، وكان موضوع النزاع مما يجوز التحكيم فيه، وليس في الحكم ما يخالف النظام العام والآداب العامة في الدولة؛</p>
<h2>لذلك أمرت المحكمة:</h2>
<ol>
  <li>بالمصادقة على حكم التحكيم المشار إليه، وتذييله بالصيغة التنفيذية لتنفيذه بكامل ما قضى به.</li>
  <li>بإلزام المطلوب ضدها بالرسوم والمصروفات.</li>
</ol>
<p>ويجوز التظلم من هذا الأمر أمام محكمة الاستئناف المختصة خلال (30) ثلاثين يوماً من اليوم التالي للإعلان، وفقاً للمادة (57) من القانون ذاته.</p>
<table class="sigs">
  <tr><td></td><td>القاضي/ سعيد عبيد الرميثي<br>بالندب من رئيس المحكمة</td></tr>
</table>
""",
            "marks": [
                {"id": "c10-p3-signature-judge", "type": "signature", "color": BLACK_INK, "top": 728, "left": 140,
                 "width": 170, "height": 66, "rotate": -5, "seed": 137,
                 "label_en": "Judge's signature (delegated by the Chief Justice)"},
                {"id": "c10-p3-stamp-court", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["محكمة الاستئناف", "نموذج تدريبي", "26/10/2026"], "top": 735, "left": 300, "width": 160,
                 "height": 96, "rotate": -8, "seed": 139,
                 "label_en": "Court of Appeal stamp (training sample)",
                 "text_ar": "محكمة الاستئناف — نموذج تدريبي — 26/10/2026"},
                {"id": "c10-p3-hand-execution", "type": "handwriting", "color": INK, "size": 21,
                 "text": "قُيِّد ملف التنفيذ رقم ٧٥٢ / ٢٠٢٦ تنفيذ تجاري بتاريخ ٢٨/١٠/٢٠٢٦", "top": 900, "left": 300,
                 "rotate": -3,
                 "label_en": "Execution clerk's handwritten note: execution file number and date",
                 "text_ar": "قيد ملف التنفيذ رقم 752 / 2026 تنفيذ تجاري بتاريخ 28/10/2026"},
            ],
        },
    ],
}
