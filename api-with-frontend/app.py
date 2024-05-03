from flask import Flask, request, jsonify, render_template, redirect, url_for
import decimal

app = Flask(__name__)

# 匯率資料，通常這部分會從外部系統獲取或注入
currencies = {
    "TWD": {"TWD": 1, "JPY": 3.669, "USD": 0.03281},
    "JPY": {"TWD": 0.26956, "JPY": 1, "USD": 0.00885},
    "USD": {"TWD": 30.444, "JPY": 111.801, "USD": 1}
}

class CurrencyExchangeService:
    def __init__(self, rates):
        self.rates = rates

    def convert(self, source, target, amount):
        # 驗證貨幣是否存在
        if source not in self.rates or target not in self.rates[source]:
            return None, "Currency not supported"
        
        # 嘗試解析並計算金額
        try:
            clean_amount = decimal.Decimal(amount.replace(',', ''))
            result = clean_amount * decimal.Decimal(self.rates[source][target])
            result = result.quantize(decimal.Decimal('0.01'), rounding=decimal.ROUND_HALF_UP)
            return f"{result:,.2f}", "success"
        except Exception as e:
            return None, str(e)
        
@app.route('/')
def index():
    result = request.args.get('result', '')
    return render_template('index.html', result=result)

@app.route('/convert', methods=['GET'])
def convert():
    source = request.args.get('source')
    target = request.args.get('target')
    amount = request.args.get('amount')

    service = CurrencyExchangeService(currencies)
    result, message = service.convert(source, target, amount)
    
    if result is None:
        return jsonify({"msg": message}), 400
    
    return redirect(url_for('index', result=result))

if __name__ == "__main__":
    app.run(debug=True)
