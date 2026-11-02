# -*- coding: utf-8 -*-
"""Case 05: commercial claim on three returned cheques, with a provisional attachment (fictional).

A supplier of electrical equipment holds three cheques from a contracting company that came
back unpaid. The summary judge ordered a provisional attachment of the debtor's bank balances;
the supplier then filed the main claim to confirm its right and the attachment. Everything is
made up; the articles cited were checked against the official texts on 29 Oct 2026.

Planted for the reader: an article range "المواد (663-665)" of the Commercial Transactions Law
(three valid articles), a citation of Article 350 of the Civil Procedure Law (the law has 338
articles), and the deadline to file the main claim, which must be worked out from the decision
date: 8 days under Article 250(2) of the Civil Procedure Law.
"""
from cases import BLACK_INK, BLUE, INK, PURPLE

CASE = {
    "id": "case-05",
    "slug": "cheques",
    "title_en": "Commercial claim: three returned cheques and a provisional attachment of bank accounts",
    "pages": [
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مكتب درع القانون للمحاماة والاستشارات القانونية</div>
    <div class="ent-sub">Diraa Al Qanoon Advocates &amp; Legal Consultants</div>
  </div>
  <div class="meta">
    <div>التاريخ: 14/09/2026</div>
    <div>المرجع: DQ/COM/2026/233</div>
  </div>
</div>
<h1 class="title">صحيفة دعوى تجارية</h1>
<p class="center">مقدمة إلى: محكمة الشارقة الاتحادية الابتدائية — الدائرة التجارية</p>
<table class="parties">
  <tr><th>المدعية</th><td>شركة ومضة النور لتوريد المعدات الكهربائية ذ.م.م، رخصة تجارية رقم 000000، الشارقة.</td></tr>
  <tr><th>المدعى عليها</th><td>شركة أعمدة الشروق للمقاولات ذ.م.م، الشارقة، ويمثلها مديرها/ عمار سليم القباني.</td></tr>
</table>
<h2>الوقائع</h2>
<p>بموجب اتفاقية توريد مؤرخة 10/02/2026 حررت المدعى عليها للمدعية ثلاثة شيكات ارتدت دون صرف:</p>
<table class="grid">
  <tr><th>رقم الشيك</th><th>التاريخ</th><th>المبلغ (درهم)</th><th>البنك المسحوب عليه</th><th>سبب الارتجاع</th></tr>
  <tr><td>000731</td><td>15/06/2026</td><td>96,400</td><td>مصرف الكثبان الوطني</td><td>عدم كفاية الرصيد</td></tr>
  <tr><td>000732</td><td>15/07/2026</td><td>112,750</td><td>مصرف الكثبان الوطني</td><td>عدم كفاية الرصيد</td></tr>
  <tr><td>000733</td><td>15/08/2026</td><td>88,600</td><td>مصرف الكثبان الوطني</td><td>عدم مطابقة التوقيع</td></tr>
  <tr class="total"><td colspan="2">الإجمالي</td><td>297,750</td><td colspan="2"></td></tr>
</table>
<p>وبتاريخ 09/09/2026 أمر قاضي الأمور المستعجلة في الطلب رقم (412/2026) بالحجز التحفظي على أرصدة المدعى عليها.</p>
<h2>الأسانيد</h2>
<ol>
  <li>الشيك مستحق الوفاء في تاريخ إصداره وفقاً للمادة (648) من المرسوم بقانون اتحادي رقم (50) لسنة 2022 بإصدار قانون المعاملات التجارية، وقد ثبت امتناع المسحوب عليه عن الدفع ببيان مؤرخ على كل شيك، فيحق للمدعية الرجوع على الساحبة عملاً بالمواد (663-665) من قانون المعاملات التجارية.</li>
  <li>يجوز الحجز التحفظي لحامل سند بدين مستحق الأداء وفقاً للمادة (247) من المرسوم بقانون اتحادي رقم (42) لسنة 2022 بإصدار قانون الإجراءات المدنية، وتُرفع هذه الدعوى في الميعاد المقرر في المادة (250) من القانون ذاته.</li>
</ol>
<h2>الطلبات</h2>
<p>أولاً: الحكم بصحة الحجز التحفظي الموقع في الطلب رقم (412/2026) وتثبيته. ثانياً: إلزام المدعى عليها بأداء مبلغ (297,750) درهم والفائدة بواقع (5%) سنوياً من تاريخ استحقاق كل شيك. ثالثاً: إلزامها بالرسوم والمصروفات ومقابل أتعاب المحاماة عملاً بالمادة (350) من قانون الإجراءات المدنية.</p>
<div class="sigline">وكيل المدعية — المحامي/ ماجد عيسى البلوشي</div>
""",
            "marks": [
                {"id": "c5-p1-stamp-registry", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["قلم قيد الدعاوى", "نموذج تدريبي", "15/09/2026"],
                 "top": 120, "left": 52, "width": 170, "height": 86, "rotate": 7, "seed": 61,
                 "label_en": "Court registry date stamp (training sample)",
                 "text_ar": "قلم قيد الدعاوى — نموذج تدريبي — 15/09/2026"},
                {"id": "c5-p1-signature-lawyer", "type": "signature", "color": INK, "top": 978, "left": 120,
                 "width": 180, "height": 66, "rotate": 3, "seed": 67,
                 "label_en": "Signature of the claimant's lawyer"},
            ],
        },
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مصرف الكثبان الوطني (ش.م.ع)</div>
    <div class="ent-sub">Al Kuthban National Bank PJSC</div>
    <div class="ent-sub">فرع الصجعة — الشارقة</div>
  </div>
  <div class="meta">
    <div>التاريخ: 03/09/2026</div>
    <div>المرجع: KNB/CLR/2026/1187</div>
  </div>
</div>
<h1 class="title">إفادة بارتجاع شيكات</h1>
<p>إلى من يهمه الأمر،</p>
<table class="parties">
  <tr><th>الساحب</th><td>شركة أعمدة الشروق للمقاولات ذ.م.م — الحساب الجاري رقم (0000-000000-000) لدى فرع الصجعة.</td></tr>
  <tr><th>الحامل</th><td>شركة ومضة النور لتوريد المعدات الكهربائية ذ.م.م.</td></tr>
  <tr><th>طريقة التقديم</th><td>غرفة المقاصة الإلكترونية.</td></tr>
</table>
<p>بناءً على طلب الحامل، يفيد مصرف الكثبان الوطني بأن الشيكات المبينة أدناه، المسحوبة على الحساب المذكور، قد قُدمت للوفاء وأعيدت دون صرف للأسباب المبينة قرين كل منها، وقد أُثبت بيان الارتجاع مؤرخاً على كل شيك:</p>
<table class="grid">
  <tr><th>رقم الشيك</th><th>تاريخ الشيك</th><th>المبلغ (درهم)</th><th>تاريخ التقديم</th><th>تاريخ الارتجاع</th><th>سبب الارتجاع</th></tr>
  <tr><td>000731</td><td>15/06/2026</td><td>96,400</td><td>15/06/2026</td><td>16/06/2026</td><td>عدم كفاية الرصيد</td></tr>
  <tr><td>000732</td><td>15/07/2026</td><td>112,750</td><td>15/07/2026</td><td>16/07/2026</td><td>عدم كفاية الرصيد</td></tr>
  <tr><td>000733</td><td>15/08/2026</td><td>88,600</td><td>17/08/2026</td><td>18/08/2026</td><td>عدم مطابقة التوقيع</td></tr>
  <tr class="total"><td colspan="2">الإجمالي</td><td>297,750</td><td colspan="3"></td></tr>
</table>
<p>وقد أُخطر المصرف المركزي ببيانات صاحب الحساب عن الشيكين المرتجعين لعدم كفاية الرصيد، وفقاً للأنظمة المعمول بها.</p>
<p>أُعطيت هذه الإفادة بناءً على طلب الحامل لتقديمها إلى الجهات المختصة، دون أدنى مسؤولية على المصرف.</p>
<div class="sigline">قسم المقاصة والعمليات — المفوض بالتوقيع</div>
""",
            "marks": [
                {"id": "c5-p2-signature-bank", "type": "signature", "color": BLACK_INK, "top": 770, "left": 110,
                 "width": 170, "height": 64, "rotate": -3, "seed": 71,
                 "label_en": "Bank's authorised signatory signature"},
                {"id": "c5-p2-stamp-bank", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["مصرف الكثبان الوطني", "نموذج تدريبي", "فرع الصجعة — الشارقة"],
                 "top": 772, "left": 310, "width": 210, "height": 92, "rotate": -6, "seed": 73,
                 "label_en": "Bank stamp (training sample)",
                 "text_ar": "مصرف الكثبان الوطني — نموذج تدريبي — فرع الصجعة — الشارقة"},
            ],
        },
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">محكمة الشارقة الاتحادية الابتدائية</div>
    <div class="ent-sub">قاضي الأمور المستعجلة — الأوامر على العرائض</div>
  </div>
  <div class="meta">
    <div>رقم الطلب: 412/2026 حجز تحفظي تجاري</div>
    <div>تاريخ تقديم الطلب: 07/09/2026</div>
    <div>تاريخ القرار: 09/09/2026</div>
  </div>
</div>
<h1 class="title">قرار في طلب حجز تحفظي</h1>
<table class="parties">
  <tr><th>الطالبة</th><td>شركة ومضة النور لتوريد المعدات الكهربائية ذ.م.م، وكيلها: المحامي/ ماجد عيسى البلوشي.</td></tr>
  <tr><th>المطلوب ضدها</th><td>شركة أعمدة الشروق للمقاولات ذ.م.م — الشارقة، منطقة الصجعة الصناعية.</td></tr>
  <tr><th>موضوع الطلب</th><td>توقيع الحجز التحفظي على الحسابات المصرفية للمطلوب ضدها لدى المصارف العاملة في الدولة في حدود مبلغ (297,750) درهم، قيمة ثلاثة شيكات مرتجعة.</td></tr>
  <tr><th>المستندات</th><td>صور الشيكات الثلاثة، وإفادة مصرف الكثبان الوطني المؤرخة 03/09/2026.</td></tr>
</table>
<p>بعد الاطلاع على الطلب والمستندات المرفقة، وعلى المادة (249) من المرسوم بقانون اتحادي رقم (42) لسنة 2022 بإصدار قانون الإجراءات المدنية:</p>
<table class="grid">
  <tr><th>القرار</th></tr>
  <tr><td>&nbsp;<br>&nbsp;<br>&nbsp;<br>&nbsp;<br>&nbsp;<br>&nbsp;<br>&nbsp;<br>&nbsp;</td></tr>
</table>
<div class="sigline">قاضي الأمور المستعجلة — القاضي/ سعيد مبارك الطنيجي</div>
""",
            "marks": [
                {"id": "c5-p3-hand-decision", "type": "handwriting", "color": BLACK_INK, "size": 21,
                 "text": "قررنا: توقيع الحجز التحفظي على أرصدة المطلوب ضدها لدى المصارف العاملة في الدولة في حدود مبلغ ٢٩٧,٧٥٠ درهماً، وعلى الطالبة رفع دعوى ثبوت الحق خلال (٨) ثمانية أيام من تاريخ صدور هذا القرار وإلا اعتُبر الحجز كأن لم يكن.",
                 "top": 520, "left": 76, "rotate": -1, "width": 636,
                 "label_en": "Judge's handwritten decision: attachment ordered; main claim to be filed within 8 days",
                 "text_ar": "قررنا: توقيع الحجز التحفظي على أرصدة المطلوب ضدها لدى المصارف العاملة في الدولة في حدود مبلغ 297,750 درهماً، وعلى الطالبة رفع دعوى ثبوت الحق خلال (8) ثمانية أيام من تاريخ صدور هذا القرار وإلا اعتبر الحجز كأن لم يكن."},
                {"id": "c5-p3-signature-judge", "type": "signature", "color": BLACK_INK, "top": 800, "left": 110,
                 "width": 180, "height": 68, "rotate": -5, "seed": 79,
                 "label_en": "Summary judge's signature"},
                {"id": "c5-p3-stamp-court", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["محكمة الشارقة الاتحادية الابتدائية", "نموذج تدريبي", "09/09/2026"],
                 "top": 795, "left": 330, "width": 240, "height": 104, "rotate": 7, "seed": 83,
                 "label_en": "Court stamp (training sample)",
                 "text_ar": "محكمة الشارقة الاتحادية الابتدائية — نموذج تدريبي — 09/09/2026"},
            ],
        },
    ],
}
