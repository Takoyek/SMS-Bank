import re

# آدرس فایل
file_path = "D:\\AVIDA\\CODE\\Bank\\SMS.txt"

# الگوهای جستجو برای پیدا کردن اعداد بعد از کلمات "واریز" و "برداشت"
deposit_pattern = r"واریز: ([\d,]+) ریال"
withdrawal_pattern = r"برداشت: ([\d,]+) ریال"

total_deposit = 0  # مقدار اولیه جمع کل واریزها
total_withdrawal = 0  # مقدار اولیه جمع کل برداشت‌ها

try:
    # خواندن محتوای فایل
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # پردازش هر خط و پیدا کردن مقادیر واریز و برداشت
    for line in content:
        deposit_match = re.search(deposit_pattern, line)
        withdrawal_match = re.search(withdrawal_pattern, line)

        if deposit_match:
            amount = deposit_match.group(1)
            total_deposit += int(amount.replace(',', ''))  # تبدیل به عدد و اضافه به جمع واریزها

        if withdrawal_match:
            amount = withdrawal_match.group(1)
            total_withdrawal += int(amount.replace(',', ''))  # تبدیل به عدد و اضافه به جمع برداشت‌ها

    # نمایش جمع کل
    print("Total Deposits: {:,} Rials".format(total_deposit))
    print("Total Withdrawals: {:,} Rials".format(total_withdrawal))

except FileNotFoundError:
    print("Error: File not found.")
except Exception as e:
    print(f"An error occurred: {e}")