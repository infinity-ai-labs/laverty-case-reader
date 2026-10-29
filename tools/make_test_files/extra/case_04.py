# -*- coding: utf-8 -*-
"""Case 04: labour claim before the Abu Dhabi labour court (fictional).

A sales manager claims two months' unpaid wages, unused annual leave, the end-of-service
gratuity and the notice allowance from a trading company, after the Ministry of Human
Resources and Emiratisation referred the dispute to court. Everything is made up; the
Labour Law articles cited were checked against the official text on 29 Oct 2026.

Planted for the reader: a clause-first citation ("البند (9) من المادة (29)"), a citation
written with "رقم" ("المادة رقم (51)"), and a first hearing date that appears only in the
lawyer's handwritten note on the ministry memo.
"""
from cases import BLUE, INK, PURPLE

CASE = {
    "id": "case-04",
    "slug": "labour-abudhabi",
    "title_en": "Labour claim (Abu Dhabi): unpaid wages, annual leave, gratuity and notice allowance",
    "pages": [
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مكتب منارة الحق للمحاماة والاستشارات القانونية</div>
    <div class="ent-sub">Manarat Al Haq Advocates &amp; Legal Consultants</div>
    <div class="ent-sub">أبوظبي — ص.ب: 00000</div>
  </div>
  <div class="meta">
    <div>التاريخ: 07/10/2026</div>
    <div>المرجع: MH/LAB/2026/064</div>
  </div>
</div>
<h1 class="title">صحيفة دعوى عمالية</h1>
<p class="center">مقدمة إلى: محكمة أبوظبي العمالية الابتدائية</p>
<table class="parties">
  <tr><th>المدعي</th><td>مازن رياض العطار، لبناني الجنسية، هوية رقم 784-1986-0000000-0، مدير مبيعات.</td></tr>
  <tr><th>المدعى عليها</th><td>شركة قوس الندى للتجارة العامة ذ.م.م، رخصة تجارية رقم 000000، أبوظبي — مصفح.</td></tr>
</table>
<h2>الوقائع</h2>
<ol>
  <li>عمل المدعي لديها منذ 01/03/2022 براتب شهري (22,000) درهم، منه أجر أساسي (14,000) درهم، ومهلة إنذار (30) يوماً.</li>
  <li>لم تصرف أجره عن شهري يوليو وأغسطس 2026، وأنهت خدمته في 31/08/2026 دون إنذار، وله رصيد إجازة (24) يوماً.</li>
  <li>تعذرت التسوية الودية للشكوى رقم (AUH-2026-47102) المقدمة بتاريخ 07/09/2026، فأحالت الوزارة النزاع إلى المحكمة بمذكرة مؤرخة 28/09/2026 عملاً بالمادة (54) من المرسوم بقانون اتحادي رقم (33) لسنة 2021 بشأن تنظيم علاقات العمل.</li>
</ol>
<h2>الأسانيد القانونية</h2>
<ol>
  <li>توجب المادة (22) من المرسوم بقانون المشار إليه أداء الأجور في مواعيد استحقاقها.</li>
  <li>يستحق المدعي أجر أيام إجازته غير المستعملة على أساس الأجر الأساسي وفقاً للبند (9) من المادة (29).</li>
  <li>تستحق له مكافأة نهاية الخدمة بواقع أجر (21) يوماً عن كل سنة على أساس الأجر الأساسي، عملاً بالمادة رقم (51).</li>
  <li>لم تلتزم المدعى عليها بمهلة الإنذار وفق المادة (43)، ولا بأداء المستحقات خلال (14) يوماً وفق المادة (53).</li>
</ol>
<p><b>الطلبات:</b> إلزام المدعى عليها بأن تؤدي للمدعي ما يلي، مع الرسوم والمصروفات ومقابل أتعاب المحاماة:</p>
<table class="grid">
  <tr><th>م</th><th>البند</th><th>المبلغ (درهم)</th></tr>
  <tr><td>1</td><td>الأجور المتأخرة عن شهري يوليو وأغسطس 2026</td><td>44,000</td></tr>
  <tr><td>2</td><td>بدل رصيد الإجازة السنوية (24 يوماً على أساس الأجر الأساسي)</td><td>11,200</td></tr>
  <tr><td>3</td><td>مكافأة نهاية الخدمة (4 سنوات و6 أشهر × 21 يوماً)</td><td>44,100</td></tr>
  <tr><td>4</td><td>بدل الإنذار (30 يوماً)</td><td>22,000</td></tr>
  <tr class="total"><td></td><td>الإجمالي</td><td>121,300</td></tr>
</table>
<div class="sigline">وكيلة المدعي — المحامية/ نورة سالم المهيري</div>
""",
            "marks": [
                {"id": "c4-p1-stamp-registry", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["محكمة أبوظبي العمالية", "قلم القيد — نموذج تدريبي", "08/10/2026"],
                 "top": 140, "left": 48, "width": 196, "height": 80, "rotate": -7, "seed": 41,
                 "label_en": "Court registry date stamp (training sample)",
                 "text_ar": "محكمة أبوظبي العمالية — قلم القيد — نموذج تدريبي — 08/10/2026"},
                {"id": "c4-p1-signature-lawyer", "type": "signature", "color": INK, "top": 975, "left": 110,
                 "width": 180, "height": 66, "rotate": -4, "seed": 43,
                 "label_en": "Signature of the claimant's lawyer"},
                {"id": "c4-p1-stamp-lawfirm", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["مكتب منارة الحق للمحاماة", "Manarat Al Haq Advocates", "أبوظبي — الإمارات"],
                 "top": 962, "left": 320, "width": 230, "height": 84, "rotate": 5, "seed": 47,
                 "label_en": "Law firm stamp", "text_ar": "مكتب منارة الحق للمحاماة — أبوظبي — الإمارات"},
            ],
        },
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">وزارة الموارد البشرية والتوطين</div>
    <div class="ent-sub">إدارة علاقات العمل — أبوظبي</div>
  </div>
  <div class="meta">
    <div>رقم الشكوى: AUH-2026-47102</div>
    <div>التاريخ: 28/09/2026</div>
  </div>
</div>
<h1 class="title">مذكرة إحالة نزاع عمالي إلى المحكمة المختصة</h1>
<p class="center">(لتعذر التسوية الودية)</p>
<table class="parties">
  <tr><th>العامل</th><td>مازن رياض العطار — مدير مبيعات — هوية رقم 784-1986-0000000-0.</td></tr>
  <tr><th>صاحب العمل</th><td>شركة قوس الندى للتجارة العامة ذ.م.م، ويمثلها مدير الموارد البشرية/ فراس حسن الدباغ.</td></tr>
  <tr><th>تاريخ الشكوى</th><td>07/09/2026</td></tr>
</table>
<h2>أولاً: ملخص النزاع</h2>
<p>أفاد العامل بأنه يعمل لدى صاحب العمل منذ 01/03/2022 براتب إجمالي قدره (22,000) درهم، منه أجر أساسي قدره (14,000) درهم، وأن صاحب العمل لم يصرف أجره عن شهري يوليو وأغسطس 2026 وأنهى خدمته بتاريخ 31/08/2026 دون إنذار، وطالب بمبلغ (121,300) درهم عن الأجور المتأخرة وبدل الإجازة السنوية ومكافأة نهاية الخدمة وبدل الإنذار.</p>
<h2>ثانياً: رد صاحب العمل</h2>
<p>أقر ممثل صاحب العمل بتأخر صرف الأجور لظروف مالية، ونازع في بدل الإنذار بدعوى أن الإنهاء تم باتفاق الطرفين، وقدم عرضاً كتابياً مؤرخاً 15/09/2026 بسداد مبلغ (60,000) درهم على ثلاثة أقساط شهرية، تسويةً نهائية وشاملة لجميع مستحقات العامل.</p>
<h2>ثالثاً: موقف العامل</h2>
<p>رفض العامل العرض الكتابي في جلسة التسوية المنعقدة يوم الأربعاء الموافق 16/09/2026، وتمسك بكامل طلباته.</p>
<h2>رابعاً: توصية الوزارة</h2>
<p>ترى الوزارة أحقية العامل في أجوره وبدل إجازته ومكافأة نهاية الخدمة، وتترك تقدير بدل الإنذار للمحكمة.</p>
<h2>خامساً: القرار</h2>
<p>لتعذر التسوية الودية، ولتجاوز قيمة المطالبة مبلغ (50,000) درهم، يُحال النزاع إلى المحكمة المختصة عملاً بالمادة (54) من المرسوم بقانون اتحادي رقم (33) لسنة 2021 بشأن تنظيم علاقات العمل، مرفقاً به ملف الشكوى.</p>
<div class="sigline">الباحثة القانونية/ موزة خلفان الرميثي</div>
""",
            "marks": [
                {"id": "c4-p2-stamp-ministry", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["وزارة الموارد البشرية والتوطين", "نموذج تدريبي", "28/09/2026"],
                 "top": 905, "left": 70, "width": 230, "height": 104, "rotate": -8, "seed": 53,
                 "label_en": "Ministry of Human Resources and Emiratisation stamp (training sample)",
                 "text_ar": "وزارة الموارد البشرية والتوطين — نموذج تدريبي — 28/09/2026"},
                {"id": "c4-p2-hand-lawyer-note", "type": "handwriting", "color": INK, "size": 21,
                 "text": "عرض الشركة شفهياً بعد الإحالة: ٨٥,٠٠٠ درهم — رفضه الموكل. الجلسة الأولى: ١٠/١١/٢٠٢٦ — ن.م",
                 "top": 960, "left": 420, "rotate": -3, "width": 320,
                 "label_en": "Claimant's lawyer's handwritten note: employer's oral offer and first hearing date",
                 "text_ar": "عرض الشركة شفهياً بعد الإحالة: 85,000 درهم — رفضه الموكل. الجلسة الأولى: 10/11/2026 — ن.م"},
            ],
        },
    ],
}
