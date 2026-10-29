# -*- coding: utf-8 -*-
"""Three made-up Arabic case files for testing the LAVERTY Case Reader.

Everything here is fictional: the people, companies, case numbers, ID and licence numbers,
addresses and events. Every page carries a footer saying so. The laws cited are real UAE laws,
and every valid citation was checked against the official texts on 29 Oct 2026. Two citations
are deliberately wrong (an article number the law does not have), so the reader's citation
check has something to catch; the answer key marks them as invalid.

Positions of stamps, signatures and handwriting are in CSS pixels on a 794 x 1123 page (A4).
"""

FOOTER = "وثيقة خيالية لأغراض الاختبار فقط — لا تمثل قضية حقيقية · Fictional test document, not a real case"

BLUE = "#23379a"
PURPLE = "#5b2a86"
INK = "#14287a"
BLACK_INK = "#1d1d28"
RED = "#a12a2a"

CASES = [
    # ------------------------------------------------------------------ case 01: labour
    {
        "id": "case-01",
        "slug": "labour",
        "title_en": "Labour claim: unpaid wages, gratuity and unlawful dismissal",
        "pages": [
            {
                "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مكتب نجم السدرة للمحاماة والاستشارات القانونية</div>
    <div class="ent-sub">Najm Al Sidra Advocates &amp; Legal Consultants</div>
    <div class="ent-sub">دبي — ص.ب: 00000</div>
  </div>
  <div class="meta">
    <div>التاريخ: 05/10/2026</div>
    <div>المرجع: NS/LAB/2026/118</div>
  </div>
</div>
<h1 class="title">صحيفة دعوى عمالية</h1>
<p class="center">مقدمة إلى: المحكمة العمالية الابتدائية — إمارة دبي</p>
<table class="parties">
  <tr><th>المدعي</th><td>سامر خليل الحداد، أردني الجنسية، هوية رقم 784-1987-0000000-0، يعمل لدى المدعى عليها بوظيفة محاسب أول. وكيله: المحامي/ يوسف عبدالله المرزوقي.</td></tr>
  <tr><th>المدعى عليها</th><td>شركة نجمة الخليج للمقاولات العامة ذ.م.م، رخصة تجارية رقم 000000، العنوان: دبي — منطقة القوز الصناعية الثالثة.</td></tr>
  <tr><th>الموضوع</th><td>المطالبة بالأجور المتأخرة وبدل الإنذار ومكافأة نهاية الخدمة وبدل الإجازة السنوية والتعويض عن الإنهاء غير المشروع.</td></tr>
</table>
<h2>الوقائع</h2>
<ol>
  <li>التحق المدعي بالعمل لدى المدعى عليها بتاريخ 01/03/2019 بموجب عقد عمل غير محدد المدة بوظيفة محاسب أول، براتب إجمالي قدره (18,000) درهم شهرياً، منه أجر أساسي قدره (12,000) درهم.</li>
  <li>توقفت المدعى عليها عن سداد أجور المدعي اعتباراً من شهر يونيو 2026، فتقدم بشكوى إلى وزارة الموارد البشرية والتوطين بتاريخ 04/08/2026 قُيِّدت برقم (MO-2026-58213).</li>
  <li>بتاريخ 15/08/2026، أي بعد أحد عشر يوماً من تقديم الشكوى، أصدرت المدعى عليها كتاباً بإنهاء خدمة المدعي اعتباراً من التاريخ ذاته، دون إنذار مسبق ودون سداد مستحقاته.</li>
  <li>تعذرت التسوية الودية لدى الوزارة، فأحالت النزاع إلى المحكمة بتاريخ 22/09/2026 لتجاوز قيمة المطالبة مبلغ (50,000) درهم، وذلك وفقاً للمادة (54) من المرسوم بقانون اتحادي رقم (33) لسنة 2021 بشأن تنظيم علاقات العمل.</li>
</ol>
<p class="cont">يتبع في الصفحة التالية ...</p>
""",
                "marks": [
                    {"id": "c1-p1-stamp-registry", "type": "stamp", "kind": "oval", "color": PURPLE,
                     "lines": ["قلم القيد", "نموذج تدريبي", "06/10/2026"], "top": 150, "left": 52, "width": 150,
                     "height": 92, "rotate": -11, "seed": 3,
                     "label_en": "Registry date stamp (training sample)", "text_ar": "قلم القيد — نموذج تدريبي — 06/10/2026"},
                    {"id": "c1-p1-hand-registration", "type": "handwriting", "color": INK, "size": 21,
                     "text": "قُيِّدت برقم ١٢٣٤ / ٢٠٢٦ عمالي جزئي", "top": 800, "left": 70, "rotate": -3,
                     "label_en": "Registry clerk's handwritten case number",
                     "text_ar": "قيدت برقم 1234 / 2026 عمالي جزئي"},
                ],
            },
            {
                "html": """
<h2>الأسانيد القانونية</h2>
<ol>
  <li>إن إنهاء خدمة المدعي جاء بسبب تقدمه بشكوى جدية إلى الوزارة، مما يجعله إنهاءً غير مشروع وفقاً للبند (1) من المادة (47) من المرسوم بقانون المشار إليه، ويستحق عنه تعويضاً لا يجاوز أجر ثلاثة أشهر وفقاً للبند (2) من المادة ذاتها.</li>
  <li>لم تلتزم المدعى عليها بمدة الإنذار المنصوص عليها في المادة (43)، والتي لا تقل عن ثلاثين يوماً، فيستحق المدعي بدل الإنذار عنها.</li>
  <li>يستحق المدعي مكافأة نهاية الخدمة وفقاً للمادة (51)، بواقع أجر (21) يوماً عن كل سنة من السنوات الخمس الأولى، وأجر (30) يوماً عن كل سنة مما زاد على ذلك، تحسب على أساس الأجر الأساسي.</li>
  <li>ألزمت المادة (53) صاحب العمل بسداد أجور العامل وجميع مستحقاته خلال (14) يوماً من تاريخ انتهاء العقد، وهو ما لم تلتزم به المدعى عليها.</li>
  <li>كما يطالب المدعي بتعويض عن التأخير في سداد الأجور استناداً إلى المادة (145) من المرسوم بقانون ذاته.</li>
  <li>تُعفى الدعوى من الرسوم القضائية عملاً بالمادة (55) من المرسوم بقانون ذاته.</li>
</ol>
<h2>الطلبات</h2>
<table class="grid">
  <tr><th>م</th><th>البند</th><th>المبلغ (درهم)</th></tr>
  <tr><td>1</td><td>الأجور المتأخرة عن شهري يونيو ويوليو 2026 والفترة من 01/08/2026 حتى 15/08/2026</td><td>45,000</td></tr>
  <tr><td>2</td><td>بدل الإنذار (30 يوماً)</td><td>18,000</td></tr>
  <tr><td>3</td><td>مكافأة نهاية الخدمة</td><td>71,460</td></tr>
  <tr><td>4</td><td>بدل الإجازة السنوية غير المستخدمة (20 يوماً)</td><td>8,000</td></tr>
  <tr><td>5</td><td>التعويض عن الإنهاء غير المشروع</td><td>54,000</td></tr>
  <tr class="total"><td></td><td>الإجمالي</td><td>196,460</td></tr>
</table>
<p>مع إلزام المدعى عليها بتسليم المدعي شهادة الخبرة، وبالرسوم والمصروفات ومقابل أتعاب المحاماة.</p>
<div class="sigline">وكيل المدعي — المحامي/ يوسف عبدالله المرزوقي</div>
""",
                "marks": [
                    {"id": "c1-p2-signature-lawyer", "type": "signature", "color": INK, "top": 745, "left": 110,
                     "width": 190, "height": 74, "rotate": -5, "seed": 11,
                     "label_en": "Signature of the claimant's lawyer"},
                    {"id": "c1-p2-stamp-lawfirm", "type": "stamp", "kind": "rect", "color": BLUE,
                     "lines": ["مكتب نجم السدرة للمحاماة", "Najm Al Sidra Advocates", "دبي — الإمارات"],
                     "top": 760, "left": 300, "width": 230, "height": 96, "rotate": 7, "seed": 5,
                     "label_en": "Law firm stamp", "text_ar": "مكتب نجم السدرة للمحاماة — دبي"},
                ],
            },
            {
                "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">محضر جلسة</div>
    <div class="ent-sub">الدائرة العمالية الثالثة</div>
  </div>
  <div class="meta">
    <div>الدعوى رقم: 1234 لسنة 2026 عمالي جزئي</div>
    <div>تاريخ الجلسة: 27/10/2026</div>
  </div>
</div>
<p>إنه في يوم الثلاثاء الموافق 27/10/2026، انعقدت الجلسة علناً برئاسة القاضي/ خالد سالم النعيمي، وبحضور أمين السر/ مريم أحمد الشامسي.</p>
<p>حضر وكيل المدعي المحامي/ يوسف عبدالله المرزوقي، وحضرت المحامية/ هند سعيد الكعبي وكيلةً عن المدعى عليها، وقدمت سند وكالتها.</p>
<p>طلبت وكيلة المدعى عليها أجلاً للاطلاع والرد على صحيفة الدعوى.</p>
<h2>قرار المحكمة</h2>
<p>قررت المحكمة تأجيل الدعوى لجلسة 17/11/2026 لرد المدعى عليها، على أن تقدم مذكرة ردها مع المستندات في موعد أقصاه 10/11/2026، وكلفت المدعى عليها بتقديم أصل عقد العمل وكشوف رواتب المدعي عن الفترة من يناير إلى أغسطس 2026.</p>
<table class="sigs">
  <tr><td>أمين السر</td><td>رئيس الدائرة</td></tr>
</table>
""",
                "marks": [
                    {"id": "c1-p3-signature-clerk", "type": "signature", "color": BLACK_INK, "top": 440, "left": 480,
                     "width": 160, "height": 64, "rotate": 3, "seed": 23, "label_en": "Court clerk's signature"},
                    {"id": "c1-p3-signature-judge", "type": "signature", "color": BLACK_INK, "top": 440, "left": 140,
                     "width": 170, "height": 66, "rotate": -6, "seed": 31, "label_en": "Presiding judge's signature"},
                    {"id": "c1-p3-stamp-sessions", "type": "stamp", "kind": "oval", "color": PURPLE,
                     "lines": ["قلم الجلسات", "نموذج تدريبي", "27/10/2026"], "top": 500, "left": 300, "width": 160,
                     "height": 96, "rotate": 9, "seed": 8,
                     "label_en": "Hearings desk stamp (training sample)", "text_ar": "قلم الجلسات — نموذج تدريبي — 27/10/2026"},
                    {"id": "c1-p3-hand-lawyer-note", "type": "handwriting", "color": INK, "size": 22,
                     "text": "متابعة: مذكرة رد الشركة بتاريخ ١٠/١١ — الجلسة القادمة ١٧/١١", "top": 660, "left": 150,
                     "rotate": -3, "label_en": "Lawyer's handwritten follow-up note",
                     "text_ar": "متابعة: مذكرة رد الشركة بتاريخ 10/11 — الجلسة القادمة 17/11"},
                ],
            },
        ],
    },
    # ------------------------------------------------------------------ case 02: commercial
    {
        "id": "case-02",
        "slug": "commercial",
        "title_en": "Commercial claim: unpaid supply invoices and a returned cheque",
        "pages": [
            {
                "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">شركة الأفق الأزرق لتوريد مواد البناء ذ.م.م</div>
    <div class="ent-sub">Blue Horizon Building Materials Supply LLC</div>
    <div class="ent-sub">دبي — ص.ب: 00000 — رخصة تجارية رقم 000000</div>
  </div>
  <div class="meta">
    <div>التاريخ: 01/09/2026</div>
    <div>المرجع: BH/FIN/2026/77</div>
  </div>
</div>
<h1 class="title">إنذار رسمي بالوفاء</h1>
<p>إلى: مؤسسة الصقر الذهبي للمقاولات (مؤسسة فردية) — المالك: راشد حمد الفلاسي — دبي.</p>
<p><b>الموضوع: إنذار رسمي بسداد مبلغ (386,500) درهم.</b></p>
<p>بالإشارة إلى اتفاقية التوريد المؤرخة 10/01/2026 والمبرمة بيننا، فقد قمنا بتوريد مواد بناء (حديد تسليح وأسمنت) إلى مشروعكم الكائن في منطقة الخوانيج بموجب الفواتير المبينة أدناه، وتسلمتموها كاملة دون أي تحفظ:</p>
<table class="grid">
  <tr><th>رقم الفاتورة</th><th>التاريخ</th><th>المبلغ (درهم)</th><th>تاريخ الاستحقاق</th></tr>
  <tr><td>INV-2026-114</td><td>15/03/2026</td><td>142,000</td><td>14/04/2026</td></tr>
  <tr><td>INV-2026-131</td><td>20/04/2026</td><td>128,500</td><td>20/05/2026</td></tr>
  <tr><td>INV-2026-147</td><td>28/05/2026</td><td>236,000</td><td>27/06/2026</td></tr>
  <tr class="total"><td>الإجمالي</td><td></td><td>506,500</td><td></td></tr>
</table>
<p>وقد سددتم مبلغ (120,000) درهم بتحويل بنكي بتاريخ 10/05/2026، أما الشيك رقم (004512) بمبلغ (150,000) درهم المؤرخ 30/06/2026 فقد ارتد دون صرف بتاريخ 02/07/2026 لعدم كفاية الرصيد، فيكون المبلغ المستحق (386,500) درهم.</p>
<p>لذلك ننذركم بسداد المبلغ المستحق خلال (15) خمسة عشر يوماً من تاريخ استلامكم هذا الإنذار، وإلا سنضطر إلى اتخاذ الإجراءات القضائية للمطالبة به مع الفائدة التأخيرية المتفق عليها بنسبة (6%) سنوياً وفقاً للبند (9) من الاتفاقية، والمصروفات.</p>
<p>يوجَّه هذا الإنذار عن طريق الكاتب العدل وفقاً للمادة (81) من المرسوم بقانون اتحادي رقم (50) لسنة 2022 بإصدار قانون المعاملات التجارية.</p>
<div class="sigline">المدير العام — طارق ماهر السويدي</div>
""",
                "marks": [
                    {"id": "c2-p1-signature-gm", "type": "signature", "color": INK, "top": 750, "left": 110,
                     "width": 180, "height": 70, "rotate": -3, "seed": 41, "label_en": "General manager's signature"},
                    {"id": "c2-p1-stamp-company", "type": "stamp", "kind": "rect", "color": BLUE,
                     "lines": ["الأفق الأزرق لتوريد مواد البناء", "Blue Horizon Building Materials", "دبي — ذ.م.م"],
                     "top": 765, "left": 300, "width": 240, "height": 98, "rotate": -6, "seed": 12,
                     "label_en": "Claimant company stamp", "text_ar": "الأفق الأزرق لتوريد مواد البناء — دبي"},
                    {"id": "c2-p1-stamp-notary", "type": "stamp", "kind": "oval", "color": PURPLE,
                     "lines": ["الكاتب العدل", "نموذج تدريبي", "01/09/2026"], "top": 155, "left": 60, "width": 150,
                     "height": 92, "rotate": 12, "seed": 14,
                     "label_en": "Notary stamp (training sample)", "text_ar": "الكاتب العدل — نموذج تدريبي — 01/09/2026"},
                    {"id": "c2-p1-hand-service", "type": "handwriting", "color": INK, "size": 21,
                     "text": "سُلِّم للمنذَر إليه بتاريخ ٣/٩/٢٠٢٦", "top": 885, "left": 420, "rotate": -5,
                     "label_en": "Handwritten note: notice served on the debtor",
                     "text_ar": "سلم للمنذر إليه بتاريخ 3/9/2026"},
                ],
            },
            {
                "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مكتب الزرعوني للمحاماة</div>
    <div class="ent-sub">Al Zarouni Advocates</div>
  </div>
  <div class="meta">
    <div>التاريخ: 05/10/2026</div>
  </div>
</div>
<h1 class="title">صحيفة دعوى تجارية</h1>
<p class="center">مقدمة إلى: محكمة دبي الابتدائية — الدوائر التجارية</p>
<table class="parties">
  <tr><th>المدعية</th><td>شركة الأفق الأزرق لتوريد مواد البناء ذ.م.م، ويمثلها المحامي/ عمر فاروق الزرعوني.</td></tr>
  <tr><th>المدعى عليها</th><td>مؤسسة الصقر الذهبي للمقاولات (مؤسسة فردية)، ومالكها راشد حمد الفلاسي.</td></tr>
</table>
<h2>الوقائع</h2>
<p>وردت المدعية إلى المدعى عليها مواد بناء بموجب اتفاقية التوريد المؤرخة 10/01/2026 والفواتير أرقام INV-2026-114 وINV-2026-131 وINV-2026-147 بإجمالي (506,500) درهم، سددت منها المدعى عليها (120,000) درهم، وارتد شيكها رقم (004512) بمبلغ (150,000) درهم. ورغم إنذارها رسمياً بتاريخ 01/09/2026 واستلامها الإنذار بتاريخ 03/09/2026، لم تقم بالسداد حتى تاريخه.</p>
<h2>الأسانيد</h2>
<ol>
  <li>تنص المادة (73) من قانون المعاملات التجارية الصادر بالمرسوم بقانون اتحادي رقم (50) لسنة 2022 على أنه: "إذا تضمن العقد اتفاقاً على سعر الفائدة، وتأخر المدين في الوفاء، احتسبت الفائدة التأخيرية على أساس السعر المتفق عليه حتى تمام السداد"، وقد اتفق الطرفان في البند (9) على فائدة تأخيرية بنسبة (6%) سنوياً.</li>
  <li>لا تطالب المدعية بفائدة مركبة، التزاماً بالمادة (88) من القانون ذاته.</li>
  <li>تستحق المدعية التعويض عن الشيك المرتجع وفقاً للمادة (712) من القانون ذاته.</li>
</ol>
<h2>الطلبات</h2>
<ol>
  <li>إلزام المدعى عليها بأن تؤدي للمدعية مبلغ (386,500) درهم.</li>
  <li>الفائدة التأخيرية بواقع (6%) سنوياً من تاريخ استحقاق كل فاتورة وحتى السداد التام.</li>
  <li>إلزام المدعى عليها بالرسوم والمصروفات ومقابل أتعاب المحاماة.</li>
</ol>
<div class="sigline">وكيل المدعية — المحامي/ عمر فاروق الزرعوني</div>
""",
                "marks": [
                    {"id": "c2-p2-signature-lawyer", "type": "signature", "color": INK, "top": 845, "left": 120,
                     "width": 180, "height": 70, "rotate": 4, "seed": 53, "label_en": "Signature of the claimant's lawyer"},
                    {"id": "c2-p2-stamp-registry", "type": "stamp", "kind": "oval", "color": PURPLE,
                     "lines": ["قلم القيد", "نموذج تدريبي", "06/10/2026"], "top": 128, "left": 46, "width": 146,
                     "height": 90, "rotate": -8, "seed": 19,
                     "label_en": "Registry date stamp (training sample)", "text_ar": "قلم القيد — نموذج تدريبي — 06/10/2026"},
                    {"id": "c2-p2-hand-hearing", "type": "handwriting", "color": INK, "size": 21,
                     "text": "حُددت جلسة ٢٤/١١/٢٠٢٦ أمام الدائرة التجارية الكلية الثانية", "top": 960, "left": 32,
                     "rotate": -2, "width": 370,
                     "label_en": "Registry clerk's handwritten hearing date",
                     "text_ar": "حددت جلسة 24/11/2026 أمام الدائرة التجارية الكلية الثانية"},
                ],
            },
            {
                "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">شركة الأفق الأزرق لتوريد مواد البناء ذ.م.م</div>
    <div class="ent-sub">قسم الحسابات</div>
  </div>
  <div class="meta">
    <div>التاريخ: 30/09/2026</div>
  </div>
</div>
<h1 class="title">كشف حساب العميل</h1>
<p class="center">العميل: مؤسسة الصقر الذهبي للمقاولات — حتى تاريخ 30/09/2026</p>
<table class="grid">
  <tr><th>التاريخ</th><th>البيان</th><th>مدين (درهم)</th><th>دائن (درهم)</th></tr>
  <tr><td>15/03/2026</td><td>فاتورة INV-2026-114</td><td>142,000</td><td>—</td></tr>
  <tr><td>20/04/2026</td><td>فاتورة INV-2026-131</td><td>128,500</td><td>—</td></tr>
  <tr><td>10/05/2026</td><td>تحويل بنكي من العميل</td><td>—</td><td>120,000</td></tr>
  <tr><td>28/05/2026</td><td>فاتورة INV-2026-147</td><td>236,000</td><td>—</td></tr>
  <tr><td>02/07/2026</td><td>الشيك رقم 004512 (150,000) مرتجع لعدم كفاية الرصيد — لا يحتسب سداداً</td><td>—</td><td>—</td></tr>
  <tr class="total"><td></td><td>الرصيد المستحق على العميل</td><td><span class="struck">380,500</span></td><td></td></tr>
</table>
<p>نشهد بأن الرصيد أعلاه مطابق لدفاتر الشركة.</p>
<table class="sigs">
  <tr><td>المحاسب</td><td>المدير المالي</td></tr>
</table>
""",
                "marks": [
                    {"id": "c2-p3-hand-correction", "type": "handwriting", "color": RED, "size": 23,
                     "text": "٣٨٦,٥٠٠ — م.ح", "top": 462, "left": 104, "rotate": -5,
                     "label_en": "Handwritten correction of the balance to 386,500, with initials",
                     "text_ar": "386,500 — م.ح"},
                    {"id": "c2-p3-signature-accountant", "type": "signature", "color": INK, "top": 565, "left": 480,
                     "width": 160, "height": 62, "rotate": -4, "seed": 61, "label_en": "Accountant's signature"},
                    {"id": "c2-p3-signature-cfo", "type": "signature", "color": INK, "top": 565, "left": 140,
                     "width": 170, "height": 66, "rotate": 5, "seed": 67, "label_en": "Finance manager's signature"},
                    {"id": "c2-p3-stamp-company", "type": "stamp", "kind": "rect", "color": BLUE,
                     "lines": ["الأفق الأزرق لتوريد مواد البناء", "قسم الحسابات", "دبي"], "top": 615, "left": 300,
                     "width": 220, "height": 92, "rotate": 10, "seed": 21,
                     "label_en": "Company accounts stamp", "text_ar": "الأفق الأزرق لتوريد مواد البناء — قسم الحسابات — دبي"},
                ],
            },
        ],
    },
    # ------------------------------------------------------------------ case 03: tenancy
    {
        "id": "case-03",
        "slug": "tenancy",
        "title_en": "Tenancy claim: eviction for unpaid rent (Dubai)",
        "pages": [
            {
                "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">طلب إخلاء ومطالبة بالأجرة المتأخرة</div>
    <div class="ent-sub">مقدم إلى: مركز فض المنازعات الإيجارية — دبي</div>
  </div>
  <div class="meta">
    <div>التاريخ: 07/10/2026</div>
  </div>
</div>
<table class="parties">
  <tr><th>المؤجرة</th><td>عائشة محمد بن حارب الكتبي، مواطنة، دبي.</td></tr>
  <tr><th>المستأجرة</th><td>شركة مسار الواحة للتجارة العامة ذ.م.م، رخصة تجارية رقم 000000.</td></tr>
  <tr><th>العين المؤجرة</th><td>محل رقم (12)، مبنى رقم (7)، منطقة القصيص الصناعية الثانية، دبي.</td></tr>
  <tr><th>عقد الإيجار</th><td>من 01/01/2026 إلى 31/12/2026، بأجرة سنوية قدرها (95,000) درهم تُدفع بأربعة شيكات قيمة كل منها (23,750) درهم.</td></tr>
</table>
<h2>الوقائع</h2>
<p>ارتد الشيكان الثاني المستحق بتاريخ 01/04/2026 والثالث المستحق بتاريخ 01/07/2026 دون صرف، فبلغت الأجرة المتأخرة (47,500) درهم. وقد أُخطرت المستأجرة بالسداد عن طريق الكاتب العدل بتاريخ 02/09/2026، وانقضت مهلة الثلاثين يوماً بتاريخ 02/10/2026 دون سداد.</p>
<h2>الأسانيد</h2>
<p>المادة (19) بشأن التزام المستأجر بسداد الأجرة في مواعيدها، والبند (1/أ) من المادة (25) بشأن الإخلاء لعدم السداد خلال ثلاثين يوماً من تاريخ الإخطار، والمادة (31) التي تنص على أن رفع دعوى الإخلاء لا يعفي المستأجر من سداد الأجرة، وذلك من القانون رقم (26) لسنة 2007 بشأن تنظيم العلاقة بين مؤجري ومستأجري العقارات في إمارة دبي.</p>
<h2>الطلبات</h2>
<ol>
  <li>إخلاء المستأجرة من العين المؤجرة وتسليمها خالية من الشواغل.</li>
  <li>إلزامها بسداد الأجرة المتأخرة وقدرها (47,500) درهم، وما يستجد من أجرة حتى تاريخ الإخلاء الفعلي.</li>
  <li>إلزامها بالرسوم والمصروفات.</li>
</ol>
<div class="sigline">المؤجرة — عائشة محمد بن حارب الكتبي</div>
""",
                "marks": [
                    {"id": "c3-p1-signature-landlord", "type": "signature", "color": INK, "top": 770, "left": 110,
                     "width": 180, "height": 70, "rotate": -2, "seed": 71, "label_en": "Landlord's signature"},
                    {"id": "c3-p1-hand-hearing", "type": "handwriting", "color": INK, "size": 22,
                     "text": "جلسة ١٢/١١/٢٠٢٦ — الساعة ١٠:٠٠ صباحاً", "top": 885, "left": 330, "rotate": -4,
                     "label_en": "Centre clerk's handwritten hearing date",
                     "text_ar": "جلسة 12/11/2026 — الساعة 10:00 صباحاً"},
                    {"id": "c3-p1-stamp-centre", "type": "stamp", "kind": "oval", "color": PURPLE,
                     "lines": ["قسم التسجيل", "نموذج تدريبي", "07/10/2026"], "top": 34, "left": 235, "width": 150,
                     "height": 90, "rotate": 6, "seed": 25,
                     "label_en": "Registration desk stamp (training sample)", "text_ar": "قسم التسجيل — نموذج تدريبي — 07/10/2026"},
                ],
            },
            {
                "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">إخطار بالسداد</div>
    <div class="ent-sub">مرفق رقم (1) بطلب الإخلاء</div>
  </div>
  <div class="meta">
    <div>التاريخ: 01/09/2026</div>
  </div>
</div>
<p>من: عائشة محمد بن حارب الكتبي (المؤجرة).</p>
<p>إلى: شركة مسار الواحة للتجارة العامة ذ.م.م (المستأجرة) — محل رقم (12)، مبنى رقم (7)، منطقة القصيص الصناعية الثانية، دبي.</p>
<p>تحية طيبة وبعد،</p>
<p>نخطركم بأن الشيكين رقمي (100002) و(100003) بقيمة (23,750) درهم لكل منهما، المستحقين بتاريخي 01/04/2026 و01/07/2026 عن أجرة العين المؤجرة، قد ارتدا دون صرف، وأن المبلغ المتأخر في ذمتكم هو (47,500) درهم.</p>
<p>وعليه نطالبكم بسداد هذا المبلغ خلال ثلاثين يوماً من تاريخ استلامكم هذا الإخطار، وإلا سنتقدم بطلب إخلاء العين المؤجرة والمطالبة بالأجرة المتأخرة، وذلك عملاً بالبند (1/أ) من المادة (25) من القانون رقم (26) لسنة 2007 بشأن تنظيم العلاقة بين مؤجري ومستأجري العقارات في إمارة دبي.</p>
<div class="sigline">المؤجرة</div>
""",
                "marks": [
                    {"id": "c3-p2-signature-landlord", "type": "signature", "color": INK, "top": 430, "left": 70,
                     "width": 170, "height": 66, "rotate": 3, "seed": 79, "label_en": "Landlord's signature"},
                    {"id": "c3-p2-stamp-notary", "type": "stamp", "kind": "oval", "color": PURPLE,
                     "lines": ["الكاتب العدل", "نموذج تدريبي", "02/09/2026"], "top": 500, "left": 290, "width": 150,
                     "height": 92, "rotate": -10, "seed": 29,
                     "label_en": "Notary stamp (training sample)", "text_ar": "الكاتب العدل — نموذج تدريبي — 02/09/2026"},
                    {"id": "c3-p2-hand-receipt", "type": "handwriting", "color": BLACK_INK, "size": 22,
                     "text": "استلمت الأصل — ٢/٩/٢٠٢٦ — أمين الصندوق", "top": 830, "left": 300, "rotate": -3,
                     "label_en": "Tenant staff's handwritten receipt note",
                     "text_ar": "استلمت الأصل — 2/9/2026 — أمين الصندوق"},
                    {"id": "c3-p2-signature-receiver", "type": "signature", "color": BLACK_INK, "top": 880, "left": 380,
                     "width": 140, "height": 56, "rotate": -7, "seed": 83, "label_en": "Tenant staff's signature on receipt"},
                    {"id": "c3-p2-stamp-tenant", "type": "stamp", "kind": "rect", "color": BLUE,
                     "lines": ["مسار الواحة للتجارة العامة", "ذ.م.م — دبي"], "top": 870, "left": 90, "width": 220,
                     "height": 80, "rotate": 5, "seed": 33,
                     "label_en": "Tenant company stamp", "text_ar": "مسار الواحة للتجارة العامة — ذ.م.م — دبي"},
                ],
            },
        ],
    },
]
