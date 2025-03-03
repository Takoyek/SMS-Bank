import re
import datetime
import os
import jdatetime  # برای تبدیل تاریخ میلادی به شمسی

def read_input_file(input_file):
    # بررسی می‌کنیم که فایل ورودی وجود دارد یا خیر
    if not os.path.exists(input_file):
        print('Input file not found. Please check the file path.')
        exit()
    try:
        # باز کردن فایل ورودی و خواندن خطوط آن
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except IOError:
        print('Error reading the input file.')
        exit()

def extract_deposits(lines):
    deposits = []
    # الگوی عبارت منظم برای استخراج مبلغ و تاریخ
    pattern = r'(\d+)\s+هزار تومان\s+-\s+در تاریخ\s+([\d\-]+)'
    for line in lines:
        match = re.search(pattern, line)
        if match:
            amount = int(match.group(1))  # استخراج مبلغ
            date_str = match.group(2)     # استخراج تاریخ به صورت رشته
            # تبدیل رشته تاریخ به شیء datetime برای مرتب‌سازی
            try:
                date_parts = date_str.split('-')
                date_parts = [int(part) for part in date_parts]
                # فرض می‌کنیم قالب تاریخ به صورت روز-ماه-سال است
                date = datetime.date(year=date_parts[2], month=date_parts[1], day=date_parts[0])
            except ValueError:
                print(f'Invalid date format in line: {line.strip()}')
                continue
            # افزودن اطلاعات واریز به لیست
            deposits.append({'amount': amount, 'date': date, 'line': line.strip()})
    # مرتب‌سازی واریزها بر اساس تاریخ
    deposits.sort(key=lambda x: x['date'])
    # استخراج مبالغ و خطوط واریزها
    deposit_amounts = [d['amount'] for d in deposits]
    deposit_lines = [d['line'] for d in deposits]
    return deposit_amounts, deposit_lines

def get_previous_balance():
    while True:
        try:
            previous_balance = int(input('Mandeh Ghabli: '))
            return previous_balance
        except ValueError:
            print('Please enter a valid integer.')

def get_current_date():
    # دریافت تاریخ میلادی جاری
    gregorian_date = datetime.datetime.now()
    # تبدیل به تاریخ شمسی
    jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
    # استخراج سال، ماه و روز
    year = jalali_date.year
    month = jalali_date.month
    day = jalali_date.day
    # تبدیل ماه و روز به فرمت دو رقمی
    month_str = f'{month:02d}'
    day_str = f'{day:02d}'
    # بازگشت تاریخ به فرمت YYYY/MM/DD
    return f'{year}/{month_str}/{day_str}'

def calculate_totals(previous_balance, total_deposits):
    # محاسبه مانده کل حساب
    total_balance = previous_balance - total_deposits
    return total_balance

def write_output_file(output_file, deposit_lines, total_deposits, previous_balance, total_balance, current_date):
    output_lines = []
    output_lines.append('💳 واریز ها :\n')
    output_lines.append('____________________________________\n\n')
    # افزودن خطوط واریزها
    for line in deposit_lines:
        output_lines.append(line + '\n')
    output_lines.append('____________________________________\n')
    # افزودن جمع واریزها و مبلغ مانده از قبل
    output_lines.append(f'جمع واریز ها:  `{total_deposits}`\n')
    output_lines.append(f'مبلغ مانده از قبل:  `{previous_balance}`\n\n')
    # افزودن تاریخ و مانده کل حساب
    output_lines.append(f'در تاریخ:  {current_date}\n')
    output_lines.append(f'جمع کل مانده حساب شما:  `{total_balance}` هزار تومان\n')
    output_lines.append('.\n')
    try:
        # نوشتن محتوای خروجی در فایل خروجی
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(output_lines)
        print('Output file has been saved successfully.')
    except IOError:
        print('Error writing the output file.')

def main():
    input_file = r'D:\AVIDA\CODE\Invoice\Dep_in.txt'     # مسیر فایل ورودی
    output_file = r'D:\AVIDA\CODE\Invoice\Dep_out.txt'   # مسیر فایل خروجی

    lines = read_input_file(input_file)  # خواندن فایل ورودی
    deposit_amounts, deposit_lines = extract_deposits(lines)  # استخراج واریزها
    total_deposits = sum(deposit_amounts)  # محاسبه جمع واریزها
    previous_balance = get_previous_balance()  # دریافت مبلغ مانده از قبل از کاربر
    current_date = get_current_date()  # دریافت تاریخ جاری به صورت شمسی

    total_balance = calculate_totals(previous_balance, total_deposits)  # محاسبه مانده کل حساب
    write_output_file(output_file, deposit_lines, total_deposits, previous_balance, total_balance, current_date)  # نوشتن در فایل خروجی

if __name__ == '__main__':
    main()
