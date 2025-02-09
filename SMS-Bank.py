import re
<<<<<<< HEAD
import jdatetime
=======
import jdatetime  # کتابخانه برای کار با تاریخ شمسی
>>>>>>> 1beedcc (Refactor date handling to use jdatetime for Jalali date formatting and calculations)

file_path = "D:\\AVIDA\\CODE\\Bank\\SMS.txt"

deposit_pattern = r"واریز:\s*([\d,]+)\s*ریال"
withdrawal_pattern = r"برداشت:\s*([\d,]+)\s*ریال"
date_pattern = r"(\d{4}/\d{2}/\d{2})"

<<<<<<< HEAD
def parse_jalali_date(date_str):
    try:
        year, month, day = map(int, date_str.split('/'))
        return jdatetime.date(year, month, day)
    except Exception as e:
        print(f"خطا در پردازش تاریخ {date_str}: {str(e)}")
        return None
=======
# تابع تبدیل تاریخ شمسی به رشته‌ی قابل‌خواندن
def format_jalali_date(date_str):
    year, month, day = map(int, date_str.split('/'))
    jalali_date = jdatetime.date(year, month, day)
    return jalali_date.strftime("%Y/%m/%d")  # فرمت تاریخ شمسی
>>>>>>> 1beedcc (Refactor date handling to use jdatetime for Jalali date formatting and calculations)

try:
    with open(file_path, 'r', encoding='utf-8') as file:
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

<<<<<<< HEAD
    if transactions:
        # مرتب‌سازی تراکنش‌ها بر اساس تاریخ
        transactions.sort(key=lambda x: x[2])
        
        current_period_start = transactions[0][2]
        period_deposits = 0
        period_withdrawals = 0

        print("\n\u001b[1mگزارش دوره‌های 30 روزه:\u001b[0m")
        for trans in transactions:
            trans_type, amount, date = trans

            # محاسبه تفاوت روزها
            if (date - current_period_start).days >= 30:
                # نمایش تاریخ‌ها با فرمت فارسی
                start = current_period_start.strftime("%Y/%m/%d")
                end = (current_period_start + jdatetime.timedelta(days=29)).strftime("%Y/%m/%d")
                print(f"\n╭─ \u001b[33mپریود: {start} تا {end}\u001b[0m ─╮")
                print(f"│ • جمع واریزها: \u001b[32m{period_deposits:,}\u001b[0m ریال")
                print(f"│ • جمع برداشت‌ها: \u001b[31m{period_withdrawals:,}\u001b[0m ریال")
                print("╰─────────────────────────────────────────────────╯")
=======
        # استخراج برداشت
        withdrawal_match = re.search(withdrawal_pattern, line)
        if withdrawal_match and current_date:
            amount = int(withdrawal_match.group(1).replace(',', ''))
            transactions.append(("withdrawal", amount, current_date))

    # گروه‌بندی تراکنش‌ها در بازه‌های ۳۰ روزه
    if not transactions:
        print("No transactions found.")
    else:
        # پیدا کردن اولین تاریخ
        first_date = transactions[0][2]
        first_jalali = jdatetime.date(*map(int, first_date.split('/')))

        # ذخیره جمع واریزها و برداشت‌ها در هر بازه
        period_deposits = 0
        period_withdrawals = 0
        current_period_start = first_jalali

        print("Transactions per 30-day periods:")
        for transaction in transactions:
            type_, amount, date = transaction
            jalali_date = jdatetime.date(*map(int, date.split('/')))

            # اگر تراکنش در بازه‌ی ۳۰ روزه فعلی نباشد، نتایج را نمایش داده و بازه را به‌روزرسانی کنید
            if (jalali_date - current_period_start).days >= 30:
                period_end = current_period_start + jdatetime.timedelta(days=29)
                print(f"Period from {current_period_start.strftime('%Y/%m/%d')} to {period_end.strftime('%Y/%m/%d')}:")
                print(f"  Total Deposits: {period_deposits:,}")
                print(f"  Total Withdrawals: {period_withdrawals:,}")
                print("-" * 40)
>>>>>>> 1beedcc (Refactor date handling to use jdatetime for Jalali date formatting and calculations)

                # شروع دوره جدید
                current_period_start = current_period_start + jdatetime.timedelta(days=30)
                period_deposits = 0
                period_withdrawals = 0
<<<<<<< HEAD
=======
                current_period_start += jdatetime.timedelta(days=30)
>>>>>>> 1beedcc (Refactor date handling to use jdatetime for Jalali date formatting and calculations)

            # محاسبه جمع دوره
            if trans_type == 'deposit':
                period_deposits += amount
            else:
                period_withdrawals += amount

<<<<<<< HEAD
        # نمایش آخرین دوره
        start = current_period_start.strftime("%Y/%m/%d")
        end = (current_period_start + jdatetime.timedelta(days=29)).strftime("%Y/%m/%d")
        print(f"\n╭─ \u001b[33mپریود: {start} تا {end}\u001b[0m ─╮")
        print(f"│ • جمع واریزها: \u001b[32m{period_deposits:,}\u001b[0m ریال")
        print(f"│ • جمع برداشت‌ها: \u001b[31m{period_withdrawals:,}\u001b[0m ریال")
        print("╰─────────────────────────────────────────────────╯")

        # نمایش جمع کل
        print("\n\u001b[1m════════════════ نتیجه نهایی ════════════════\u001b[0m")
        print(f"\u001b[32mجمع کل واریزی‌ها: {grand_total_deposit:,} ریال\u001b[0m")
        print(f"\u001b[31mجمع کل برداشت‌ها: {grand_total_withdrawal:,} ریال\u001b[0m")
        print(f"\u001b[34mمانده نهایی: {grand_total_deposit - grand_total_withdrawal:,} ریال\u001b[0m")

    else:
        print("⚠️ هیچ تراکنشی یافت نشد!")
=======
        # نمایش نتایج برای آخرین بازه
        period_end = current_period_start + jdatetime.timedelta(days=29)
        print(f"Period from {current_period_start.strftime('%Y/%m/%d')} to {period_end.strftime('%Y/%m/%d')}:")
        print(f"  Total Deposits: {period_deposits:,}")
        print(f"  Total Withdrawals: {period_withdrawals:,}")
>>>>>>> 1beedcc (Refactor date handling to use jdatetime for Jalali date formatting and calculations)

except FileNotFoundError:
    print("\u001b[31mخطا: فایل SMS.txt یافت نشد!\u001b[0m")
except Exception as e:
    print(f"\u001b[31mخطای ناشناخته: {str(e)}\u001b[0m")