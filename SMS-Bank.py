import re

# آدرس فایل
file_path = "D:\\AVIDA\\CODE\\Bank\\SMS.txt"

# خواندن محتوای فایل
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.readlines()

# الگوهای جستجو برای پیدا کردن اعداد بعد از کلمات "واریز" و "برداشت"
deposit_pattern = r"واریز: ([\d,]+) ریال"
withdrawal_pattern = r"برداشت: ([\d,]+) ریال"

total_deposit = 0  # مقدار اولیه جمع کل واریزها
total_withdrawal = 0  # مقدار اولیه جمع کل برداشت‌ها

print("Deposits:")
# پردازش هر خط و پیدا کردن مقادیر واریز و برداشت
for line in content:
    deposit_match = re.search(deposit_pattern, line)
    if deposit_match:
        amount = deposit_match.group(1)
        # تبدیل مقدار به عدد صحیح و حذف کاماها
        amount_int = int(amount.replace(',', ''))
        total_deposit += amount_int
        print(amount)

print("\nWithdrawals:")
for line in content:
    withdrawal_match = re.search(withdrawal_pattern, line)
    if withdrawal_match:
        amount = withdrawal_match.group(1)
        # تبدیل مقدار به عدد صحیح و حذف کاماها
        amount_int = int(amount.replace(',', ''))
        total_withdrawal += amount_int
        print(amount)

# نمایش جمع کل
print("\nTotal Deposits: {:,} Rials".format(total_deposit))
print("Total Withdrawals: {:,} Rials".format(total_withdrawal))
