import re
import jdatetime
from jinja2 import Template
from weasyprint import HTML

input_path = "D:\\AVIDA\\CODE\\Bank\\SMS-Bank\\Input.txt"
html_output_path = "D:\\AVIDA\\CODE\\Bank\\SMS-Bank\\Output.html"
pdf_output_path = "D:\\AVIDA\\CODE\\Bank\\SMS-Bank\\Output.pdf"

deposit_pattern = r"واریز:\s*([\d,]+)\s*ریال"
withdrawal_pattern = r"برداشت:\s*([\d,]+)\s*ریال"
date_pattern = r"(\d{4}/\d{2}/\d{2})"

def parse_jalali_date(date_str):
    try:
        year, month, day = map(int, date_str.split('/'))
        return jdatetime.date(year, month, day)
    except Exception as e:
        print(f"خطا در پردازش تاریخ {date_str}: {str(e)}")
        return None

try:
    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    transactions = []
    current_date = None
    grand_total_deposit = 0
    grand_total_withdrawal = 0

    for line in content:
        line = line.strip()
        
        # استخراج تاریخ با فرمت 1403/11/20
        date_match = re.search(date_pattern, line)
        if date_match:
            current_date = parse_jalali_date(date_match.group(1))
            continue

        if current_date:
            # استخراج واریز
            if re.search(deposit_pattern, line):
                amount = int(re.search(deposit_pattern, line).group(1).replace(',', ''))
                transactions.append(('deposit', amount, current_date))
                grand_total_deposit += amount
            
            # استخراج برداشت
            elif re.search(withdrawal_pattern, line):
                amount = int(re.search(withdrawal_pattern, line).group(1).replace(',', ''))
                transactions.append(('withdrawal', amount, current_date))
                grand_total_withdrawal += amount

    if transactions:
        # مرتب‌سازی تراکنش‌ها بر اساس تاریخ
        transactions.sort(key=lambda x: x[2])

        periods = []
        current_period_start = transactions[0][2]
        while current_period_start <= transactions[-1][2]:
            period_end = current_period_start + jdatetime.timedelta(days=29)
            period_transactions = [t for t in transactions if current_period_start <= t[2] <= period_end]

            if period_transactions:
                period_deposits = sum(t[1] for t in period_transactions if t[0] == 'deposit')
                period_withdrawals = sum(t[1] for t in period_transactions if t[0] == 'withdrawal')

                periods.append({
                    'start': current_period_start.strftime("%Y/%m/%d"),
                    'end': period_end.strftime("%Y/%m/%d"),
                    'deposits': f"{period_deposits:,}",
                    'withdrawals': f"{period_withdrawals:,}"
                })

            current_period_start += jdatetime.timedelta(days=30)

        total_balance = grand_total_deposit - grand_total_withdrawal

        # قالب HTML
        html_template = """
        <!DOCTYPE html>
        <html lang="fa">
        <head>
            <meta charset="UTF-8">
            <title>گزارش تراکنش‌ها</title>
            <style>
                body { font-family: Tahoma; direction: rtl; text-align: right; background-color: rgb(52, 29, 99); }
                table { width: 80%; margin: auto; border-collapse: collapse; }
                th, td { border: 0.1mm solid #5cd3ec; padding: 12px; }
                th { background-color: #d21e8c; }
                .deposits { color: rgb(255, 255, 255); }
                .withdrawals { color: rgb(255, 255, 0); }
                .total { font-weight: bold; }
                h2 { text-align: center; color: #5cd3ec; } /* گزارش دوره‌های 30 روزه */
                h3 { text-align: center; color: rgb(39, 209, 172); } /* نتیجه نهایی */
                th { text-align: center; color: rgb(255, 255, 255); } /* xxxxxx */
                td { text-align: center; color: #5cd3ec; } /* xxxxxx */
/*                kd { text-align: center; color: rgb(200, 255, 0); } /* xxxxxx */
            </style>
        </head>
        <body>
            <h2>گزارش دوره‌های 30 روزه</h2>
            <table>
                <tr>
                    <th>دوره</th>
                    <th>جمع واریزها (ریال)</th>
                    <th>جمع برداشت‌ها (ریال)</th>
                </tr>
                {% for period in periods %}
                <tr>
                    <td>{{ period.start }} تا {{ period.end }}</td>
                    <td class="deposits">{{ period.deposits }}</td>
                    <td class="withdrawals">{{ period.withdrawals }}</td>
                </tr>
                {% endfor %}
            </table>
            <h2>نتیجه نهایی</h2>
            <table>
                <tr>
                    <td>جمع کل واریزی‌ها:</td>
                    <td class="deposits">{{ grand_total_deposit }}</td>
                </tr>
                <tr>
                    <td>جمع کل برداشت‌ها:</td>
                    <td class="withdrawals">{{ grand_total_withdrawal }}</td>
                </tr>
                <tr>
                    <td class="total">مانده نهایی:</td>
                    <td class="total">{{ total_balance }}</td>
                </tr>
            </table>
        </body>
        </html>
        """

        template = Template(html_template)
        rendered_html = template.render(
            periods=periods,
            grand_total_deposit=f"{grand_total_deposit:,}",
            grand_total_withdrawal=f"{grand_total_withdrawal:,}",
            total_balance=f"{total_balance:,}"
        )

        # ذخیره فایل HTML
        with open(html_output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(rendered_html)

        # تبدیل HTML به PDF با استفاده از WeasyPrint
        HTML(string=rendered_html).write_pdf(pdf_output_path)

        print("گزارش با موفقیت به فرمت‌های HTML و PDF ذخیره شد.")

    else:
        print("هیچ تراکنشی یافت نشد!")

except FileNotFoundError:
    print("خطا: فایل Input.txt یافت نشد!")
except Exception as e:
    print(f"خطای ناشناخته: {str(e)}")
