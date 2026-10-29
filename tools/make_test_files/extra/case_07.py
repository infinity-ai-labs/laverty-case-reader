# -*- coding: utf-8 -*-
"""Case 07 (fictional): a civil claim for compensation after a traffic accident in Dubai on
16 June 2026, against the driver and his insurer.

The accident happened after 1 June 2026, so the claim rests on the NEW Civil Transactions Law
(Federal Decree-Law No. 25 of 2025). Deliberate challenge for the Case Reader: the claim quotes
Article 255 of that law in quotation marks, but one word is changed ("محتملة", probable, where the
official text says "طبيعية", natural). The permanent disability percentage on the medical report is
written by hand by the doctor.

Everyone and everything here is invented. Every citation was read against the official texts on
29 Oct 2026.
"""
from cases import BLUE, PURPLE, INK, BLACK_INK  # noqa: F401

CASE = {
    "id": "case-07",
    "slug": "traffic-compensation",
    "title_en": "Civil claim: compensation for injuries in a traffic accident (Dubai)",
    "pages": [
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">صحيفة دعوى مدنية (تعويض)</div>
    <div class="ent-sub">مقدمة إلى: محكمة دبي الابتدائية — الدوائر المدنية</div>
    <div class="ent-sub">من: مكتب ضفاف العدالة للمحاماة والاستشارات القانونية — دبي</div>
  </div>
  <div class="meta">
    <div>التاريخ: 22/10/2026</div>
    <div>المرجع: DA/CIV/2026/64</div>
  </div>
</div>
<table class="parties">
  <tr><th>المدعي</th><td>مازن إبراهيم العطار، وتنوب عنه المحامية/ ريم عبدالعزيز الجروان.</td></tr>
  <tr><th>المدعى عليه الأول</th><td>هشام توفيق البدري، قائد المركبة المتسببة في الحادث.</td></tr>
  <tr><th>المدعى عليها الثانية</th><td>شركة سنام الرمال للتأمين ش.م.ع، المؤمِّنة على مركبة المدعى عليه الأول بالوثيقة رقم 000000.</td></tr>
</table>
<h2>الوقائع</h2>
<ol>
  <li>بتاريخ 16/06/2026 نحو الساعة 21:40، تجاوز المدعى عليه الأول الإشارة الضوئية الحمراء عند تقاطع شارع أم سقيم مع شارع الوصل في دبي، فصدم مركبة المدعي (تقرير الحادث رقم 0000/2026، مرفق رقم 1).</li>
  <li>أُصيب المدعي بكسور في ساقه اليمنى وكاحله الأيمن، وبقي في المستشفى حتى 29/06/2026، وتخلف لديه عجز دائم جزئي بنسبة (15%) وفق التقرير الطبي (مرفق 2). وأدانت محكمة جنح السير المدعى عليه الأول بتاريخ 28/07/2026 في القضية رقم 3471 لسنة 2026 جنح سير، وغرّمته (10,000) درهم، وصار الحكم باتاً بعدم الطعن عليه وفق شهادة المحكمة المؤرخة 03/09/2026.</li>
</ol>
<h2>الأسانيد</h2>
<ol>
  <li>لوقوع الحادث بعد 01/06/2026 يسري عليه قانون المعاملات المدنية الصادر بالمرسوم بقانون اتحادي رقم (25) لسنة 2025، وتُلزم المادة (246) منه فاعل الإضرار بالغير بضمان الضرر، وتنص المادة (255) على أنه: "يُقدّر التعويض في جميع الأحوال بقدر ما لحق المضرور من ضرر وما فاته من كسب، بشرط أن يكون ذلك نتيجة محتملة للفعل الضار".</li>
  <li>وتلتزم المدعى عليها الثانية بالتعويض بصفتها المؤمِّنة من المسؤولية المدنية بعد مطالبة المؤمَّن له، عملاً بالمادة (965) من القانون ذاته.</li>
  <li>ويتقيد القاضي المدني بالحكم الجزائي في الوقائع التي فصل فيها وكان فصله فيها ضرورياً، ومنها خطأ المدعى عليه الأول، عملاً بالمادة (88) من قانون الإثبات في المعاملات المدنية والتجارية الصادر بالمرسوم بقانون اتحادي رقم (35) لسنة 2022.</li>
</ol>
<h2>الطلبات</h2>
<table class="grid">
  <tr><th>م</th><th>بند التعويض</th><th>المبلغ (درهم)</th></tr>
  <tr><td>1</td><td>نفقات العلاج والعملية الجراحية والعلاج الطبيعي</td><td>58,640</td></tr>
  <tr><td>2</td><td>الكسب الفائت: الأجر من 16/06/2026 حتى 15/10/2026 (4 أشهر × 19,500)</td><td>78,000</td></tr>
  <tr><td>3</td><td>التعويض عن العجز الدائم الجزئي (15%)</td><td>150,000</td></tr>
  <tr><td>4</td><td>التعويض عن الضرر الأدبي (البند (1) من المادة (254) من قانون المعاملات المدنية)</td><td>60,000</td></tr>
  <tr class="total"><td></td><td>الإجمالي، يُلزم به المدعى عليهما بالتضامن مع الرسوم والمصروفات وأتعاب المحاماة</td><td>346,640</td></tr>
</table>
<div class="sigline">وكيلة المدعي — المحامية/ ريم عبدالعزيز الجروان</div>
""",
            "marks": [
                {"id": "c7-p1-stamp-registry", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["قلم القيد", "نموذج تدريبي", "26/10/2026"], "top": 37, "left": 248, "width": 156,
                 "height": 90, "rotate": 8, "seed": 47,
                 "label_en": "Court registry date stamp (training sample)",
                 "text_ar": "قلم القيد — نموذج تدريبي — 26/10/2026"},
                {"id": "c7-p1-signature-lawyer", "type": "signature", "color": INK, "top": 990, "left": 110,
                 "width": 180, "height": 64, "rotate": -3, "seed": 107,
                 "label_en": "Signature of the claimant's lawyer"},
                {"id": "c7-p1-stamp-lawfirm", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["مكتب ضفاف العدالة للمحاماة", "Difaf Al Adala Advocates", "دبي — الإمارات"],
                 "top": 962, "left": 364, "width": 230, "height": 82, "rotate": -5, "seed": 53,
                 "label_en": "Law firm stamp", "text_ar": "مكتب ضفاف العدالة للمحاماة — دبي"},
            ],
        },
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">ملخص تقرير حادث مروري</div>
    <div class="ent-sub">الإدارة العامة للمرور — قسم الحوادث المرورية — دبي</div>
    <div class="ent-sub">نموذج تدريبي — ليس تقريراً رسمياً</div>
  </div>
  <div class="meta">
    <div>رقم التقرير: 0000/2026</div>
    <div>تاريخ الإصدار: 18/06/2026</div>
  </div>
</div>
<table class="parties">
  <tr><th>تاريخ الحادث</th><td>الثلاثاء 16/06/2026 — الساعة 21:40 — الطقس صحو والطريق مضاء</td></tr>
  <tr><th>الموقع</th><td>تقاطع شارع أم سقيم مع شارع الوصل، دبي (تقاطع منظم بإشارات ضوئية)</td></tr>
  <tr><th>نوع الحادث</th><td>تصادم جانبي بين مركبتين، نتج عنه إصابة بليغة</td></tr>
</table>
<h2>بيانات الأطراف</h2>
<table class="grid">
  <tr><th>البيان</th><th>الطرف الأول</th><th>الطرف الثاني</th></tr>
  <tr><td>قائد المركبة</td><td>هشام توفيق البدري</td><td>مازن إبراهيم العطار</td></tr>
  <tr><td>المركبة</td><td>خصوصي — دبي — 00000</td><td>خصوصي — الشارقة — 00000</td></tr>
  <tr><td>شركة التأمين</td><td>شركة سنام الرمال للتأمين ش.م.ع</td><td>تأمين شامل</td></tr>
  <tr><td>رقم الوثيقة</td><td>000000</td><td>000000</td></tr>
  <tr><td>الإصابات</td><td>لا توجد</td><td>كسور في الساق اليمنى</td></tr>
  <tr><td>المسؤولية</td><td>متسبب (100%)</td><td>غير متسبب</td></tr>
</table>
<h2>وصف الحادث</h2>
<p>أثناء سير المركبة الأولى على شارع أم سقيم باتجاه شارع الشيخ زايد، تجاوز قائدها الإشارة الضوئية وهي حمراء عند التقاطع مع شارع الوصل، فاصطدم بالجانب الأيسر للمركبة الثانية التي كانت تعبر التقاطع والإشارة خضراء لاتجاهها. وثبت ذلك من تسجيل كاميرا المراقبة عند التقاطع ومن أقوال شاهد عيان. ونُقل قائد المركبة الثانية بالإسعاف إلى مستشفى رواسي التخصصي.</p>
<h2>الإجراء المتخذ</h2>
<p>أُحيل الملف إلى نيابة السير والمرور بتاريخ 18/06/2026 لاتخاذ الإجراءات القانونية بحق قائد المركبة الأولى.</p>
<div class="sigline">ضابط التحقيق — الملازم أول/ حمد سيف الغفلي</div>
""",
            "marks": [
                {"id": "c7-p2-signature-officer", "type": "signature", "color": BLACK_INK, "top": 830, "left": 110,
                 "width": 170, "height": 62, "rotate": 4, "seed": 113,
                 "label_en": "Investigating officer's signature"},
                {"id": "c7-p2-stamp-police", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["قسم الحوادث المرورية", "نموذج تدريبي", "18/06/2026"], "top": 838, "left": 330,
                 "width": 160, "height": 94, "rotate": -9, "seed": 59,
                 "label_en": "Traffic accidents section stamp (training sample)",
                 "text_ar": "قسم الحوادث المرورية — نموذج تدريبي — 18/06/2026"},
            ],
        },
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مستشفى رواسي التخصصي</div>
    <div class="ent-sub">Rawasi Specialty Hospital — قسم جراحة العظام والمفاصل</div>
    <div class="ent-sub">دبي — ص.ب: 00000 — هاتف: 04 000 0000</div>
  </div>
  <div class="meta">
    <div>التاريخ: 08/10/2026</div>
    <div>رقم الملف: MR-000000</div>
  </div>
</div>
<h1 class="title">تقرير طبي نهائي (مقتطف)</h1>
<p class="center">يُعطى بناءً على طلب المريض لتقديمه إلى الجهات المختصة</p>
<table class="parties">
  <tr><th>اسم المريض</th><td>مازن إبراهيم العطار — 36 سنة — هوية رقم 784-1990-0000000-0</td></tr>
  <tr><th>تاريخ الدخول</th><td>16/06/2026 عن طريق قسم الطوارئ، إثر حادث مروري</td></tr>
  <tr><th>تاريخ الخروج</th><td>29/06/2026</td></tr>
</table>
<h2>التشخيص</h2>
<p>كسر مفتت في عظمتي القصبة والشظية بالساق اليمنى، وكسر في الكاحل الأيمن، مع رضوض متفرقة في الصدر والذراع اليسرى.</p>
<h2>العلاج</h2>
<p>أُجريت للمريض بتاريخ 17/06/2026 عملية رد مفتوح وتثبيت داخلي بمسمار نخاعي وشريحة ومسامير، ثم خضع لـ (36) جلسة علاج طبيعي من 06/07/2026 حتى 30/09/2026. ومُنح إجازة مرضية من 16/06/2026 حتى 15/10/2026.</p>
<h2>الحالة الراهنة والرأي الطبي</h2>
<p>التأم الكسر واستقرت الحالة، ويعاني المريض من تيبّس جزئي في مفصل الكاحل الأيمن ومحدودية في حركته، وعرج خفيف عند المشي. وهو لائق للعودة إلى عمله اعتباراً من 16/10/2026 مع تجنب الوقوف لفترات طويلة، وقد تخلف لديه عجز دائم جزئي.</p>
<p><b>نسبة العجز الدائم الجزئي في الطرف السفلي الأيمن:</b></p>
<div class="sigline">الطبيب المعالج — د. نادر سليم الخوري، استشاري جراحة العظام</div>
""",
            "marks": [
                {"id": "c7-p3-hand-disability", "type": "handwriting", "color": INK, "size": 24,
                 "text": "١٥٪ (خمسة عشر بالمئة)", "top": 641, "left": 318, "rotate": -3,
                 "label_en": "Doctor's handwritten permanent disability percentage",
                 "text_ar": "15% (خمسة عشر بالمئة)"},
                {"id": "c7-p3-signature-doctor", "type": "signature", "color": INK, "top": 738, "left": 115,
                 "width": 180, "height": 66, "rotate": -5, "seed": 127,
                 "label_en": "Treating doctor's signature"},
                {"id": "c7-p3-stamp-hospital", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["مستشفى رواسي التخصصي", "Rawasi Specialty Hospital", "قسم جراحة العظام — دبي"],
                 "top": 748, "left": 345, "width": 230, "height": 90, "rotate": 5, "seed": 61,
                 "label_en": "Hospital stamp", "text_ar": "مستشفى رواسي التخصصي — قسم جراحة العظام — دبي"},
            ],
        },
    ],
}
