import re
import jdatetime

input_path = "D:\\AVIDA\\CODE\\Bank\\SMS-Bank\\Input.txt"
output_path = "D:\\AVIDA\\CODE\\Bank\\SMS-Bank\\Output.txt"

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
                amount = int(re.search(deposit_pattern, line)
                             .group(1).replace(',', ''))
                transactions.append(('deposit', amount, current_date))
                grand_total_deposit += amount
            
            # استخراج برداشت
            elif re.search(withdrawal_pattern, line):
                amount = int(re.search(withdrawal_pattern, line)
                             .group(1).replace(',', ''))
                transactions.append(('withdrawal', amount, current_date))
                grand_total_withdrawal += amount

    if transactions:
        # مرتب‌سازی تراکنش‌ها بر اساس تاریخ
        transactions.sort(key=lambda x: x[2])
        
        current_period_start = transactions[0][2]
        period_deposits = 0
        period_withdrawals = 0

        # باز کردن فایل خروجی برای نوشتن
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write("\nگزارش دوره‌های 30 روزه:\n")
            for trans in transactions:
                trans_type, amount, date = trans

                # محاسبه تفاوت روزها
                if (date - current_period_start).days >= 30:
                    # نمایش تاریخ‌ها با فرمت فارسی
                    start = current_period_start.strftime("%Y/%m/%d")
                    end_date = current_period_start + jdatetime.timedelta(
                        days=29)
                    end = end_date.strftime("%Y/%m/%d")
                    output_file.write(f"\nپریود: {start} تا {end}\n")
                    output_file.write(f"جمع واریزها: {period_deposits:,} ریال\n")
                    output_file.write(f"جمع برداشت‌ها: {period_withdrawals:,} ریال\n")

                    # شروع دوره جدید
                    current_period_start += jdatetime.timedelta(days=30)
                    period_deposits = 0
                    period_withdrawals = 0

                # محاسبه جمع دوره
                if trans_type == 'deposit':
                    period_deposits += amount
                else:
                    period_withdrawals += amount

            # نمایش آخرین دوره
            start = current_period_start.strftime("%Y/%m/%d")
            end_date = current_period_start + jdatetime.timedelta(days=29)
            end = end_date.strftime("%Y/%m/%d")
            output_file.write(f"\nپریود: {start} تا {end}\n")
            output_file.write(f"جمع واریزها: {period_deposits:,} ریال\n")
            output_file.write(f"جمع برداشت‌ها: {period_withdrawals:,} ریال\n")

            # نمایش جمع کل
            output_file.write("\nنتیجه نهایی:\n")
            output_file.write(f"جمع کل واریزی‌ها: {grand_total_deposit:,} ریال\n")
            output_file.write(f"جمع کل برداشت‌ها: {grand_total_withdrawal:,} ریال\n")
            balance = grand_total_deposit - grand_total_withdrawal
            output_file.write(f"مانده نهایی: {balance:,} ریال\n")

    else:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.write("هیچ تراکنشی یافت نشد!\n")

except FileNotFoundError:
    print("خطا: فایل Input.txt یافت نشد!")
except Exception as e:
    print(f"خطای ناشناخته: {str(e)}")
