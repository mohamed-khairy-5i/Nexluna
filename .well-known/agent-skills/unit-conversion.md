# Skill: unit-conversion

تحويل قيمة رقمية بين وحدتين قياس ضمن نفس الفئة، بحساب حتمي دقيق يجري بالكامل داخل المتصفح. Convert a numeric value between two units of the same measurement category — deterministic, client-side, no server.

## كيفية الاستخدام (WebMCP)

الأداة مُسجّلة في كل صفحة عبر `navigator.modelContext.provideContext()`.

### الأداة: `convert_units`

المدخلات (inputSchema):

```json
{
  "category": "string (enum)",
  "from": "string (unit code)",
  "to": "string (unit code)",
  "value": "number"
}
```

### الأداة: `list_units`

تُعيد رموز الوحدات المتاحة لفئة (أو كل الفئات). Returns unit codes for a category (or all categories).

## الفئات المدعومة (categories)

- `length` — الطول: https://nexluna.netlify.app/converters/length.html
- `weight` — الوزن: https://nexluna.netlify.app/converters/weight.html
- `area` — المساحة: https://nexluna.netlify.app/converters/area.html
- `volume` — الحجم والسعة: https://nexluna.netlify.app/converters/volume.html
- `temperature` — درجة الحرارة: https://nexluna.netlify.app/converters/temperature.html
- `data` — البيانات الرقمية: https://nexluna.netlify.app/converters/data.html
- `speed` — السرعة: https://nexluna.netlify.app/converters/speed.html
- `time` — الوقت: https://nexluna.netlify.app/converters/time.html
- `pressure` — الضغط: https://nexluna.netlify.app/converters/pressure.html
- `energy` — الطاقة: https://nexluna.netlify.app/converters/energy.html
- `power` — القدرة: https://nexluna.netlify.app/converters/power.html
- `angle` — الزوايا: https://nexluna.netlify.app/converters/angle.html
- `fuel` — استهلاك الوقود: https://nexluna.netlify.app/converters/fuel.html
- `frequency` — التردد: https://nexluna.netlify.app/converters/frequency.html

## موارد ذات صلة

- Markdown pages: https://nexluna.netlify.app/md/index.md
- llms.txt: https://nexluna.netlify.app/llms.txt
- API catalog: https://nexluna.netlify.app/.well-known/api-catalog

Developer: Mohamed Khairy (MERN Stack & AI Engineer) — https://mokhairy.netlify.app/
