from flask import Flask, render_template, request, jsonify, redirect, url_for
import time
import requests
import random
import os
import urllib.parse
from dotenv import load_dotenv
import datetime

# .env dosyasını yükle
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    # Çevre değişkenlerini al
    config = {}
    
    # Genel ayarlar
    config['APP_NAME'] = os.getenv('APP_NAME', 'YT-MP3')
    config['APP_DESCRIPTION'] = os.getenv('APP_DESCRIPTION', 'YouTube videolarını MP3 formatına dönüştürün')
    config['APP_YEAR'] = os.getenv('APP_YEAR', str(datetime.datetime.now().year))
    
    # Navbar ve Logo
    config['NAVBAR_TITLE'] = os.getenv('NAVBAR_TITLE', 'YT-MP3')
    config['NAVBAR_MENU_HOME'] = os.getenv('NAVBAR_MENU_HOME', 'Ana Sayfa')
    config['NAVBAR_MENU_FEATURES'] = os.getenv('NAVBAR_MENU_FEATURES', 'Özellikler')
    config['NAVBAR_MENU_HOW_IT_WORKS'] = os.getenv('NAVBAR_MENU_HOW_IT_WORKS', 'Nasıl Çalışır')
    
    # Hero Section
    config['HERO_TITLE'] = os.getenv('HERO_TITLE', 'YouTube\'dan MP3')
    config['HERO_SUBTITLE'] = os.getenv('HERO_SUBTITLE', 'Hızlı ve Kolay')
    config['HERO_DESCRIPTION'] = os.getenv('HERO_DESCRIPTION', 'YouTube videolarını MP3 formatına dönüştürün')
    
    # Converter Section
    config['CONVERTER_LABEL'] = os.getenv('CONVERTER_LABEL', 'YouTube Video URL\'si')
    config['CONVERTER_PLACEHOLDER'] = os.getenv('CONVERTER_PLACEHOLDER', 'https://www.youtube.com/watch?v=...')
    config['CONVERTER_BUTTON'] = os.getenv('CONVERTER_BUTTON', 'MP3 olarak dönüştür')
    config['CONVERTER_LOADING'] = os.getenv('CONVERTER_LOADING', 'Dönüştürülüyor...')
    config['CONVERTER_SUCCESS'] = os.getenv('CONVERTER_SUCCESS', 'Dönüştürme işlemi başarılı!')
    config['CONVERTER_SUCCESS_DESC'] = os.getenv('CONVERTER_SUCCESS_DESC', 'MP3 dosyası indirilmeye hazır.')
    config['CONVERTER_DOWNLOAD_BUTTON'] = os.getenv('CONVERTER_DOWNLOAD_BUTTON', 'MP3 Dosyasını İndir')
    config['CONVERTER_MANUAL_DOWNLOAD'] = os.getenv('CONVERTER_MANUAL_DOWNLOAD', 'İndirme otomatik başlamazsa, buraya tıklayın')
    
    # Features Section
    config['FEATURES_TITLE'] = os.getenv('FEATURES_TITLE', 'Neden Biz?')
    config['FEATURE1_TITLE'] = os.getenv('FEATURE1_TITLE', 'Hızlı Dönüşüm')
    config['FEATURE1_DESCRIPTION'] = os.getenv('FEATURE1_DESCRIPTION', 'Saniyeler içinde dönüştürün')
    config['FEATURE2_TITLE'] = os.getenv('FEATURE2_TITLE', 'Güvenli ve Ücretsiz')
    config['FEATURE2_DESCRIPTION'] = os.getenv('FEATURE2_DESCRIPTION', 'Ücretsiz ve kayıt gerektirmez')
    config['FEATURE3_TITLE'] = os.getenv('FEATURE3_TITLE', 'Yüksek Kalite')
    config['FEATURE3_DESCRIPTION'] = os.getenv('FEATURE3_DESCRIPTION', 'En iyi ses kalitesi')
    
    # How It Works Section
    config['HOW_IT_WORKS_TITLE'] = os.getenv('HOW_IT_WORKS_TITLE', 'Nasıl Çalışır?')
    config['HOW_STEP1_TITLE'] = os.getenv('HOW_STEP1_TITLE', 'URL\'yi Yapıştırın')
    config['HOW_STEP1_DESCRIPTION'] = os.getenv('HOW_STEP1_DESCRIPTION', 'YouTube bağlantısını yapıştırın')
    config['HOW_STEP2_TITLE'] = os.getenv('HOW_STEP2_TITLE', 'Dönüştürün')
    config['HOW_STEP2_DESCRIPTION'] = os.getenv('HOW_STEP2_DESCRIPTION', 'Dönüştür düğmesine tıklayın')
    config['HOW_STEP3_TITLE'] = os.getenv('HOW_STEP3_TITLE', 'İndirin') 
    config['HOW_STEP3_DESCRIPTION'] = os.getenv('HOW_STEP3_DESCRIPTION', 'MP3 dosyasını indirin')
    
    # Footer
    config['FOOTER_DESCRIPTION'] = os.getenv('FOOTER_DESCRIPTION', 'YouTube videolarını MP3 formatına dönüştürün')
    config['FOOTER_LINKS_TITLE'] = os.getenv('FOOTER_LINKS_TITLE', 'Bağlantılar')
    config['FOOTER_LINKS_HOME'] = os.getenv('FOOTER_LINKS_HOME', 'Ana Sayfa')
    config['FOOTER_LINKS_FEATURES'] = os.getenv('FOOTER_LINKS_FEATURES', 'Özellikler')
    config['FOOTER_LINKS_HOW_IT_WORKS'] = os.getenv('FOOTER_LINKS_HOW_IT_WORKS', 'Nasıl Çalışır')
    config['FOOTER_LEGAL_TITLE'] = os.getenv('FOOTER_LEGAL_TITLE', 'Yasal')
    config['FOOTER_LEGAL_PRIVACY'] = os.getenv('FOOTER_LEGAL_PRIVACY', 'Gizlilik Politikası')
    config['FOOTER_LEGAL_TERMS'] = os.getenv('FOOTER_LEGAL_TERMS', 'Kullanım Koşulları')
    config['FOOTER_LEGAL_DMCA'] = os.getenv('FOOTER_LEGAL_DMCA', 'DMCA')
    
    # Telif hakkı metni için özel işlem
    copyright_template = os.getenv('FOOTER_COPYRIGHT', '&copy; {year} {app_name} Dönüştürücü. Tüm hakları saklıdır.')
    config['FOOTER_COPYRIGHT'] = copyright_template.format(year=config['APP_YEAR'], app_name=config['APP_NAME'])
    
    return render_template('index.html', config=config)

@app.route('/convert', methods=['POST'])
def convert():
    # Video URL'sini formdan al
    video_url = request.form.get('video_url')
    
    if not video_url:
        return jsonify({"error": "Video URL'si boş olamaz!"})
    
    # HTTP başlıkları
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua-platform': '"Windows"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'Accept': '*/*',
        'Origin': 'https://ytmp3.cc',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://ytmp3.cc/',
        'Accept-Language': 'tr,en-US;q=0.9,en;q=0.8,tr-TR;q=0.7',
    }

    try:
        # İlk istek için timestamp oluştur
        timestamp = f"{random.random():.16f}"
        params = {
            'k': 'MjVmZDc5YTRhNTE3MmJlYzQ4ZTQ0MWVlZjg1NzBkYTMtdnFLMDBLdEFyQldqTDJjSTNwMnZZcnhiWVBnN29z',
            '_': timestamp,
        }

        # İlk istek - API'yi başlatma
        response = requests.get('https://d.ecoe.cc/api/v1/init', params=params, headers=headers)
        init_data = response.json()

        if 'convertURL' not in init_data or init_data.get('error') != '0':
            return jsonify({"error": "API başlatılamadı"})

        # Dönüştürme URL'sini al
        convert_url = init_data['convertURL']

        # İkinci istek için yeni bir timestamp oluştur
        timestamp2 = f"{random.random():.16f}"

        # İkinci istek - Dönüştürme işlemini başlat
        convert_params = {
            'v': video_url,
            'f': 'mp3',
            '_': timestamp2
        }

        # redirectURL'yi takip et ve sonunda indirme URL'sini al
        current_url = convert_url
        redirect_count = 0
        max_redirects = 5
        download_url = None

        while redirect_count < max_redirects:
            try:
                response = requests.get(current_url, params=convert_params, headers=headers)
                data = response.json()
                
                # Eğer downloadURL varsa, işlem tamamlandı demektir
                if data.get("downloadURL"):
                    download_url = data["downloadURL"]
                    break
                
                # Eğer yönlendirme (redirect) varsa, yeni URL'ye yönlendir
                elif data.get("redirect") == 1 and data.get("redirectURL"):
                    redirect_count += 1
                    current_url = data["redirectURL"]
                    # Parametreler zaten URL içinde olduğundan, boş parametre gönder
                    convert_params = {}
                    time.sleep(2)  # Sunucuya yük bindirmemek için kısa bir bekleme
                
                # Eğer indirme henüz hazır değilse, bekle ve tekrar dene
                else:
                    time.sleep(2)
                
            except requests.RequestException as e:
                return jsonify({"error": f"İstek hatası: {str(e)}"})
        
        if download_url:
            # Dosya adını URL'den çıkarmaya çalış
            try:
                filename = os.path.basename(urllib.parse.urlparse(download_url).path)
                if not filename or '.' not in filename:
                    filename = "youtube_mp3.mp3"
            except:
                filename = "youtube_mp3.mp3"
            
            # İndirme bağlantısı ve dosya adını döndür
            return jsonify({
                "success": True,
                "download_url": download_url,
                "filename": filename
            })
        else:
            return jsonify({
                "error": "İndirme URL'si alınamadı. Lütfen daha sonra tekrar deneyin."
            })
    
    except Exception as e:
        return jsonify({"error": f"Beklenmeyen hata: {str(e)}"})

@app.route('/download/<path:url>')
def download_proxy(url):
    """İndirme bağlantısını yönlendirme ile proxy'le"""
    return redirect(url)

if __name__ == '__main__':
    app.run(debug=True) 