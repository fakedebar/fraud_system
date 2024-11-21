import os

def process_file(filepath):
    """
    دالة لتحليل الملف وتحديد المعاملات المشبوهة.
    """
    result_filepath = os.path.join(app.config['RESULT_FOLDER'], os.path.basename(filepath))

    # تعريف المعاملات المشبوهة
    suspicious_transactions = []

    # حد معين للمبلغ لتحديد المعاملة المشبوهة
    SUSPICIOUS_AMOUNT = 10000
    SUSPICIOUS_KEYWORDS = ['fraud', 'suspicious', 'illegal']

    with open(filepath, 'r') as f, open(result_filepath, 'w') as result_file:
        result_file.write("=== Suspicious Transactions Analysis ===\n")
        
        for line_number, line in enumerate(f, start=1):
            # تقسيم السطر إلى أجزاء (نفترض أنه يتبع صيغة معينة مثل: ID, Name, Amount, Description)
            parts = line.strip().split(',')
            if len(parts) < 2:
                continue  # تجاوز السطر إذا لم يكن لديه 4 أعمدة على الأقل
            
            transaction_id = parts[0]
            transaction_name = parts[1]
            try:
                amount = float(parts[2])
            except ValueError:
                amount = 0  # إذا لم يكن الرقم قابلاً للتحويل، اعتبره 0
            
            description = parts[3]

            # التحقق من الشروط
            if amount > SUSPICIOUS_AMOUNT or any(keyword in description.lower() for keyword in SUSPICIOUS_KEYWORDS):
                suspicious_transactions.append({
                    'line': line_number,
                    'id': transaction_id,
                    'name': transaction_name,
                    'amount': amount,
                    'description': description
                })
        
        # كتابة النتائج إلى الملف الناتج
        if suspicious_transactions:
            for txn in suspicious_transactions:
                result_file.write(f"Line {txn['line']}: Transaction ID: {txn['id']}, "
                                  f"Name: {txn['name']}, Amount: {txn['amount']}, "
                                  f"Description: {txn['description']}\n")
        else:
            result_file.write("No suspicious transactions found.\n")
        
        result_file.write("\n=== Original Content ===\n")
        f.seek(0)  # إعادة مؤشر الملف للبداية
        result_file.write(f.read())
    
    return result_filepath