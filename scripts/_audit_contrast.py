#!/usr/bin/env python3
"""فحص تباين الألوان وفق WCAG 2.1 AA — للنصوص العادية 4.5:1 وللنصوص الكبيرة 3:1."""
import re

ROOT = '/home/ubuntu/Nexluna/assets/css/style.css'
css = open(ROOT, encoding='utf-8').read()

def luminance(rgb):
    cs = []
    for v in rgb:
        v = v / 255.0
        v = v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        cs.append(v)
    return 0.2126 * cs[0] + 0.7152 * cs[1] + 0.0722 * cs[2]

def hex2rgb(h):
    h = h.strip()
    m = re.match(r'rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)', h)
    if m:
        return (int(float(m.group(1))), int(float(m.group(2))), int(float(m.group(3))))
    h = h.lstrip('#').lower()
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

# الأزواج المرشحة للفحص — تُقرأ القيم الفعلية من CSS (لضمان عدم تفكك الفحص عن التصميم)
def read_var(name):
    m = re.search(r'--' + name + r':\s*([^;]+);', css)
    return m.group(1).strip() if m else None

accent = read_var('accent') or '#14b8a6'
accent600 = read_var('accent-600') or '#0d9488'
primary = read_var('primary') or '#0f9488'
text = read_var('text') or '#0b1f24'
bg = read_var('bg') or '#f7f5ef'
# أفتح لون في تدرج العلامة: نلتقط stops من --grad-brand ونحسب التباين مع أصغرها لمعانًا
g = read_var('grad-brand') or '#0f9488'
grad_stops = re.findall(r'#[0-9a-fA-F]{6}', g)
lightest = max(grad_stops, key=lambda h: luminance(hex2rgb(h))) if grad_stops else '#0f9488'

dark_bg = read_var('bg') if False else '#071417'
dark_surface = '#0e2226'
dark_text = '#eef4f2'
dark_muted = '#8ba3a3'
pairs = [
    # (اسم, لون النص, لون الخلفية)
    ('نص أساسي --text على --bg', text, bg),
    ('نص مكتوم --text-muted على --bg', read_var('text-muted') or '#566b70', bg),
    ('نص أبيض على --accent (غير مسموح نصًا)', '#ffffff', accent),
    ('نص أبيض على --accent-600 (embed button)', '#ffffff', accent600),
    ('نص أبيض على تدرج العلامة (أفتح stop)', '#ffffff', lightest),
    ('نص --text على --surface بطاقة', text, '#ffffff'),
    ('نص chip على --surface-2', read_var('text-muted') or '#566b70', read_var('surface-2') or '#f2efe6'),
    ('نص معاد على --bg داكن', dark_text, dark_bg),
    ('نص مكتوم داكن على --surface داكن', dark_muted, dark_surface),
    ('نص white على --primary-700', '#ffffff', read_var('primary-700') or '#0b665e'),
    ('نص --primary-700 على خلفية بيضاء (btn-outline)', read_var('primary-700') or '#0b665e', '#ffffff'),
    ('نص hero على --nx-ink-deep (افتراضي)', '#ffffff', '#0f2b33'),
    ('chip.hero على خلفية شفافة بيضاء 8%', '#eef4f2', '#0f2b33'),
    ('نص .btn-primary على --primary (كبير فقط، 3:1)', '#ffffff', primary),
]

print('=== فحص التباين WCAG AA ===')
for name, fg, bg in pairs:
    f = hex2rgb(fg)
    b = hex2rgb(bg)
    cr = contrast(f, b)
    ok = '✓' if cr >= 4.5 else ('Δ' if cr >= 3.0 else '✗ FAIL')
    print(f'{ok} {name:48s} ratio={cr:.2f}')
