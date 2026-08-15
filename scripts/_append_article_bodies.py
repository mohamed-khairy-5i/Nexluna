"""Append missing Arabic article bodies (area, fuel) to build_blog.py ARTICLES entries."""
import re

ROOT = None


def main():
    path = "build_blog.py"
    src = open(path, encoding="utf-8").read()

    area_body = '''<p>تُعدّ وحدات قياس المساحات من أكثر ما يسبّب ارتباكًا في التعاملات العقارية والأراضي الزراعية، خاصة في مصر والوطن العربي حيث يُستخدم الفدّان والقيراط والسهم والدونم إلى جانب الأكر والهكتار الدوليين.</p>
        <h2>الفدّان المصري مقابل الأكر الدولي</h2>
        <p>الفدّان وحدة مصرية تقليدية تساوي 4200.833 مترًا مربعًا تقريبًا، بينما الأكر الدولي (Acre) المستخدم في الولايات المتحدة وبريطانيا يساوي 4046.856 مترًا مربعًا. الفرق بينهما نحو 3.8%، وهو فرق كافٍ للتأثير على حسابات الأسعار والمساحات في العقود.</p>
        <h2>أهم الوحدات في المنطقة</h2>
        <table>
          <thead><tr><th>الوحدة</th><th>القيمة بالمتر المربع</th></tr></thead>
          <tbody>
            <tr><td>الفدّان</td><td>4200.833</td></tr>
            <tr><td>القيراط (المصري)</td><td>175.03</td></tr>
            <tr><td>السهم</td><td>7.29</td></tr>
            <tr><td>الدونم</td><td>1000</td></tr>
            <tr><td>الهكتار</td><td>10,000</td></tr>
            <tr><td>الأكر</td><td>4046.856</td></tr>
          </tbody>
        </table>
        <p>حوّل بين أي من هذه الوحدات بدقة عبر <a href="/converters/area.html">محول المساحات من Nexluna</a>.</p>'''

    fuel_body = '''<p>تُقاس كفاءة استهلاك الوقود بثلاث اتفاقيات رئيسية حول العالم، وكل منها يعكس طريقة تفكير مختلفة: المسافة لكل لتر في الشرق الأوسط وأوروبا كثيرًا، والمسافة لكل غالون في أمريكا وبريطانيا، وحجم الوقود لكل مسافة (لتر/100 كم) في معظم أوروبا.</p>
        <h2>الغولون الأمريكي مقابل البريطاني</h2>
        <p>الغالون الأمريكي يساوي 3.785 لترًا، بينما الغالون البريطاني (الإمبراطوري) يساوي 4.546 لترًا. لذلك فإن رقم «30 mpg» أمريكي يعادل نحو 36 mpg بريطانيًا — نفس الاستهلاك الحقيقي برقمين مختلفين.</p>
        <h2>قواعد التحويل الأساسية</h2>
        <table>
          <thead><tr><th>من</th><th>إلى</th><th>القاعدة</th></tr></thead>
          <tbody>
            <tr><td>كم/لتر</td><td>mpg أمريكي</td><td>× 2.352</td></tr>
            <tr><td>لتر/100 كم</td><td>كم/لتر</td><td>100 ÷ القيمة</td></tr>
            <tr><td>mpg أمريكي</td><td>l/100km</td><td>235.215 ÷ القيمة</td></tr>
          </tbody>
        </table>
        <p>قارن بين كل هذه الاتفاقيات فورًا عبر <a href="/converters/fuel.html">محول استهلاك الوقود من Nexluna</a>.</p>'''

    def insert(slug, body):
        nonlocal src
        # Find the article dict in ARTICLES and append body key after 'excerpt'
        start = src.find('(\n        "slug": "%s"' % slug)
        if start == -1:
            print("not found:", slug)
            return
        end = src.find('"excerpt":', start)
        if end == -1:
            print("no excerpt:", slug)
            return
        end = src.find("\n", end) + 1
        if '"body"' in src[src.find(']', start, start + 100000) and start:src.find('",\n    },', end + 300000)]:
            print("skip, body exists:", slug)
            return
        insertion = f'        "body": \'{body}\','
        src = src[:end] + insertion + "\n" + src[end:]
        print("inserted body for:", slug)

    insert("area-measurement-guide", area_body)
    insert("fuel-economy-units", fuel_body)

    open(path, "w", encoding="utf-8").write(src)


if __name__ == "__main__":
    main()
