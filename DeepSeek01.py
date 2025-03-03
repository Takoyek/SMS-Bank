import re
import jdatetime
from jinja2 import Template
from weasyprint import HTML
from datetime import datetime

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
        
        date_match = re.search(date_pattern, line)
        if date_match:
            current_date = parse_jalali_date(date_match.group(1))
            continue

        if current_date:
            if re.search(deposit_pattern, line):
                amount = int(re.search(deposit_pattern, line).group(1).replace(',', ''))
                transactions.append(('deposit', amount, current_date))
                grand_total_deposit += amount
            
            elif re.search(withdrawal_pattern, line):
                amount = int(re.search(withdrawal_pattern, line).group(1).replace(',', ''))
                transactions.append(('withdrawal', amount, current_date))
                grand_total_withdrawal += amount

    if transactions:
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
                    'deposits': period_deposits,
                    'withdrawals': period_withdrawals
                })

            current_period_start += jdatetime.timedelta(days=30)

        total_balance = grand_total_deposit - grand_total_withdrawal
        generated_date = jdatetime.date.today().strftime("%Y/%m/%d")
        generated_time = datetime.now().strftime("%H:%M:%S")

        html_template = """
        <!DOCTYPE html>
        <html lang="fa" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>گزارش مالی حرفه‌ای | Avida Bank</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
            <style>
                @font-face {
                    font-family: 'IRANSans';
                    src: url('https://cdn.jsdelivr.net/gh/rastikerdar/iran-sans-font@5/dist/woff2/IRANSansWeb.woff2') format('woff2');
                }
                
                body {
                    font-family: 'IRANSans', Tahoma, sans-serif;
                    background: #f8f9fa;
                    margin: 0;
                    padding: 40px 0;
                }
                
                .container {
                    max-width: 1000px;
                    margin: 0 auto;
                    background: white;
                    box-shadow: 0 0 30px rgba(0,0,0,0.1);
                    border-radius: 15px;
                    overflow: hidden;
                }
                
                .header {
                    background: linear-gradient(135deg, #2c3e50, #3498db);
                    color: white;
                    padding: 40px 30px;
                    text-align: center;
                }
                
                .logo {
                    width: 120px;
                    margin-bottom: 20px;
                }
                
                .report-title {
                    font-size: 28px;
                    margin: 0;
                    letter-spacing: 2px;
                }
                
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 30px 0;
                }
                
                th {
                    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
                    color: #2c3e50;
                    padding: 18px;
                    font-size: 15px;
                    border-bottom: 3px solid #dee2e6;
                }
                
                td {
                    padding: 15px;
                    border-bottom: 1px solid #dee2e6;
                    font-size: 14px;
                }
                
                tr:hover {
                    background-color: #f8f9fa;
                }
                
                .deposit-amount {
                    color: #28a745;
                    font-weight: 600;
                }
                
                .withdrawal-amount {
                    color: #dc3545;
                    font-weight: 600;
                }
                
                .total-card {
                    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
                    border-radius: 10px;
                    padding: 25px;
                    margin: 30px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                }
                
                .total-item {
                    text-align: center;
                }
                
                .total-label {
                    color: #6c757d;
                    font-size: 14px;
                    margin-bottom: 8px;
                }
                
                .total-value {
                    font-size: 22px;
                    font-weight: 700;
                }
                
                .footer {
                    background: #2c3e50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    font-size: 12px;
                }
                
                .period-range {
                    color: #6c757d;
                    font-size: 13px;
                }
                
                .badge {
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-size: 12px;
                }
                
                .badge-success {
                    background: #d4edda;
                    color: #155724;
                }
                
                .badge-danger {
                    background: #f8d7da;
                    color: #721c24;
                }
                
                @media print {
                    body {
                        padding: 0;
                    }
                    .container {
                        box-shadow: none;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 class="report-title">گزارش تراکنش‌های مالی</h1>
                    <div class="report-subtitle">بانک تجارت آویدا</div>
                </div>
                
                <div style="padding: 30px">
                    <table>
                        <thead>
                            <tr>
                                <th>دوره زمانی</th>
                                <th>مجموع واریزها</th>
                                <th>مجموع برداشت‌ها</th>
                                <th>وضعیت</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for period in periods %}
                            <tr>
                                <td>
                                    <div class="period-range">{{ period.start }} تا {{ period.end }}</div>
                                </td>
                                <td class="deposit-amount">{{ "{:,}".format(period.deposits) }} ریال</td>
                                <td class="withdrawal-amount">{{ "{:,}".format(period.withdrawals) }} ریال</td>
                                <td>
                                    {% if period.deposits > period.withdrawals %}
                                    <span class="badge badge-success">
                                        <i class="fas fa-arrow-up"></i> مثبت
                                    </span>
                                    {% else %}
                                    <span class="badge badge-danger">
                                        <i class="fas fa-arrow-down"></i> منفی
                                    </span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                    
                    <div class="total-card">
                        <div class="total-item">
                            <div class="total-label">کل واریزی‌ها</div>
                            <div class="total-value deposit-amount">{{ "{:,}".format(grand_total_deposit) }} ریال</div>
                        </div>
                        <div class="total-item">
                            <div class="total-label">کل برداشت‌ها</div>
                            <div class="total-value withdrawal-amount">{{ "{:,}".format(grand_total_withdrawal) }} ریال</div>
                        </div>
                        <div class="total-item">
                            <div class="total-label">مانده نهایی</div>
                            <div class="total-value" style="color: #2c3e50">{{ "{:,}".format(total_balance) }} ریال</div>
                        </div>
                    </div>
                </div>
                
                <div class="footer">
                    <div>تاریخ تولید گزارش: {{ generated_date }} - ساعت {{ generated_time }}</div>
                    <div style="margin-top: 8px">Avida Bank - کلیه حقوق محفوظ است © ۱۴۰۳</div>
                </div>
            </div>
        </body>
        </html>
        """

        template = Template(html_template)
        rendered_html = template.render(
            periods=periods,
            grand_total_deposit=grand_total_deposit,
            grand_total_withdrawal=grand_total_withdrawal,
            total_balance=total_balance,
            generated_date=generated_date,
            generated_time=generated_time
        )

        with open(html_output_path, 'w', encoding='utf-8') as output_file:
            output_file.write(rendered_html)

        HTML(string=rendered_html).write_pdf(
            pdf_output_path,
            stylesheets=["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"]
        )

        print("گزارش حرفه‌ای با موفقیت تولید شد!")

    else:
        print("هیچ تراکنشی یافت نشد!")

except FileNotFoundError:
    print("خطا: فایل ورودی یافت نشد!")
except Exception as e:
    print(f"خطای سیستمی: {str(e)}")