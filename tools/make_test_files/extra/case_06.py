# -*- coding: utf-8 -*-
"""Case 06 (fictional): a tenant company objects at the Rental Disputes Center, Dubai, to a rent
increase demanded at renewal and to the landlord's threat of eviction.

Deliberate challenges for the Case Reader:
  - Dubai Decree No. (43) of 2013 on rent increases is a real decree that is not in the official
    library, so the reader cannot check it and must say so;
  - the date the tenant received the landlord's notice appears only in a handwritten receipt note,
    and that date decides whether the 90-day notice under Article 14 was given (it was not);
  - the last day for a valid notice (lease expiry minus 90 days) is not printed and must be computed.

Everyone and everything here is invented. Every valid citation was read against the official
texts on 29 Oct 2026; Decree No. (43) of 2013 was read on the Dubai Legislation Portal.
"""
from cases import BLUE, PURPLE, INK, BLACK_INK  # noqa: F401

CASE = {
    "id": "case-06",
    "slug": "rent-increase",
    "title_en": "Tenancy claim: rent increase at renewal and eviction threat (Dubai)",
    "pages": [
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">صحيفة دعوى إيجارية</div>
    <div class="ent-sub">مقدمة إلى: مركز فض المنازعات الإيجارية — إمارة دبي</div>
    <div class="ent-sub">الموضوع: الاعتراض على زيادة الأجرة عند التجديد وعلى المطالبة بالإخلاء</div>
  </div>
  <div class="meta">
    <div>التاريخ: 20/10/2026</div>
    <div>المرجع: NG/ADM/2026/31</div>
  </div>
</div>
<table class="parties">
  <tr><th>المدعية</th><td>شركة نسيم الغاف لتجارة المواد الغذائية ذ.م.م (المستأجرة)، ويمثلها مديرها/ باسل عدنان الطحان.</td></tr>
  <tr><th>المدعى عليه</th><td>مبارك سالم بن عتيق القمزي (المؤجر)، مواطن، دبي.</td></tr>
  <tr><th>العين والعقد</th><td>مستودع رقم (9)، منطقة رأس الخور الصناعية الثانية، دبي، بعقد مسجل في (إيجاري) برقم 000000، من 01/01/2026 إلى 31/12/2026، بأجرة سنوية (210,000) درهم.</td></tr>
</table>
<h2>الوقائع</h2>
<ol>
  <li>وجّه المدعى عليه إلى المدعية إخطاراً مؤرخاً 24/09/2026 (مرفق رقم 2) بزيادة الأجرة السنوية عند التجديد إلى (252,000) درهم بنسبة (20%)، وأمهلها خمسة عشر يوماً من تاريخه للموافقة، وإلا اعتُبر العقد منتهياً في 31/12/2026 ووجب عليها الإخلاء.</li>
  <li>سُلِّم الإخطار باليد، ولم تتسلمه المدعية إلا في التاريخ الثابت بتأشيرة الاستلام المدونة عليه بخط اليد، بعد فوات مهلة التسعين يوماً، فردّت بتاريخ 15/10/2026 برفض الزيادة وعرضت التجديد بالأجرة ذاتها.</li>
</ol>
<h2>الأسانيد القانونية</h2>
<ol>
  <li>أوجبت المادة (14) من القانون رقم (26) لسنة 2007 بشأن تنظيم العلاقة بين مؤجري ومستأجري العقارات في إمارة دبي على من يرغب في تعديل شروط العقد إخطار الطرف الآخر قبل مدة لا تقل عن تسعين يوماً من انتهائه، فلا يُنتج الإخطار المتأخر أثره، ويتجدد العقد بذات شروطه عملاً بالمادة (6) من القانون ذاته.</li>
  <li>وإذا لم يتفق الطرفان على الأجرة، تحدد اللجنة الأجر العادل وفقاً للمادة (13) آخذة في الاعتبار المعايير الواردة في البند (2) من المادة (9). وتحدد المادة (1) من المرسوم رقم (43) لسنة 2013 بشأن تحديد الزيادة في بدل إيجار العقارات في إمارة دبي الزيادة القصوى بنسبة (5%) إذا قلّ بدل الإيجار عن متوسط أجر المثل بنسبة بين 11% و20%، ومتوسط أجر المثل للعين وفق مؤشر بدل الإيجارات (240,000) درهم، فتقل الأجرة عنه بنسبة (12.5%)، ولا تجاوز الأجرة الجديدة (220,500) درهم.</li>
  <li>لا يجوز طلب الإخلاء عند انتهاء العقد إلا في الحالات الواردة حصراً في البند (2) من المادة (25)، وبإخطار قبل اثني عشر شهراً على الأقل عن طريق الكاتب العدل أو البريد المسجل، وليس رفض الزيادة منها.</li>
</ol>
<h2>الطلبات</h2>
<ol>
  <li>عدم الاعتداد بالإخطار المؤرخ 24/09/2026، وتجديد العقد لمدة سنة بالأجرة ذاتها وقدرها (210,000) درهم.</li>
  <li>واحتياطياً: تحديد الأجرة العادلة لسنة التجديد بما لا يجاوز (220,500) درهم.</li>
  <li>رفض مطالبة المدعى عليه بالإخلاء في 31/12/2026، وإلزامه بالرسوم والمصروفات.</li>
</ol>
<div class="sigline">عن المدعية — المدير/ باسل عدنان الطحان</div>
""",
            "marks": [
                {"id": "c6-p1-stamp-registry", "type": "stamp", "kind": "oval", "color": PURPLE,
                 "lines": ["فض المنازعات الإيجارية", "قسم التسجيل — نموذج تدريبي", "20/10/2026"],
                 "top": 42, "left": 232, "width": 172, "height": 86, "rotate": -7, "seed": 37,
                 "label_en": "Rental Disputes Center registration stamp (training sample)",
                 "text_ar": "فض المنازعات الإيجارية — قسم التسجيل — نموذج تدريبي — 20/10/2026"},
                {"id": "c6-p1-signature-manager", "type": "signature", "color": INK, "top": 972, "left": 105,
                 "width": 180, "height": 66, "rotate": -4, "seed": 89,
                 "label_en": "Signature of the claimant's manager"},
                {"id": "c6-p1-stamp-tenant", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["نسيم الغاف لتجارة المواد الغذائية", "Naseem Al Ghaf Foodstuff Trading", "دبي — ذ.م.م"],
                 "top": 938, "left": 335, "width": 236, "height": 86, "rotate": 6, "seed": 41,
                 "label_en": "Claimant (tenant) company stamp",
                 "text_ar": "نسيم الغاف لتجارة المواد الغذائية — دبي — ذ.م.م"},
            ],
        },
        {
            "html": """
<div class="hdr">
  <div class="ent">
    <div class="ent-name">مبارك سالم بن عتيق القمزي</div>
    <div class="ent-sub">مالك العقار — دبي — ص.ب: 00000</div>
  </div>
  <div class="meta">
    <div>التاريخ: 24/09/2026</div>
    <div>بالتسليم باليد</div>
  </div>
</div>
<h1 class="title">إخطار بتعديل بدل الإيجار</h1>
<p>إلى: شركة نسيم الغاف لتجارة المواد الغذائية ذ.م.م (المستأجرة) — مستودع رقم (9)، منطقة رأس الخور الصناعية الثانية، دبي.</p>
<p><b>الموضوع: تعديل بدل الإيجار عند تجديد عقد الإيجار المسجل في نظام (إيجاري) برقم 000000.</b></p>
<p>تحية طيبة وبعد،</p>
<p>بالإشارة إلى عقد إيجار العين المذكورة أعلاه، الذي تنتهي مدته في 31/12/2026 بأجرة سنوية قدرها (210,000) درهم، نخطركم برغبتنا في تعديل بدل الإيجار السنوي عند التجديد ليصبح (252,000) درهم، وذلك عملاً بالمادة (14) من القانون رقم (26) لسنة 2007 بشأن تنظيم العلاقة بين مؤجري ومستأجري العقارات في إمارة دبي.</p>
<p>وعليه نرجو تأكيد موافقتكم كتابةً وتوقيع عقد التجديد خلال خمسة عشر يوماً من تاريخ هذا الإخطار. وفي حال عدم الموافقة خلال هذه المهلة، يُعتبر العقد منتهياً بانتهاء مدته في 31/12/2026، وعليكم إخلاء العين المؤجرة وتسليمها خالية من الشواغل في ذلك التاريخ، وإلا سنتخذ الإجراءات القانونية اللازمة لإخلائكم.</p>
<p>وتفضلوا بقبول فائق الاحترام،</p>
<div class="sigline">المؤجر — مبارك سالم بن عتيق القمزي</div>
""",
            "marks": [
                {"id": "c6-p2-signature-landlord", "type": "signature", "color": INK, "top": 552, "left": 90,
                 "width": 180, "height": 68, "rotate": -3, "seed": 97, "label_en": "Landlord's signature"},
                {"id": "c6-p2-hand-receipt", "type": "handwriting", "color": BLACK_INK, "size": 22,
                 "text": "استلمت الأصل بتاريخ ١٢/١٠/٢٠٢٦ — الاستقبال / ريم", "top": 800, "left": 300, "rotate": -3,
                 "label_en": "Tenant staff's handwritten receipt note, with the date the notice was received",
                 "text_ar": "استلمت الأصل بتاريخ 12/10/2026 — الاستقبال / ريم"},
                {"id": "c6-p2-signature-receiver", "type": "signature", "color": BLACK_INK, "top": 850, "left": 400,
                 "width": 140, "height": 56, "rotate": -6, "seed": 101,
                 "label_en": "Tenant staff's signature on the receipt"},
                {"id": "c6-p2-stamp-tenant", "type": "stamp", "kind": "rect", "color": BLUE,
                 "lines": ["نسيم الغاف لتجارة المواد الغذائية", "ذ.م.م — دبي"], "top": 860, "left": 90,
                 "width": 230, "height": 80, "rotate": -5, "seed": 43,
                 "label_en": "Tenant company stamp on the receipt",
                 "text_ar": "نسيم الغاف لتجارة المواد الغذائية — ذ.م.م — دبي"},
            ],
        },
    ],
}
