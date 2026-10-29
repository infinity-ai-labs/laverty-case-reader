# -*- coding: utf-8 -*-
"""Case 13 (fictional): construction contract (muqawala) claim for the final payment and the retention.

Everything is invented: the contractor, the villa owner, the consultant, the plot and all numbers.
The contract is dated 12/01/2026, before 1 June 2026, so the 1985 Civil Transactions Law
(Federal Law No. 5 of 1985) still governs it although Federal Decree-Law No. 25 of 2025 repealed
it from that date. Every citation is valid and was read in the official texts: the muqawala
articles 872-874, 885 and 887 of the 1985 law, and Article 4(1) of the 2025 law (no retroactive
effect). Planted for the reader: the actual completion date exists only in handwriting (page 2),
and the printed retention on the payment certificate is struck through and corrected by hand (page 3).
"""
from cases import BLUE, PURPLE, INK, BLACK_INK, RED  # noqa: F401

CASE = {
    "id": "case-13",
    "slug": "construction",
    "title_en": "Construction contract (muqawala) claim: final payment and retention for a villa",
    "pages": [
        # ------------------------------------------------------------ page 1: statement of claim
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مكتب سنا الحق للمحاماة والاستشارات القانونية</div>
    <div class="ent-sub">Sana Al Haq Advocates &amp; Legal Consultants — دبي</div>
  </div>
  <div class="meta">
    <div>التاريخ: 26/10/2026</div>
    <div>المرجع: SH/CIV/2026/207</div>
  </div>
</div>
<h1 class="title">صحيفة دعوى مستحقات عقد مقاولة</h1>
<p class="center">مقدمة إلى: محكمة دبي الابتدائية — الدوائر المدنية</p>
<table class="parties">
  <tr><th>المدعية</th><td>شركة بنيان الربى للمقاولات العامة ذ.م.م، رخصة تجارية رقم 000000، دبي (المقاول).</td></tr>
  <tr><th>المدعى عليه</th><td>سلطان خليفة المهيري، مواطن، هوية رقم 784-1979-0000000-0، دبي (صاحب العمل).</td></tr>
</table>
<p><b>الوقائع:</b> بموجب عقد مقاولة بمبلغ مقطوع مؤرخ 12/01/2026 تعهدت المدعية بإنشاء فيلا للمدعى عليه في العوير الأولى بقيمة (1,480,000) درهم خلال ثمانية أشهر من استلام الموقع في 02/02/2026، بإشراف مكتب المرسام للاستشارات الهندسية، واعتُمد أمر التغيير رقم (1) بقيمة (46,500) درهم. وبعد إنجاز الأعمال أصدر الاستشاري شهادة الإنجاز في 21/09/2026 مثبتاً فيها تاريخ الإنجاز الفعلي (المرفق 2)، وقدمت ضمان الصيانة البنكي في 22/09/2026، وصدرت شهادة الدفع النهائية رقم (8) في 24/09/2026 (المرفق 3). وتسلم المدعى عليه الفيلا في 05/10/2026 بعد إنجاز الملاحظات، وامتنع عن السداد رغم إنذاره رسمياً في 12/10/2026.</p>
<h2>الأسانيد القانونية</h2>
<ol>
  <li>أُبرم العقد قبل نفاذ قانون المعاملات المدنية الصادر بالمرسوم بقانون اتحادي رقم (25) لسنة 2025 في 01/06/2026، فيحكمه القانون الاتحادي رقم (5) لسنة 1985، إذ لا يسري الأخير على ما سبقه من تصرفات وفقاً للبند (1) من المادة (4) منه.</li>
  <li>توافرت في العقد أركان المقاولة التي نصت عليها المواد من (872) إلى (874) من القانون الاتحادي رقم (5) لسنة 1985، إذ تعهدت المدعية بتقديم المادة والعمل لقاء بدل محدد وفي مدة محددة.</li>
  <li>تنص المادة (885) على أن "يلتزم صاحب العمل بدفع البدل عند تسليم المعقود عليه إلا إذا نص الاتفاق أو جرى العرف على غير ذلك"، وحدد البند (9) من العقد أجل الدفعة النهائية بـ(14) يوماً من شهادة الدفع والمحتجزات بـ(30) يوماً من شهادة الإنجاز.</li>
  <li>صدر أمر التغيير رقم (1) برضا المدعى عليه، فيُراعى بشأنه الاتفاق الجاري عملاً بالبند (2) من المادة (887) من القانون ذاته.</li>
</ol>
<h2>الطلبات</h2>
<table class="grid">
  <tr><th>م</th><th>البند</th><th>المبلغ (درهم)</th></tr>
  <tr><td>1</td><td>صافي الدفعة النهائية بموجب شهادة الدفع رقم (8)</td><td>167,850</td></tr>
  <tr><td>2</td><td>المحتجزات (10%) المستحق الإفراج عنها</td><td>152,650</td></tr>
  <tr class="total"><td></td><td>الإجمالي</td><td>320,500</td></tr>
</table>
<p>مع الفائدة القانونية (5%) سنوياً من تاريخ المطالبة حتى السداد التام، والرسوم والمصروفات وأتعاب المحاماة.</p>
<div class="sigline">وكيل المدعية — المحامي/ مازن وليد الشحي</div>
""",
            "marks": [
                {"id": "c13-p1-stamp-registry", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["قلم القيد", "نموذج تدريبي", "27/10/2026"], "top": 26, "left": 262, "width": 140,
                 "height": 80, "rotate": 6, "seed": 213,
                 "label_en": "Registry date stamp (training sample)", "text_ar": "قلم القيد — نموذج تدريبي — 27/10/2026"},
                {"id": "c13-p1-hand-hearing", "type": "handwriting", "color": INK, "size": 21,
                 "text": "حُددت جلسة ١٨/١١/٢٠٢٦", "top": 128, "left": 62, "rotate": -3,
                 "label_en": "Registry clerk's handwritten hearing date",
                 "text_ar": "حددت جلسة 18/11/2026"},
                {"id": "c13-p1-signature-lawyer", "type": "signature", "color": INK, "top": 950, "left": 405,
                 "width": 170, "height": 60, "rotate": 3, "seed": 221,
                 "label_en": "Signature of the claimant's lawyer"},
                {"id": "c13-p1-stamp-lawfirm", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["مكتب سنا الحق للمحاماة", "Sana Al Haq Advocates", "دبي — الإمارات"],
                 "top": 948, "left": 540, "width": 196, "height": 76, "rotate": -4, "seed": 223,
                 "label_en": "Law firm stamp", "text_ar": "مكتب سنا الحق للمحاماة — دبي"},
            ],
        },
        # ------------------------------------------------------------ page 2: completion certificate
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مكتب المرسام للاستشارات الهندسية</div>
    <div class="ent-sub">Al Mirsam Engineering Consultants — دبي</div>
  </div>
  <div class="meta">
    <div>التاريخ: 21/09/2026</div>
    <div>المرجع: MRS/CC/2026/031</div>
  </div>
</div>
<h1 class="title">شهادة إنجاز الأعمال (الاستلام الابتدائي)</h1>
<table class="parties">
  <tr><th>المشروع</th><td>إنشاء فيلا سكنية (طابق أرضي وملحق خدمات وسور) — القطعة رقم (000000) — العوير الأولى — دبي</td></tr>
  <tr><th>المالك</th><td>سلطان خليفة المهيري</td></tr>
  <tr><th>المقاول</th><td>شركة بنيان الربى للمقاولات العامة ذ.م.م</td></tr>
  <tr><th>العقد</th><td>عقد مقاولة بمبلغ مقطوع مؤرخ 12/01/2026 بقيمة (1,480,000) درهم — استلام الموقع: 02/02/2026 — مدة التنفيذ: ثمانية أشهر</td></tr>
</table>
<p>نشهد بصفتنا الاستشاري المشرف على المشروع بأننا أجرينا بتاريخ 17/09/2026 معاينة مشتركة للأعمال بحضور ممثل المقاول، وتبين أنها أُنجزت وفقاً للمخططات والمواصفات المعتمدة وأصبحت صالحة للاستعمال في الغرض المخصص لها، فيما عدا الملاحظات البسيطة المدونة أدناه التي لا تحول دون الاستلام، ويلتزم المقاول بإنجازها في المدة المحددة لها.</p>
<p>تبدأ فترة الصيانة ومدتها (12) شهراً من تاريخ الإنجاز الفعلي المبين أدناه، ويظل المقاول مسؤولاً خلالها عن إصلاح ما يظهر من عيوب وفقاً لشروط العقد.</p>
<p><b>تاريخ الإنجاز الفعلي:</b></p>
<p><b>قائمة الملاحظات (النواقص):</b></p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<table class="sigs">
  <tr><td>المهندس المشرف — كريم فؤاد الحلبي</td><td>ممثل المقاول — م. أنس طارق الخطيب</td></tr>
</table>
""",
            "marks": [
                {"id": "c13-p2-hand-completion-date", "type": "handwriting", "color": INK, "size": 23,
                 "text": "١٤/٩/٢٠٢٦", "top": 553, "left": 495, "rotate": -3,
                 "label_en": "Actual completion date, handwritten by the supervising engineer (not printed anywhere)",
                 "text_ar": "14/9/2026"},
                {"id": "c13-p2-hand-snags", "type": "handwriting", "color": INK, "size": 19, "width": 600,
                 "text": "١- تسرب مياه بسيط أسفل مغسلة حمام الضيوف ٢- إعادة دهان أجزاء من السور الخارجي ٣- تركيب مقابض خزائن المطبخ — تُنجز خلال ١٤ يوماً من تاريخه",
                 "top": 640, "left": 110, "rotate": -1,
                 "label_en": "Handwritten snag list (three items, to be completed within 14 days)",
                 "text_ar": "1- تسرب مياه بسيط أسفل مغسلة حمام الضيوف 2- إعادة دهان أجزاء من السور الخارجي 3- تركيب مقابض خزائن المطبخ — تنجز خلال 14 يوماً من تاريخه"},
                {"id": "c13-p2-signature-engineer", "type": "signature", "color": INK, "top": 820, "left": 470,
                 "width": 170, "height": 64, "rotate": -4, "seed": 231,
                 "label_en": "Supervising engineer's signature"},
                {"id": "c13-p2-stamp-consultant", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["مكتب المرسام للاستشارات الهندسية", "Al Mirsam Engineering Consultants", "دبي"],
                 "top": 880, "left": 420, "width": 250, "height": 82, "rotate": 5, "seed": 233,
                 "label_en": "Consultant's stamp", "text_ar": "مكتب المرسام للاستشارات الهندسية — دبي"},
                {"id": "c13-p2-signature-contractor", "type": "signature", "color": BLACK_INK, "top": 830, "left": 130,
                 "width": 150, "height": 58, "rotate": 3, "seed": 239,
                 "label_en": "Contractor's representative's signature"},
            ],
        },
        # ------------------------------------------------------------ page 3: final payment certificate
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مكتب المرسام للاستشارات الهندسية</div>
    <div class="ent-sub">Al Mirsam Engineering Consultants — دبي</div>
  </div>
  <div class="meta">
    <div>التاريخ: 24/09/2026</div>
    <div>المرجع: MRS/PC/2026/08</div>
  </div>
</div>
<h1 class="title">شهادة الدفع النهائية رقم (8)</h1>
<p class="center">المشروع: فيلا سكنية — القطعة رقم (000000) — العوير الأولى — دبي</p>
<p>المالك: سلطان خليفة المهيري — المقاول: شركة بنيان الربى للمقاولات العامة ذ.م.م — عقد المقاولة المؤرخ 12/01/2026.</p>
<table class="grid">
  <tr><th>م</th><th>البيان</th><th>المبلغ (درهم)</th></tr>
  <tr><td>1</td><td>قيمة العقد الأصلية (مبلغ مقطوع)</td><td>1,480,000</td></tr>
  <tr><td>2</td><td>أمر التغيير رقم (1) المعتمد في 14/04/2026 (مظلة مواقف وأعمال تبليط إضافية)</td><td>46,500</td></tr>
  <tr><td>3</td><td>إجمالي قيمة الأعمال المنجزة (100%)</td><td>1,526,500</td></tr>
  <tr><td>4</td><td>يُخصم: المحتجزات (10%)</td><td><span class="struck">125,650</span></td></tr>
  <tr><td>5</td><td>صافي قيمة الأعمال بعد خصم المحتجزات</td><td>1,373,850</td></tr>
  <tr><td>6</td><td>يُخصم: الدفعات المسددة بموجب الشهادات من (1) إلى (7)</td><td>1,206,000</td></tr>
  <tr class="total"><td></td><td>صافي المستحق للمقاول بموجب هذه الشهادة (الدفعة النهائية)</td><td>167,850</td></tr>
</table>
<p>أُعدت هذه الشهادة على أساس الحساب الختامي للأعمال المنجزة بعد إصدار شهادة الإنجاز، وبعد مراجعة الكميات المنفذة على الطبيعة.</p>
<p>تُسدد الدفعة النهائية خلال (14) يوماً من تاريخ هذه الشهادة وفقاً للبند (9/3) من العقد، ويُفرج عن المحتجزات المبينة في البند (4) أعلاه خلال (30) يوماً من تاريخ شهادة الإنجاز المؤرخة 21/09/2026، مقابل ضمان الصيانة البنكي وفقاً للبند (9/4) من العقد.</p>
<table class="sigs">
  <tr><td>مهندسة الكميات — نادية سمير عوض</td><td>المهندس المشرف — كريم فؤاد الحلبي</td></tr>
</table>
""",
            "marks": [
                {"id": "c13-p3-hand-retention-correction", "type": "handwriting", "color": RED, "size": 23,
                 "text": "١٥٢,٦٥٠ — ك.ح", "top": 376, "left": 176, "rotate": -4,
                 "label_en": "Handwritten correction of the retention to 152,650, initialled by the supervising engineer",
                 "text_ar": "152,650 — ك.ح"},
                {"id": "c13-p3-signature-qs", "type": "signature", "color": INK, "top": 704, "left": 480,
                 "width": 160, "height": 60, "rotate": 4, "seed": 241,
                 "label_en": "Quantity surveyor's signature"},
                {"id": "c13-p3-signature-engineer", "type": "signature", "color": INK, "top": 704, "left": 140,
                 "width": 170, "height": 64, "rotate": -3, "seed": 243,
                 "label_en": "Supervising engineer's signature"},
                {"id": "c13-p3-stamp-consultant", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["مكتب المرسام للاستشارات الهندسية", "Al Mirsam Engineering Consultants", "دبي"],
                 "top": 744, "left": 200, "width": 250, "height": 82, "rotate": -6, "seed": 247,
                 "label_en": "Consultant's stamp", "text_ar": "مكتب المرسام للاستشارات الهندسية — دبي"},
            ],
        },
    ],
}
