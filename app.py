from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

CURRENT_DATE = "1405/04/30"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>توربوVPN | مینی‌اپ</title>
    <style>
        body {
            background-color: #0b1120;
            color: #ffffff;
            font-family: Tahoma, sans-serif;
            margin: 0;
            padding-bottom: 70px;
        }
        .header {
            text-align: center;
            padding: 15px;
            font-size: 15px;
            color: #94a3b8;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .card {
            background: rgba(30, 41, 59, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 18px;
            margin: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .card h3 {
            margin-top: 0;
            font-size: 16px;
            color: #38bdf8;
        }
        .plan-item, .service-item {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
        }
        .search-input {
            flex: 1;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 10px;
            color: #fff;
            font-family: Tahoma, sans-serif;
        }
        .badge-active {
            background: rgba(34, 197, 94, 0.2);
            color: #4ade80;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        .nav-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: #060913;
            display: flex;
            justify-content: space-around;
            padding: 12px 0;
            border-top: 1px solid rgba(255,255,255,0.08);
        }
        .nav-item {
            color: #94a3b8;
            text-align: center;
            font-size: 13px;
            cursor: pointer;
        }
        .nav-item.active {
            color: #38bdf8;
            font-weight: bold;
        }
        .btn-action {
            background: #0284c7;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-family: Tahoma, sans-serif;
            font-size: 13px;
        }
        .btn-copy {
            background: #10b981;
            color: white;
            border: none;
            padding: 6px 12px;
            border-radius: 6px;
            cursor: pointer;
            font-family: Tahoma, sans-serif;
            font-size: 12px;
            margin-right: 5px;
        }
        .tab-content {
            display: none;
        }
        .tab-content.active {
            display: block;
        }
        .info-box {
            background: rgba(15, 23, 42, 0.8);
            padding: 12px;
            border-radius: 10px;
            margin-top: 10px;
            border: 1px dashed rgba(56, 189, 248, 0.3);
        }
        .upload-section {
            margin-top: 15px;
            background: rgba(15, 23, 42, 0.8);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .file-input {
            width: 100%;
            margin-top: 8px;
            color: #94a3b8;
            font-family: Tahoma, sans-serif;
        }
    </style>
</head>
<body>

    <div class="header">توربوVPN | پنل کاربری</div>

    <!-- تب حساب کاربری -->
    <div id="tab-account" class="tab-content">
        <div class="card">
            <h3>حساب کاربری</h3>
            <p>موجودی کیف پول: <span id="balance" style="color: #4ade80; font-weight: bold;">بارگذاری...</span></p>
            <p>نوع کاربری: <span id="user_type">عادی</span></p>
            <p>تاریخ عضویت: <span id="join_date">1405/04/30</span></p>
        </div>
    </div>

    <!-- تب خرید و کارت به کارت + آپلود فیش -->
    <div id="tab-buy" class="tab-content active">
        <div class="card">
            <h3>خرید سرویس جدید (۳ پلن اصلی)</h3>
            <div id="plans-container"></div>
        </div>

        <!-- بخش اطلاعات کارت و آپلود فیش -->
        <div class="card">
            <h3>💳 کارت به کارت و ارسال فیش</h3>
            <div class="info-box">
                <p><strong>بانک:</strong> نام بانک شما</p>
                <p><strong>شماره کارت:</strong> <span style="font-family: monospace; color: #facc15;">6037XXXXXXXXXXXXXXXX</span> 
                    <button class="btn-copy" onclick="copyText('6037XXXXXXXXXXXXXXXX')">کپی شماره کارت</button>
                </p>
                <p><strong>نام صاحب حساب:</strong> نام شما</p>
            </div>

            <!-- بخش آپلود فیش داخل برنامه -->
            <div class="upload-section">
                <label for="receipt-file" style="font-size: 13px; color: #38bdf8; display: block; margin-bottom: 5px;">📤 آپلود تصویر فیش واریزی:</label>
                <input type="file" id="receipt-file" class="file-input" accept="image/*">
                <button class="btn-action" style="margin-top: 12px; width: 100%;" onclick="uploadReceipt()">ارسال فیش برای بررسی</button>
            </div>
        </div>
    </div>

    <!-- تب سرویس‌های من -->
    <div id="tab-services" class="tab-content">
        <div class="card">
            <div class="search-box">
                <input type="text" class="search-input" placeholder="جستجو در نام سرویس...">
                <button class="btn-action">جستجو</button>
            </div>
            <h3 style="font-size: 14px; color: #94a3b8; margin-bottom: 10px;">📋 اشتراک‌های فعال</h3>
            <div class="service-item">
                <div>
                    <strong style="font-size: 14px;">سرویس تست</strong><br>
                    <small style="color: #94a3b8;">you - الماس (حجمی فول تانل)</small>
                </div>
                <span class="badge-active">● فعال</span>
            </div>
        </div>
    </div>

    <!-- تب خانه -->
    <div id="tab-home" class="tab-content">
        <div class="card">
            <h3>خوش آمدید</h3>
            <p>به پنل توربوVPN خوش آمدید.</p>
        </div>
    </div>

    <!-- منوی پایین -->
    <div class="nav-bar">
        <div class="nav-item" onclick="switchTab('home', this)">خانه</div>
        <div class="nav-item active" onclick="switchTab('buy', this)">خرید</div>
        <div class="nav-item" onclick="switchTab('services', this)">سرویس‌ها</div>
        <div class="nav-item" onclick="switchTab('account', this)">حساب</div>
    </div>

    <script>
        function switchTab(tabName, element) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            document.getElementById('tab-' + tabName).classList.add('active');
            element.classList.add('active');
        }

        function copyText(text) {
            navigator.clipboard.writeText(text).then(() => {
                alert('با موفقیت کپی شد: ' + text);
            });
        }

        function uploadReceipt() {
            const fileInput = document.getElementById('receipt-file');
            if (fileInput.files.length === 0) {
                alert('لطفاً ابتدا تصویر فیش واریزی را انتخاب کنید.');
                return;
            }
            const formData = new FormData();
            formData.append('receipt', fileInput.files[0]);

            fetch('/api/upload-receipt', {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                alert(data.message);
                fileInput.value = '';
            })
            .catch(err => {
                alert('خطا در ارسال فیش');
            });
        }

        fetch('/api/user')
            .then(res => res.json())
            .then(data => {
                document.getElementById('balance').innerText = data.balance;
                document.getElementById('user_type').innerText = data.user_type;
                document.getElementById('join_date').innerText = data.join_date;
            });

        fetch('/api/plans')
            .then(res => res.json())
            .then(plans => {
                const container = document.getElementById('plans-container');
                container.innerHTML = '';
                plans.forEach(plan => {
                    container.innerHTML += `
                        <div class="plan-item">
                            <div>
                                <strong style="font-size: 14px;">${plan.title}</strong><br>
                                <small style="color: #94a3b8;">${plan.desc}</small><br>
                                <span style="color: #facc15; font-weight: bold; font-size: 14px; margin-top: 4px; display: inline-block;">${plan.price}</span>
                            </div>
                            <div>
                                <button class="btn-copy" onclick="copyText('${plan.raw_price}')">کپی مبلغ</button>
                                <button class="btn-action" onclick="alert('پلن انتخابی شما: ${plan.title}')">انتخاب</button>
                            </div>
                        </div>
                    `;
                });
            });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/user', methods=['GET'])
def get_user():
    return jsonify({
        "username": "توربوVPN",
        "balance": "۵,۰۰۰ تومان",
        "active_services": 0,
        "user_type": "عادی",
        "join_date": CURRENT_DATE,
        "phone_verified": False
    })

@app.route('/api/plans', methods=['GET'])
def get_plans():
    plans = [
        {"id": 1, "title": "طلایی اقتصادی (نامحدود)", "badge": "🥇", "price": "۱۵۰,۰۰۰ تومان 🥇", "raw_price": "150000", "desc": "نام کاربری دلخواه (ضروری)"},
        {"id": 2, "title": "پلن خاص (تک لوکیشن 🇹🇷 تانل)", "badge": "📌", "price": "۲۲۰,۰۰۰ تومان 📌", "raw_price": "220000", "desc": "نام کاربری دلخواه (ضروری)"},
        {"id": 3, "title": "الماس (حجمی فول تانل)", "badge": "🔱", "price": "۳۰۰,۰۰۰ تومان 🔱", "raw_price": "300000", "desc": "نام کاربری دلخواه (ضروری)"}
    ]
    return jsonify(plans)

@app.route('/api/upload-receipt', methods=['POST'])
def upload_receipt():
    if 'receipt' not in request.files:
        return jsonify({"message": "فایلی یافت نشد!"}), 400
    
    file = request.files['receipt']
    if file.filename == '':
        return jsonify({"message": "فایلی انتخاب نشده است."}), 400
    
    return jsonify({"message": "فیش شما با موفقیت ارسال شد و پس از بررسی تایید می‌گردد."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)