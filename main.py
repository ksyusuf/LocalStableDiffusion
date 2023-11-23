from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from PIL import Image
import local_stable_diffusion


###### BURASI YEREL BİLGİSAYAR. STABLE DİFFUSİON OLDUĞU YER.
#### BURASI AÇIK OLACAK. DİĞER TARAF BURAYA İSTEK GÖNDERECEK.
#### EĞER BURASI KAPALI İSE DİĞER TARAFTA BİLDİRİM VERİLECEK ""YEREL PC KAPALI"" DİYE

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        ##################################################################################3

        ## BURADA GELEN İSTEĞİ ALGILAYIP VERİLERİ OLUŞTURUP YOLLUYORUZ.
        ## VERİ GELMİYOR BURAYA. POST DEĞİL ÇÜNKÜ.

        # Image Content
        prompt = "latte in red cup"
        image_path = "../coffee-4908764_1280.jpg"  # Değiştirebilirsiniz
        generated_image = local_stable_diffusion.image_pipeline.generate_image(prompt=prompt,
                                                                               image_path=image_path)

        buffered = BytesIO()
        generated_image.save(buffered, format="PNG")
        image_bytes = buffered.getvalue()

        self.wfile.write(image_bytes)
        print("oluşturma tamamlandı. RESİM GERİ GÖNDERİLDİ.")

        ##################################################################################3

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        received_data = self.rfile.read(content_length)

        ## SANIRIM BURASI POST İŞLŞEMİNİN KARŞILANDIĞI YER OLUYOR.
        ## EĞER YAPABİLİRSEM POST İLE PROMT VE İMAGE ALIRIM
        ## RETURN OLARAK GENERATED_İMAGE DÖNDÜRÜRÜM BASİT.

        # Burada received_data'yi kullanabilirsiniz
        # Örneğin, dosyaya kaydedebilir veya başka bir işlem yapabilirsiniz

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("POST isteği başarıyla alındı.".encode('utf-8'))
        # RESMİN BAŞARIYLA GELDİĞİNİ BİLDİRİR AMA KARŞIDA KARŞIKLANMADIĞI İÇİN OKUYAMIYORUZ.


def run(server_class=HTTPServer, handler_class=MyHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Sunucu {port} portunda çalışıyor...")
    httpd.serve_forever()


if __name__ == '__main__':
    run()
