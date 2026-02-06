from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests
import io

app = Flask(_name_)

# ... (Apka purana code yahan hoga) ...

# --- 🖼️ FRIEND FRAME GENERATOR API ---
@app.route('/api/friend', methods=['GET'])
def friend_frame():
    try:
        # 1. Inputs lena (IDs or URLs)
        url1 = request.args.get('url1')
        url2 = request.args.get('url2')
        name1 = request.args.get('name1', 'Friend')
        name2 = request.args.get('name2', 'Friend')

        if not url1 or not url2:
            return {"error": "URLs missing"}, 400

        # 2. Base Canvas (Dark Luxury Background)
        W, H = 1000, 600
        background = Image.new('RGB', (W, H), color='#1a1a1a') # Dark Gray/Black
        draw = ImageDraw.Draw(background)

        # 3. Images Download & Process
        def process_img(url):
            resp = requests.get(url)
            img = Image.open(io.BytesIO(resp.content)).convert("RGB")
            img = ImageOps.fit(img, (350, 350), centering=(0.5, 0.5)) # Auto Adjust
            return img

        img1 = process_img(url1)
        img2 = process_img(url2)

        # 4. Drawing Gold Frames (Borders)
        # Left Frame
        draw.rectangle([45, 95, 405, 455], outline="#FFD700", width=10) # Gold Border
        background.paste(img1, (50, 100))
        
        # Right Frame
        draw.rectangle([595, 95, 955, 455], outline="#FFD700", width=10) # Gold Border
        background.paste(img2, (600, 100))

        # 5. Connecting Line (Style)
        draw.line([405, 275, 595, 275], fill="#FFD700", width=3)
        
        # Heart Icon in Center (Simple Circle for now)
        draw.ellipse([480, 255, 520, 295], fill="#FF0000", outline="#FFD700", width=2)

        # 6. TEXT (English Quotes)
        # Note: Render par default font use kar rahe hain, aap custom font file bhi upload kar sakte hain
        try:
            # Trying to load a better font if available on Linux
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
            text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
            name_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 25)
        except:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            name_font = ImageFont.load_default()

        # Title: BEST FRIENDS
        draw.text((W/2, 50), "BEST FRIENDS", font=title_font, fill="#FFD700", anchor="mm")

        # Quote
        quote = "Side by side or miles apart,\nreal friends are always close to the heart."
        draw.multiline_text((W/2, 520), quote, font=text_font, fill="white", anchor="mm", align="center")

        # Names below images
        draw.text((225, 480), name1, font=name_font, fill="white", anchor="mm")
        draw.text((775, 480), name2, font=name_font, fill="white", anchor="mm")

        # 7. Final Image Save
        img_io = io.BytesIO()
        background.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

    except Exception as e:
        return {"error": str(e)}, 500

# ... (App run code) ...
