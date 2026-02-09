from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get-video', methods=['GET'])
def get_video():
    video_url = request.args.get('url') # استقبال الرابط من المتصفح
    if not video_url:
        return jsonify({"error": "Please provide a URL"}), 400

    # منطق TikWM الذي كتبته أنت
    api_url = "https://www.tikwm.com/api/"
    if "instagram.com" in video_url:
        api_url = "https://www.tikwm.com/api/ig/post"

    response = requests.post(api_url, data={'url': video_url}).json()
    
    if response.get('code') == 0:
        data = response['data']
        # استخراج الرابط المباشر
        direct_link = data.get('play') or (data[0].get('url') if isinstance(data, list) else data.get('url'))
        
        # إرجاع الرابط العام كـ JSON
        return jsonify({
            "status": "success",
            "download_url": "https://www.tikwm.com" + direct_link if direct_link.startswith('/') else direct_link
        })
    else:
        return jsonify({"status": "error", "message": "Could not fetch video"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
