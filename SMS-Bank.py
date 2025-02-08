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
deposit_count = 0  # تعداد رکوردهای واریزها
withdrawal_count = 0  # تعداد رکوردهای برداشت‌ها

high_value_deposits = []  # لیست واریزهای با مقدار بالا
high_value_withdrawals = []  # لیست برداشت‌های با مقدار بالا

print("Deposits:")
# پردازش هر خط و پیدا کردن مقادیر واریز و برداشت
for line in content:
    deposit_match = re.search(deposit_pattern, line)
    if deposit_match:
        amount = deposit_match.group(1)
        # تبدیل مقدار به عدد صحیح و حذف کاماها
        amount_int = int(amount.replace(',', ''))
        total_deposit += amount_int
        deposit_count += 1
        print(amount)
        if amount_int > 20000000:
            high_value_deposits.append(amount)

print("\nWithdrawals:")
for line in content:
    withdrawal_match = re.search(withdrawal_pattern, line)
    if withdrawal_match:
        amount = withdrawal_match.group(1)
        # تبدیل مقدار به عدد صحیح و حذف کاماها
        amount_int = int(amount.replace(',', ''))
        total_withdrawal += amount_int
        withdrawal_count += 1
        print(amount)
        if amount_int > 20000000:
            high_value_withdrawals.append(amount)

# نمایش جمع کل و تعداد رکوردها
print("\nTotal Deposits: {:,} Rials".format(total_deposit))
print("Total Number of Deposit Records: {}".format(deposit_count))
print("Total Withdrawals: {:,} Rials".format(total_withdrawal))
print("Total Number of Withdrawal Records: {}".format(withdrawal_count))

# نمایش واریزهای با مقدار بالا
print("\nHigh Value Deposits (Greater than 20,000,000 Rials):")
for high_value_deposit in high_value_deposits:
    print(high_value_deposit)

# نمایش برداشت‌های با مقدار بالا
print("\nHigh Value Withdrawals (Greater than 20,000,000 Rials):")
for high_value_withdrawal in high_value_withdrawals:
    print(high_value_withdrawal)
