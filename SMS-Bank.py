import re
from datetime import datetime, timedelta
import jdatetime

# آدرس فایل
file_path = "D:\\AVIDA\\CODE\\Bank\\SMS.txt"

# خواندن محتوای فایل
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()  # خواندن تمام محتوا به عنوان یک رشته

# الگوی جستجو برای پیدا کردن تراکنش‌ها
transaction_pattern = r"\*بانک تجارت\*[\s\S]*?(\d{4}/\d{2}/\d{2})[\s\S]*?(واریز: ([\d,]+) ریال|برداشت: ([\d,]+) ریال)"

# تبدیل تاریخ‌های شمسی به میلادی
def jalali_to_gregorian(jalali_date):
    jdate = jdatetime.datetime.strptime(jalali_date, "%Y/%m/%d")
    gdate = jdate.togregorian()
    return gdate

transactions = []

# یافتن تمام تراکنش‌ها
matches = re.findall(transaction_pattern, content)

for match in matches:
    date_str, _, deposit_str, withdrawal_str = match
    date = jalali_to_gregorian(date_str)
    
    if deposit_str:
        amount = int(deposit_str.replace(',', ''))
        transactions.append((date, "deposit", amount))
    
    if withdrawal_str:
        amount = int(withdrawal_str.replace(',', ''))
        transactions.append((date, "withdrawal", amount))

# بررسی تعداد تراکنش‌ها
if not transactions:
    print("هیچ تراکنشی پیدا نشد. لطفاً مطمئن شوید که فرمت فایل ورودی صحیح است.")
    exit()

# محاسبه و نمایش جمع کل و تعداد رکوردها در هر ۳۰ روز
start_date = min(t[0] for t in transactions)
end_date = max(t[0] for t in transactions)
current_date = start_date

while current_date <= end_date:
    next_date = current_date + timedelta(days=30)
    deposit_sum = sum(t[2] for t in transactions if t[0] >= current_date and t[0] < next_date and t[1] == "deposit")
    withdrawal_sum = sum(t[2] for t in transactions if t[0] >= current_date and t[0] < next_date and t[1] == "withdrawal")
    deposit_count = sum(1 for t in transactions if t[0] >= current_date and t[0] < next_date and t[1] == "deposit")
    withdrawal_count = sum(1 for t in transactions if t[0] >= current_date and t[0] < next_date and t[1] == "withdrawal")
    
    # نمایش تاریخ‌ها با فرمت "Month Day, Year"
    print(f"From {current_date.strftime('%B %d, %Y')} to {next_date.strftime('%B %d, %Y')}:")
    print(f"  Total Deposits: {deposit_sum:,} Rials (Count: {deposit_count})")
    print(f"  Total Withdrawals: {withdrawal_sum:,} Rials (Count: {withdrawal_count})\n")
    
    current_date = next_date
