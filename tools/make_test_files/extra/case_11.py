# -*- coding: utf-8 -*-
"""Case 11 (fictional): payment order (أمر أداء) for unpaid invoices the debtor acknowledged in writing.

Every citation is valid (Civil Procedure Law, Federal Decree-Law No. 42 of 2022, Arts. 143-144,
checked against the official text on 29 Oct 2026). Deliberate challenges:
  - page 2: the printed amount on the debtor's acknowledgment (318,450) is struck through and
    corrected by hand to 293,450 with initials; the application claims the corrected figure;
  - page 1: the notice to pay gave 7 days from service on 1 Oct 2026; its end date (8 Oct 2026)
    is printed nowhere and must be computed.
"""
from cases import BLUE, PURPLE, INK, BLACK_INK, RED  # noqa: F401

CASE = {
    "id": "case-11",
    "slug": "payment-order",
    "title_en": "Payment order: unpaid supply invoices acknowledged in writing by the debtor",
    "pages": [
        # ------------------------------------------------------------------ page 1: the application
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مكتب نخلة الوادي للمحاماة والاستشارات القانونية</div>
    <div class="ent-sub">Nakhlat Al Wadi Advocates &amp; Legal Consultants — الشارقة</div>
  </div>
  <div class="meta">
    <div>التاريخ: 12/10/2026</div>
    <div>المرجع: NW/CIV/2026/214</div>
  </div>
</div>
<h1 class="title">عريضة استصدار أمر أداء</h1>
<p class="center">مقدمة إلى: السيد القاضي المختص بأوامر الأداء — محكمة الشارقة الاتحادية الابتدائية</p>
<table class="parties">
  <tr><th>الطالبة</th><td>شركة البريق الفضي لتجارة معدات المطابخ ذ.م.م (الدائنة)، الشارقة. وكيلها: المحامي/ مازن طلال العويس.</td></tr>
  <tr><th>المطلوب ضدها</th><td>شركة ليالي المرسى لإدارة المطاعم ذ.م.م (المدينة)، رخصة تجارية رقم 000000، الشارقة — منطقة المجاز.</td></tr>
</table>
<h2>الوقائع</h2>
<ol>
  <li>وردت الطالبة إلى المطلوب ضدها معدات مطابخ تجارية لفروعها في الشارقة، فتسلمتها دون تحفظ، وذلك بموجب الفواتير الآتية:</li>
</ol>
<table class="grid">
  <tr><th>البيان</th><th>التاريخ</th><th>المبلغ (درهم)</th></tr>
  <tr><td>فاتورة رقم SG-2026-041</td><td>09/03/2026</td><td>126,000</td></tr>
  <tr><td>فاتورة رقم SG-2026-077</td><td>21/04/2026</td><td>104,250</td></tr>
  <tr><td>فاتورة رقم SG-2026-112</td><td>02/06/2026</td><td>88,200</td></tr>
  <tr><td>يخصم: إشعار دائن رقم CN-2026-019 (بضاعة مرتجعة)</td><td>18/06/2026</td><td>(25,000)</td></tr>
  <tr class="total"><td>صافي المبلغ المستحق</td><td></td><td>293,450</td></tr>
</table>
<ol start="2">
  <li>أقرت المطلوب ضدها كتابةً بالدين بإقرار مؤرخ 06/08/2026 وقعه مديرها العام السيد/ وائل جمال الخطيب.</li>
  <li>كلفت الطالبة المطلوب ضدها بالوفاء بموجب إنذار أُعلن إليها عن طريق الكاتب العدل بتاريخ 01/10/2026، ومنحتها مهلة (7) سبعة أيام من تاريخ إعلانها للسداد، فانقضت المهلة دون وفاء.</li>
</ol>
<h2>الأسانيد</h2>
<ol>
  <li>تتبع أحكام أمر الأداء وفقاً للمادة (143) من المرسوم بقانون اتحادي رقم (42) لسنة 2022 بإصدار قانون الإجراءات المدنية "إذا كان حق الدائن ثابتًا بالكتابة -إلكترونيًّا أو ورقيًّا- وحال الأداء وكان كل ما يطالب به دينًا من النقود معين المقدار"، وهي شروط متوافرة في الدين المطالب به.</li>
  <li>وقد كلفت الطالبة المدينة بالوفاء قبل تقديم العريضة إعمالاً للبند (1) من المادة (144) من القانون ذاته، الذي يوجب تكليف المدين أولاً بالوفاء في ميعاد خمسة أيام على الأقل، ويصدر الأمر خلال ثلاثة أيام عمل من تقديم العريضة وفقاً للبند (4) من المادة ذاتها.</li>
</ol>
<h2>الطلبات</h2>
<p>إلزام المطلوب ضدها بأن تؤدي للطالبة (293,450) درهم والفائدة (5%) سنوياً من تاريخ العريضة، والرسوم والمصروفات.</p>
<div class="sigline">وكيل الطالبة — المحامي/ مازن طلال العويس</div>
""",
            "marks": [
                {"id": "c11-p1-signature-lawyer", "type": "signature", "color": INK, "top": 1009, "left": 118,
                 "width": 170, "height": 52, "rotate": -3, "seed": 151,
                 "label_en": "Signature of the applicant's lawyer"},
                {"id": "c11-p1-stamp-lawfirm", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["مكتب نخلة الوادي للمحاماة", "Nakhlat Al Wadi Advocates", "الشارقة — الإمارات"],
                 "top": 962, "left": 330, "width": 215, "height": 82, "rotate": -5, "seed": 157,
                 "label_en": "Law firm stamp", "text_ar": "مكتب نخلة الوادي للمحاماة — الشارقة"},
                {"id": "c11-p1-stamp-registry", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["مكتب إدارة الدعوى", "نموذج تدريبي", "12/10/2026"], "top": 962, "left": 578,
                 "width": 148, "height": 90, "rotate": 8, "seed": 163,
                 "label_en": "Case management office date stamp (training sample)",
                 "text_ar": "مكتب إدارة الدعوى — نموذج تدريبي — 12/10/2026"},
            ],
        },
        # ------------------------------------------------------------------ page 2: the debtor's acknowledgment
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">شركة ليالي المرسى لإدارة المطاعم ذ.م.م</div>
    <div class="ent-sub">Layali Al Marsa Restaurant Management LLC</div>
    <div class="ent-sub">الشارقة — ص.ب: 00000 — رخصة تجارية رقم 000000</div>
  </div>
  <div class="meta">
    <div>التاريخ: 06/08/2026</div>
    <div>المرجع: LM/FIN/2026/052</div>
  </div>
</div>
<h1 class="title">إقرار بالمديونية</h1>
<p>نقر نحن شركة ليالي المرسى لإدارة المطاعم ذ.م.م، ويمثلها في التوقيع على هذا الإقرار مديرها العام السيد/ وائل جمال الخطيب، بأن ذمتنا مشغولة لصالح الدائنة المبينة أدناه بمبلغ الدين المبين أدناه، وبأننا تسلمنا المعدات موضوع الفواتير المذكورة كاملة وبحالة سليمة ودون أي تحفظ:</p>
<table class="parties">
  <tr><th>الدائنة</th><td>شركة البريق الفضي لتجارة معدات المطابخ ذ.م.م — الشارقة.</td></tr>
  <tr><th>سبب الدين</th><td>قيمة معدات مطابخ تجارية موردة إلى فروعنا في الشارقة،<br>بموجب الفواتير أرقام SG-2026-041 وSG-2026-077 وSG-2026-112.</td></tr>
  <tr><th>موعد السداد</th><td>دفعة واحدة في موعد أقصاه 31/08/2026.</td></tr>
  <tr><th>مبلغ الدين</th><td>بالدرهم الإماراتي: <span class="struck">318,450</span></td></tr>
</table>
<p>ونتعهد بسداد مبلغ الدين في الموعد المبين أعلاه، ونقر بأنه دين ثابت في ذمتنا وحال الأداء في ذلك الموعد وغير متنازع عليه، ويحق للدائنة عند التأخر في السداد اتخاذ ما تراه من إجراءات قانونية لاستيفائه.</p>
<p>وهذا إقرار منا بذلك، صادر بإرادتنا الحرة ونحن بكامل الأهلية القانونية، وقد حُرر من نسختين بيد كل طرف نسخة للعمل بموجبها.</p>
<table class="sigs">
  <tr><td>المقر — عن الشركة<br>المدير العام: وائل جمال الخطيب</td><td>ختم الشركة</td></tr>
</table>
""",
            "marks": [
                {"id": "c11-p2-hand-correction", "type": "handwriting", "color": RED, "size": 23,
                 "text": "٢٩٣,٤٥٠ — و.خ", "top": 441, "left": 327, "rotate": -3,
                 "label_en": "Handwritten correction of the debt amount to 293,450, with initials",
                 "text_ar": "293,450 — و.خ"},
                {"id": "c11-p2-signature-gm", "type": "signature", "color": INK, "top": 700, "left": 500,
                 "width": 180, "height": 70, "rotate": -4, "seed": 167,
                 "label_en": "Debtor's general manager's signature"},
                {"id": "c11-p2-stamp-company", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["ليالي المرسى لإدارة المطاعم", "Layali Al Marsa Restaurant Mgmt", "الشارقة — ذ.م.م"],
                 "top": 700, "left": 120, "width": 230, "height": 92, "rotate": 6, "seed": 173,
                 "label_en": "Debtor company stamp", "text_ar": "ليالي المرسى لإدارة المطاعم — الشارقة — ذ.م.م"},
            ],
        },
    ],
}
