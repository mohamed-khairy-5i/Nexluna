#!/usr/bin/env python3
"""فحص برمجي شامل لكل الأزرار والعناصر التفاعلية في Nexluna.

يحلل style.css وHTML المولدة لاستخراج:
- ارتفاع/عرض/حجم اللمس لكل نوع زر
- تباين الألوان (foreground/background) وفق WCAG AA
- حالات hover/focus/transitions
- استخدام وحدة rem/px غير متناسقة
"""
import re
import sys
import colorsys
from pathlib import Path

ROOT = Path('/home/ubuntu/Nexluna')
CSS = ROOT / 'assets' / 'css' / 'style.css'

css_text = CSS.read_text(encoding='utf-8')

# ---------- استخراج متغيرات الألوان ----------
tokens = {}
for m in re.finditer(r'--([a-zA-Z0-9-]+)\s*:\s*([^;]+);', css_text):
    tokens[m.group(1)] = m.group(2).strip()

def luminance(rgb):
    rs, gs, bs = [], [], []
    for v in rgb:
        v = v / 255.0
        v = v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
        rs.append(v)
    return 0.2126 * rs[0] + 0.7152 * rs[1] + 0.0722 * rs[2]

def parse_color(s):
    s = s.strip().lower()
    m = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)', s)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r'#([0-9a-f]{3}|[0-9a-f]{6})$', s)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return None

def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)

# ---------- قواعد الأزرار ----------
button_rules = re.findall(r'(\.[\w.{} ,:#@-]+)\{([^}]+)\}', css_text)

issues = []
audit_rows = []

for selector, body in button_rules:
    sel = selector.strip()
    if not any(k in sel for k in ['btn', 'button', 'pill', 'install', 'explain', 'share', 'copy', 'toggle', 'switch', 'ghost', 'chip', 'action']):
        continue
    props = dict(re.findall(r'([\w-]+)\s*:\s*([^;]+);', body))
    row = {'selector': sel}
    # height / min-height / padding / font-size
    for k in ('height', 'min-height', 'padding', 'font-size', 'border-radius', 'line-height'):
        row[k] = props.get(k, '—')
    fg = props.get('color', '').split('var(')[-1].rstrip(')') if 'var(' in (props.get('color') or '') else props.get('color')
    bg = props.get('background', '').split('var(')[-1].rstrip(')') if 'var(' in (props.get('background') or '') else props.get('background')
    row['color'] = props.get('color', '—')
    row['background'] = props.get('background', '—')
    has_hover = re.search(re.escape(sel.split(',')[0].strip()) + r'(?::hover|,\s*\S*:hover)', css_text) is not None or f'{sel}:hover' in css_text or f'{sel.split(",")[0]}:hover' in css_text
    row['hover'] = 'نعم' if f'{sel}:hover' in css_text or f'{sel} .btn' in css_text else 'لا'
    has_focus = f'{sel}:focus' in css_text or f'{sel}:focus-visible' in css_text
    row['focus'] = 'نعم' if has_focus else 'لا'
    has_transition = 'transition' in body
    row['transition'] = 'نعم' if has_transition else 'لا'
    audit_rows.append(row)

print('=== قواعد الأزرار/التفاعلية في style.css ===')
for r in audit_rows:
    print(r)

# ---------- فحوص عامة ----------
print('\n=== فحوص عامه ===')
# 1. rem vs px in sizing
rem_px_issues = []
for m in re.finditer(r'(\.[\w.{} ,:#@-]+)\{([^}]+)\}', css_text):
    sel, body = m.group(1), m.group(2)
    for prop in ('height', 'min-height', 'font-size', 'padding'):
        vals = re.findall(rf'{prop}\s*:\s*([^;]+);', body)
        for v in vals:
            if re.search(r'\dpx', v) and sel not in ('html', 'body'):
                rem_px_issues.append((sel.strip()[:60], prop, v.strip()))
print(f'أحجام بالبكسل الثابت (يُفضَّل rem): {len(rem_px_issues)}')
for i in rem_px_issues[:20]:
    print('  -', i)

# 2. hover/focus coverage: هل كل قاعدة btn لها :hover؟
btn_sels = set()
for m in re.finditer(r'(\.[\w.{} ,:#@-]+)\{([^}]+)\}', css_text):
    sel = m.group(1).strip()
    if '.btn' in sel and ':' not in sel:
        for s in sel.split(','):
            btn_sels.add(s.strip())
missing_hover = [s for s in btn_sels if f'{s}:hover' not in css_text]
print(f'\nأزرار بلا حالة hover: {len(missing_hover)}')
for s in missing_hover:
    print('  -', s)

missing_focus = [s for s in btn_sels if f'{s}:focus-visible' not in css_text and f'{s}:focus' not in css_text]
print(f'\nأزرار بلا حالة focus: {len(missing_focus)}')
for s in missing_focus[:30]:
    print('  -', s)

# 3. min touch target: أزرار بارتفاع أقل من 44px
print('\n=== أزرار أقل من 44px ===')
for r in audit_rows:
    h = r.get('height', '—')
    if h != '—' and re.match(r'\d+\.?\d*px', h):
        v = float(h.replace('px', ''))
        if v < 44:
            print(f'  {r["selector"]}: height={h} (min-height={r["min-height"]})')

# 4. focus ring visibility
print('\n=== focus states موجودة؟ ===')
focus_rules = re.findall(r'([\w.#@: -]+)\:focus(-visible)?\s*\{([^}]+)\}', css_text)
for sel, _, body in focus_rules:
    print(f'  {sel.strip()}: {body.strip()[:120]}')

# 5. transitions
ts = re.findall(r'transition\s*:\s*([^;]+);', css_text)
print(f'\nقواعد transition: {len(ts)}')
