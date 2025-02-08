import re

# آدرس فایل
file_path = "D:\\AVIDA\\CODE\\Bank\\SMS.txt"

# خواندن محتوای فایل
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.readlines()

# الگوی جستجو برای پیدا کردن عدد بعد از کلمه "واریز"
pattern = r"واریز: ([\d,]+) ریال"

total_amount = 0  # مقدار اولیه جمع کل

# پردازش هر خط و پیدا کردن مقادیر مورد نظر
for line in content:
    match = re.search(pattern, line)
    if match:
        amount = match.group(1)
        # تبدیل مقدار به عدد صحیح و حذف کاماها
        amount_int = int(amount.replace(',', ''))
        total_amount += amount_int
        print(amount)

# نمایش جمع کل
print("Total Amount: {:,} Rials".format(total_amount))
