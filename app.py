from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def lacak_ip(ip_address):
    try:
        # Mengirim permintaan ke API ip-api.com
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()

        if data['status'] == 'success':
            google_maps_link = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
            data['google_maps_link'] = google_maps_link
            return data
        else:
            return {"error": "Gagal melacak IP. Pastikan IP yang dimasukkan valid."}
    except Exception as e:
        return {"error": f"Terjadi kesalahan: {str(e)}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lacak', methods=['POST'])
def lacak():
    ip_address = request.form.get('ip')
    if not ip_address:
        return jsonify({"error": "IP Address tidak diberikan"}), 400

    result = lacak_ip(ip_address)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)