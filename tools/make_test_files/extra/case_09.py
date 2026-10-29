# -*- coding: utf-8 -*-
"""Case 09 (fictional): consumer claim over a new car with a repeated gearbox fault under warranty.

Everything here is fictional: the buyer, the dealer, the car make and model, the numbers and the
events. The laws cited are real UAE laws, checked against the official texts on 29 Oct 2026, except
one deliberately invalid citation: Article 45 of the Consumer Protection Law, which has 38 articles.
The car was bought and delivered on 16 Jun 2026, after 1 June 2026, so the 2025 Civil Transactions
Law governs the sale. The date of the second repair appears only in the technician's handwriting on the job card.
"""
from cases import BLUE, PURPLE, INK, BLACK_INK, RED  # noqa: F401  (RED kept for parity with cases.py)

CASE = {
    "id": "case-09",
    "slug": "consumer-car",
    "title_en": "Consumer claim: new car with a repeated gearbox fault under warranty",
    "pages": [
        # ---------------------------------------------------------------- page 1: statement of claim
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مكتب إبراهيم الحوسني للمحاماة</div>
  </div>
  <div class="meta">
    <div>التاريخ: 21/10/2026 — المرجع: IH/CNS/2026/27</div>
  </div>
</div>
<h1 class="title">صحيفة دعوى</h1>
<p class="center">مقدمة إلى: محكمة الشارقة الاتحادية الابتدائية — الدائرة التجارية الجزئية</p>
<table class="parties">
  <tr><th>المدعية</th><td>مريم خالد الزعابي، هوية رقم 784-1991-0000000-0، الشارقة.</td></tr>
  <tr><th>المدعى عليها</th><td>شركة مرفأ النجوم للسيارات ذ.م.م، موزع سيارات ألكوريا المعتمد، رخصة رقم 000000.</td></tr>
</table>
<h2>الوقائع</h2>
<ol>
  <li>اشترت المدعية من المدعى عليها بتاريخ 16/06/2026 سيارة ألكوريا سراب 2.0 توربو موديل 2026 (رقم الهيكل 00000000000000000) بثمن (136,500) درهم مع ضمان (3) سنوات أو (100,000) كم، وتسلمتها في اليوم ذاته.</li>
  <li>ظهر بناقل الحركة عطل (ارتجاج وتأخر في التبديل)، فأُدخلت السيارة ورشة المدعى عليها ببطاقة العمل رقم JC-2026-04417 المرفقة، وأثبت الفني فيها أنه عيب مصنعي.</li>
  <li>وتكرر العطل ذاته فأعيد إصلاحه ثانيةً على البطاقة ذاتها، ثم تعطل للمرة الثالثة بتاريخ 06/10/2026.</li>
  <li>ورفضت المدعى عليها في 13/10/2026 طلب المدعية المؤرخ 08/10/2026 الاستبدال أو الرد خلال سبعة أيام.</li>
</ol>
<h2>الأسانيد القانونية</h2>
<ol>
  <li>ألزمت المادة (10) من القانون الاتحادي رقم (15) لسنة 2020 بشأن حماية المستهلك المزود بتنفيذ جميع الضمانات واستبدال السلعة أو رد قيمتها النقدية، ونصت المادة (13) منه على أنه: "يلتزم المزود إذا تكرر في السلعة الخلل ذاته ثلاث (3) مرات خلال العام الأول من تاريخ استلام المستهلك لها" بأن يستبدل بها أخرى جديدة أو يستردها ويرد قيمتها.</li>
  <li>وتلزم المادة (16) من القانون ذاته الموزع بتوفير سلعة مماثلة دون مقابل إذا جاوز تنفيذ الضمان سبعة أيام، وللمستهلك طلب التعويض وفقاً للمادة (24) منه، ويقع على المزود عبء إثبات سوء الاستخدام وفقاً للمادة (45) من قانون حماية المستهلك.</li>
  <li>وإذ لم تُصلح المدعى عليها العيب خلال مدة الضمان، فللمدعية طلب فسخ العقد والتعويض وفقاً للبند (2) من المادة (502) من المرسوم بقانون اتحادي رقم (25) لسنة 2025 بإصدار قانون المعاملات المدنية.</li>
</ol>
<h2>الطلبات</h2>
<ol>
  <li>أصلياً: إلزام المدعى عليها باستبدال السيارة بأخرى جديدة من ذات النوع والمواصفات دون أي تكلفة.</li>
  <li>احتياطياً: فسخ عقد البيع وإلزام المدعى عليها باسترداد السيارة ورد ثمنها البالغ (136,500) درهم.</li>
  <li>وفي الحالتين: إلزامها بأداء (7,920) درهم أجرة سيارة بديلة لم توفرها (36 يوماً × 220 درهم)، و(25,000) درهم تعويضاً عن الأضرار المادية والأدبية، بإجمالي (32,920) درهم، مع الرسوم والمصروفات وأتعاب المحاماة.</li>
</ol>
<div class="sigline">وكيل المدعية — المحامي/ إبراهيم يعقوب الحوسني</div>
""",
            "marks": [
                {"id": "c9-p1-stamp-registry", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["قلم القيد", "نموذج تدريبي", "21/10/2026"], "top": 104, "left": 50, "width": 156,
                 "height": 66, "rotate": 7, "seed": 97,
                 "label_en": "Registry date stamp (training sample)", "text_ar": "قلم القيد — نموذج تدريبي — 21/10/2026"},
                {"id": "c9-p1-signature-lawyer", "type": "signature", "color": INK, "top": 990, "left": 118,
                 "width": 170, "height": 60, "rotate": -3, "seed": 101,
                 "label_en": "Signature of the claimant's lawyer"},
                {"id": "c9-p1-stamp-lawfirm", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["مكتب إبراهيم الحوسني للمحاماة", "Ibrahim Al Hosani Advocates", "الشارقة — الإمارات"],
                 "top": 950, "left": 470, "width": 226, "height": 80, "rotate": -5, "seed": 103,
                 "label_en": "Law firm stamp", "text_ar": "مكتب إبراهيم الحوسني للمحاماة — الشارقة"},
            ],
        },
        # ---------------------------------------------------------------- page 2: workshop job card
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">شركة مرفأ النجوم للسيارات ذ.م.م</div>
    <div class="ent-sub">الموزع المعتمد لسيارات ألكوريا — مركز الخدمة والصيانة</div>
    <div class="ent-sub">الشارقة — المنطقة الصناعية الثانية — هاتف 060000000</div>
  </div>
  <div class="meta">
    <div>Job Card / Repair Order</div>
    <div>النموذج SV-01</div>
  </div>
</div>
<h1 class="title">بطاقة عمل — أمر إصلاح</h1>
<table class="grid">
  <tr><th>رقم البطاقة</th><td>JC-2026-04417</td><th>تاريخ الاستلام</th><td>28/07/2026 — 09:40</td></tr>
  <tr><th>اسم العميل</th><td>مريم خالد الزعابي</td><th>الهاتف</th><td>0500000000</td></tr>
  <tr><th>المركبة</th><td>ألكوريا سراب 2.0 توربو — 2026</td><th>رقم اللوحة</th><td>الشارقة / 00000</td></tr>
  <tr><th>رقم الهيكل</th><td>00000000000000000</td><th>قراءة العداد</th><td>3,184 كم</td></tr>
  <tr><th>الضمان</th><td>سارٍ — 3 سنوات / 100,000 كم</td><th>الفني المسؤول</th><td>وائل فهمي عبدالقادر</td></tr>
</table>
<p><b>شكوى العميل:</b> ارتجاج عند الانطلاق، وتأخر في التبديل من السرعة الثانية إلى الثالثة، وظهور تنبيه "عطل في ناقل الحركة" على لوحة العدادات.</p>
<table class="grid">
  <tr><th>م</th><th>العمل المنفذ</th><th>رمز العمل</th><th>التغطية</th></tr>
  <tr><td>1</td><td>فحص ناقل الحركة بجهاز التشخيص وقراءة رموز الأعطال</td><td>D-100</td><td>ضمان</td></tr>
  <tr><td>2</td><td>تحديث برمجة وحدة التحكم في ناقل الحركة</td><td>S-210</td><td>ضمان</td></tr>
  <tr><td>3</td><td>استبدال مجموعة الصمامات وتغيير زيت ناقل الحركة</td><td>T-355</td><td>ضمان</td></tr>
</table>
<p>المبلغ المستحق على العميل: لا شيء (مشمول بالضمان). تاريخ تسليم المركبة للعميل: 08/08/2026.</p>
<table class="grid">
  <tr><th>نتيجة الفحص وملاحظات الفني</th></tr>
  <tr><td><br><br><br></td></tr>
</table>
<table class="grid">
  <tr><th>إعادة الإصلاح (عودة المركبة بالشكوى ذاتها): التاريخ والإجراء</th></tr>
  <tr><td><br><br></td></tr>
</table>
<table class="sigs">
  <tr><td>توقيع الفني</td><td>ختم مركز الخدمة</td></tr>
</table>
""",
            "marks": [
                {"id": "c9-p2-hand-findings", "type": "handwriting", "color": INK, "size": 20,
                 "text": "بالفحص: انزلاق في قابض السرعة الثالثة وارتفاع حرارة زيت القير — عيب مصنعي — تم الإصلاح",
                 "top": 684, "left": 80, "rotate": -1.5, "width": 620,
                 "label_en": "Technician's handwritten findings: third-gear clutch slipping, overheating gearbox oil; manufacturing defect",
                 "text_ar": "بالفحص: انزلاق في قابض السرعة الثالثة وارتفاع حرارة زيت القير — عيب مصنعي — تم الإصلاح"},
                {"id": "c9-p2-hand-second-repair", "type": "handwriting", "color": INK, "size": 20,
                 "text": "عادت السيارة بالعطل ذاته — أعيد الإصلاح بتاريخ ٢٤/٨/٢٠٢٦ — استبدال وحدة التحكم",
                 "top": 808, "left": 90, "rotate": -1, "width": 610,
                 "label_en": "Technician's handwritten note of the second repair, with its date",
                 "text_ar": "عادت السيارة بالعطل ذاته — أعيد الإصلاح بتاريخ 24/8/2026 — استبدال وحدة التحكم"},
                {"id": "c9-p2-signature-technician", "type": "signature", "color": BLACK_INK, "top": 932, "left": 486,
                 "width": 160, "height": 58, "rotate": -4, "seed": 107,
                 "label_en": "Technician's signature"},
                {"id": "c9-p2-stamp-dealer", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["مرفأ النجوم للسيارات ذ.م.م", "مركز الخدمة — الشارقة", "Marfa Al Nujoom Motors"],
                 "top": 940, "left": 118, "width": 220, "height": 80, "rotate": 6, "seed": 109,
                 "label_en": "Dealer's service-centre stamp", "text_ar": "مرفأ النجوم للسيارات ذ.م.م — مركز الخدمة — الشارقة"},
            ],
        },
    ],
}
