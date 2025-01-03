import pandas as pd
import os

# نام فایل Excel
file_name = 'library_data.xlsx'

# لیست کتاب‌های پیش‌فرض مناسب برای رنج سنی ۱۵ سال
default_books = [
    {'ID': 1, 'Book_Title': 'داستان‌های خیابانی', 'Author': 'مهدی یزدانی‌خرم', 'ISBN': '978-964-312-087-4'},
    {'ID': 2, 'Book_Title': 'چشم‌زن', 'Author': 'علی‌اشرف درویشیان', 'ISBN': '978-964-321-301-2'},
    {'ID': 3, 'Book_Title': 'برادران کارامازوف', 'Author': 'فئودور داستایفسکی', 'ISBN': '978-964-339-003-7'},
    {'ID': 4, 'Book_Title': 'دنیای سوخته', 'Author': 'رضا امیرخانی', 'ISBN': '978-964-367-034-1'},
    {'ID': 5, 'Book_Title': 'باغ وحش', 'Author': 'داوود غفاری', 'ISBN': '978-964-296-051-5'},
    {'ID': 6, 'Book_Title': 'عشق در دریا', 'Author': 'علی‌رضا قزوه', 'ISBN': '978-964-255-240-0'},
    {'ID': 7, 'Book_Title': 'مردی در جستجوی معنی', 'Author': 'ویکتور فرانکل', 'ISBN': '978-964-267-051-6'},
    {'ID': 8, 'Book_Title': 'شازده کوچولو', 'Author': 'آنتوان دو سنت‌اگزوپری', 'ISBN': '978-964-386-044-4'},
    {'ID': 9, 'Book_Title': 'سفر به سرزمین‌های ناشناخته', 'Author': 'محمود دولت‌آبادی', 'ISBN': '978-964-311-286-2'},
    {'ID': 10, 'Book_Title': 'گنجشک‌ها', 'Author': 'حمیدرضا شکارسری', 'ISBN': '978-964-340-120-0'},
]

# اگر فایل وجود ندارد، ایجاد می‌کنیم
if not os.path.exists(file_name):
    df = pd.DataFrame(columns=['ID', 'Student_Name', 'Book_ID', 'Book_Title', 'Author', 'ISBN', 'Operation', 'Date'])

    # اضافه کردن کتاب‌های پیش‌فرض به فایل
    for book in default_books:
        new_entry = {
            'ID': len(df) + 1,
            'Student_Name': None,
            'Book_ID': book['ID'],
            'Book_Title': book['Book_Title'],
            'Author': book['Author'],
            'ISBN': book['ISBN'],
            'Operation': 'موجود',
            'Date': None
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

    df.to_excel(file_name, index=False)


# تابع برای خواندن داده‌ها از Excel
def read_data():
    return pd.read_excel(file_name)


# تابع برای ذخیره داده‌ها به Excel
def save_data(df):
    df.to_excel(file_name, index=False)


# تابع برای امانت دادن کتاب
def lend_book(df):
    student_name = input("نام دانش آموز: ")
    book_id = int(input("شماره کتاب: "))

    # بررسی اینکه کتاب موجود است
    if not any(df['Book_ID'] == book_id):
        print("کتابی با این شماره پیدا نشد.")
        return df

    operation = 'امانت'
    date = pd.Timestamp.now()
    new_entry = {
        'ID': len(df) + 1,
        'Student_Name': student_name,
        'Book_ID': book_id,
        'Book_Title': df[df['Book_ID'] == book_id]['Book_Title'].values[0],
        'Author': df[df['Book_ID'] == book_id]['Author'].values[0],
        'ISBN': df[df['Book_ID'] == book_id]['ISBN'].values[0],
        'Operation': operation,
        'Date': date
    }

    # اضافه کردن رکورد جدید با pd.concat
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    return df


# تابع برای دریافت کتاب
def return_book(df):
    student_name = input("نام دانش آموز: ")
    book_id = int(input("شماره کتاب: "))

    # بررسی اینکه کتاب موجود است
    if not any(df['Book_ID'] == book_id):
        print("کتابی با این شماره پیدا نشد.")
        return df

    operation = 'تحویل'
    date = pd.Timestamp.now()
    new_entry = {
        'ID': len(df) + 1,
        'Student_Name': student_name,
        'Book_ID': book_id,
        'Book_Title': df[df['Book_ID'] == book_id]['Book_Title'].values[0],
        'Author': df[df['Book_ID'] == book_id]['Author'].values[0],
        'ISBN': df[df['Book_ID'] == book_id]['ISBN'].values[0],
        'Operation': operation,
        'Date': date
    }

    # اضافه کردن رکورد جدید با pd.concat
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    return df


# تابع برای حذف یک عملیات ثبت شده
def delete_operation(df):
    id_to_delete = int(input("شماره ID عملیات برای حذف: "))
    return df[df['ID'] != id_to_delete]


# تابع برای نمایش لیست کتاب‌های تحویل شده
def show_returned_books(df):
    returned_books = df[df['Operation'] == 'تحویل']
    print(returned_books)


# تابع برای نمایش لیست کتاب‌های موجود
def show_available_books(df):
    lent_books = df[df['Operation'] == 'امانت']['Book_ID']
    available_books = df[~df['Book_ID'].isin(lent_books) & (df['Operation'] == 'موجود')]

    if available_books.empty:
        print("هیچ کتابی در حال حاضر موجود نیست.")
    else:
        print(available_books[['Book_ID', 'Book_Title', 'Author', 'ISBN']].drop_duplicates())


# تابع برای نمایش کلی لیست عملیات‌های صورت پذیرفته
def show_all_operations(df):
    print(df.to_string(index=False))


# منوی اصلی
def main_menu():
    df = read_data()  # خواندن داده‌ها از فایل
    while True:
        print("\n--- منوی اصلی ---")
        print("1. امانت دادن کتاب")
        print("2. دریافت کتاب")
        print("3. حذف عملیات ثبت شده")
        print("4. نمایش لیست کتاب‌های تحویل شده")
        print("5. نمایش لیست کتاب‌های موجود")
        print("6. نمایش کلی لیست عملیات‌های صورت پذیرفته")
        print("7. خروج")

        choice = input("انتخاب خود را وارد کنید: ")

        if choice == '1':
            df = lend_book(df)
            save_data(df)

        elif choice == '2':
            df = return_book(df)
            save_data(df)

        elif choice == '3':
            df = delete_operation(df)
            save_data(df)

        elif choice == '4':
            show_returned_books(df)

        elif choice == '5':
            show_available_books(df)

        elif choice == '6':
            show_all_operations(df)

        elif choice == '7':
            print("خروج از برنامه...")
            break

        else:
            print("انتخاب نامعتبر است. لطفا دوباره تلاش کنید.")


if __name__ == "__main__":
    main_menu()
