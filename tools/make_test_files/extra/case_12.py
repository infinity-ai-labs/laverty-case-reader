# -*- coding: utf-8 -*-
"""Case 12 (fictional): trademark infringement claim against a shop selling counterfeit perfume.

Everything is invented: the companies, the trademark "ZAHRANOVA", the people, and all numbers.
The laws cited are real; each valid citation was read in the official text of Federal
Decree-Law No. 36 of 2021 on Trademarks. One citation is planted on purpose: "المادة (47) مكرراً"
(Article 47 bis) does not exist; the law has 61 articles and no bis articles.
"""
from cases import BLUE, PURPLE, INK, BLACK_INK, RED  # noqa: F401

CASE = {
    "id": "case-12",
    "slug": "trademark",
    "title_en": "Trademark infringement claim: counterfeit perfume seized from a shop",
    "pages": [
        # ------------------------------------------------------------ page 1: statement of claim
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مكتب درع الحقوق للمحاماة والملكية الفكرية</div>
    <div class="ent-sub">Dir' Al Huquq Advocates &amp; IP Consultants — دبي</div>
  </div>
  <div class="meta">
    <div>التاريخ: 21/10/2026</div>
    <div>المرجع: DH/IP/2026/052</div>
  </div>
</div>
<h1 class="title">صحيفة دعوى تعدٍّ على علامة تجارية مسجلة</h1>
<p class="center">مقدمة إلى: محكمة دبي الابتدائية — الدائرة المدنية الكلية</p>
<table class="parties">
  <tr><th>المدعية</th><td>شركة زهرانوفا للعطور ومستحضرات التجميل ذ.م.م، رخصة تجارية رقم 000000، دبي.</td></tr>
  <tr><th>المدعى عليها</th><td>مؤسسة غيمة الريحان لتجارة العطور (مؤسسة فردية) ومالكها فيصل منصور الجابري، ديرة — دبي.</td></tr>
</table>
<p><b>الوقائع:</b> تملك المدعية العلامة "زهرانوفا — ZAHRANOVA" المسجلة بوزارة الاقتصاد برقم (000417) عن الفئة (3) (المرفق 1). وفي 24/09/2026 اشترى مندوبها من المدعى عليها عبوتين تحملان العلامة بسعر (95) درهماً للعبوة، وسعر الأصلي (385) درهماً (المرفق 2). وفي 06/10/2026 صدر الأمر على عريضة رقم (731) لسنة 2026 بالوصف والحجز التحفظي، ونُفذ في 08/10/2026 بضبط:</p>
<table class="grid">
  <tr><th>م</th><th>الصنف المضبوط</th><th>الكمية</th><th>سعر المنتج الأصلي (درهم)</th><th>القيمة (درهم)</th></tr>
  <tr><td>1</td><td>عطر زهرانوفا كلاسيك 100 مل</td><td>240</td><td>385</td><td>92,400</td></tr>
  <tr><td>2</td><td>عطر زهرانوفا روز 50 مل</td><td>180</td><td>245</td><td>44,100</td></tr>
  <tr><td>3</td><td>طقم هدايا (عطر وبخاخ للجسم)</td><td>60</td><td>520</td><td>31,200</td></tr>
  <tr><td>4</td><td>دهن عود زهرانوفا 12 مل</td><td>95</td><td>290</td><td>27,550</td></tr>
  <tr><td>5</td><td>علب وأغلفة فارغة تحمل العلامة</td><td>1,500</td><td>4</td><td>6,000</td></tr>
  <tr class="total"><td></td><td>إجمالي القيمة التقديرية للمضبوطات</td><td></td><td></td><td>201,250</td></tr>
</table>
<h2>الأسانيد القانونية</h2>
<ol>
  <li>تُعد المدعية مالكة العلامة بتسجيلها عملاً بالبند (1) من المادة (18) من المرسوم بقانون اتحادي رقم (36) لسنة 2021 بشأن العلامات التجارية، وتمتد حمايتها عشر سنوات من تاريخ تقديم الطلب وفقاً للبند (1) من المادة (21).</li>
  <li>ينص البند (2) من المادة (17) على أن "لمالك العلامة التجارية المسجلة الحق في منع الغير الذي لم يحصل على موافقته من استعمالها أو استعمال أي إشارة مماثلة أو مشابهة لها".</li>
  <li>صدر الأمر التحفظي استناداً إلى البند (1) من المادة (47)، وتُرفع الدعوى خلال الميعاد المقرر في البند (7) منها، كما تجيز المادة (47) مكرراً من المرسوم بقانون ذاته الأمر بإتلاف السلع المقلدة على نفقة المتعدي.</li>
  <li>تستحق المدعية التعويض وفقاً للمادة (48)، مع حفظ حقها في الدعوى الجزائية عن الفعل المؤثم بالبند (1) من المادة (50).</li>
</ol>
<p><b>الطلبات:</b> (1) تثبيت الحجز التحفظي، ومنع المدعى عليها من استعمال العلامة أو أي علامة مشابهة لها، ومصادرة المضبوطات وإتلافها على نفقتها. (2) إلزامها بأن تؤدي للمدعية تعويضاً قدره (350,000) درهم، وبالرسوم والمصروفات ومقابل أتعاب المحاماة.</p>
<div class="sigline">وكيلة المدعية — المحامية/ نوال عيسى الحمادي</div>
""",
            "marks": [
                {"id": "c12-p1-stamp-registry", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["قلم القيد", "نموذج تدريبي", "22/10/2026"], "top": 26, "left": 262, "width": 140,
                 "height": 80, "rotate": -7, "seed": 112,
                 "label_en": "Registry date stamp (training sample)", "text_ar": "قلم القيد — نموذج تدريبي — 22/10/2026"},
                {"id": "c12-p1-hand-hearing", "type": "handwriting", "color": INK, "size": 21,
                 "text": "حُددت جلسة ٩/١١/٢٠٢٦", "top": 128, "left": 62, "rotate": -4,
                 "label_en": "Registry clerk's handwritten hearing date",
                 "text_ar": "حددت جلسة 9/11/2026"},
                {"id": "c12-p1-signature-lawyer", "type": "signature", "color": INK, "top": 975, "left": 405,
                 "width": 170, "height": 60, "rotate": -4, "seed": 121,
                 "label_en": "Signature of the claimant's lawyer"},
                {"id": "c12-p1-stamp-lawfirm", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["مكتب درع الحقوق للمحاماة", "Dir' Al Huquq Advocates", "دبي — الإمارات"],
                 "top": 972, "left": 540, "width": 196, "height": 76, "rotate": 4, "seed": 123,
                 "label_en": "Law firm stamp", "text_ar": "مكتب درع الحقوق للمحاماة — دبي"},
            ],
        },
        # ------------------------------------------------------------ page 2: certificate summary + invoice
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">وزارة الاقتصاد</div>
    <div class="ent-sub">إدارة العلامات التجارية</div>
  </div>
  <div class="meta">
    <div>مرفق رقم (1)</div>
    <div>تاريخ الاستخراج: 29/09/2026</div>
  </div>
</div>
<h1 class="title">بيانات شهادة تسجيل علامة تجارية</h1>
<table class="parties">
  <tr><th>رقم العلامة</th><td>000417</td></tr>
  <tr><th>تاريخ الطلب</th><td>12/01/2026 — الأولوية: لا يوجد</td></tr>
  <tr><th>تاريخ التسجيل</th><td>18/05/2026 — تاريخ انتهاء الحماية: 11/01/2036</td></tr>
  <tr><th>المالك</th><td>شركة زهرانوفا للعطور ومستحضرات التجميل ذ.م.م — الجنسية: الإمارات — دبي، منطقة جبل علي الصناعية الأولى</td></tr>
  <tr><th>الفئة والسلع</th><td>الفئة (3): العطور، ودهن العود، ومستحضرات التجميل، وبخاخات الجسم، ومزيلات العرق.</td></tr>
  <tr><th>العلامة</th><td>ZAHRANOVA — زهرانوفا (علامة كلمية باللونين الذهبي والأسود)</td></tr>
</table>
<p>يُستخرج هذا البيان من سجل العلامات التجارية بناءً على طلب مالك العلامة، ولا يُعد بديلاً عن أصل شهادة التسجيل.</p>
<h2>مرفق رقم (2): مقتطف من فاتورة الشراء التجريبي</h2>
<table class="parties">
  <tr><th>البائع</th><td>مؤسسة غيمة الريحان لتجارة العطور — دبي — ديرة — منطقة المرر — الرقم الضريبي: 000000000000000</td></tr>
  <tr><th>الفاتورة</th><td>فاتورة ضريبية مبسطة رقم (S-2026-0815) — التاريخ: 24/09/2026 — العميل: نقدي</td></tr>
</table>
<table class="grid">
  <tr><th>الصنف</th><th>الكمية</th><th>سعر الوحدة (درهم)</th><th>المبلغ (درهم)</th></tr>
  <tr><td>عطر زهرانوفا كلاسيك 100 مل</td><td>2</td><td>95.00</td><td>190.00</td></tr>
  <tr><td>ضريبة القيمة المضافة (5%)</td><td></td><td></td><td>9.50</td></tr>
  <tr class="total"><td>الإجمالي المدفوع نقداً</td><td></td><td></td><td>199.50</td></tr>
</table>
<p>البضاعة المباعة لا تُرد ولا تُستبدل.</p>
<p>رقم الإيصال:</p>
<p>توقيع البائع وختم المحل:</p>
""",
            "marks": [
                {"id": "c12-p2-stamp-ministry", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["وزارة الاقتصاد", "نموذج تدريبي", "29/09/2026"], "top": 188,
                 "left": 100, "width": 168, "height": 96, "rotate": -9, "seed": 131,
                 "label_en": "Ministry of Economy stamp on the certificate summary (training sample)",
                 "text_ar": "وزارة الاقتصاد — نموذج تدريبي — 29/09/2026"},
                {"id": "c12-p2-hand-receipt", "type": "handwriting", "color": BLACK_INK, "size": 23,
                 "text": "٣٠٨٧", "top": 812, "left": 540, "rotate": -3,
                 "label_en": "Shop cashier's handwritten receipt number", "text_ar": "3087"},
                {"id": "c12-p2-signature-seller", "type": "signature", "color": BLACK_INK, "top": 885, "left": 420,
                 "width": 150, "height": 58, "rotate": 4, "seed": 137,
                 "label_en": "Shop cashier's signature on the invoice"},
                {"id": "c12-p2-stamp-shop", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["غيمة الريحان لتجارة العطور", "ديرة — دبي"], "top": 880, "left": 170, "width": 210,
                 "height": 78, "rotate": -6, "seed": 139,
                 "label_en": "Shop stamp on the test-purchase invoice", "text_ar": "غيمة الريحان لتجارة العطور — ديرة — دبي"},
            ],
        },
    ],
}
