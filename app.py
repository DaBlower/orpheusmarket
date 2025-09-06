from flask import Flask, render_template_string, session, request
from get_data import get_data
from dotenv import load_dotenv
import os

load_dotenv() # load env

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
BM_ITEMS = get_data()

allowed_regions = {"US", "EU", "IN", "CA", "AU", "XX"}

@app.route("/")
def home():
    session.permanent = True
    card_html = ""
    region = request.args.get('region', session.get("region", "XX")).upper()

    school = request.args.get('school', type=bool, default=False)

    if region not in allowed_regions:
        region = "XX"

    session["region"] = region

    for item in BM_ITEMS:
        region_in_store = False
        if region in item["prices"]:
            price = item["prices"].get(region)
            region_in_store = True
        elif "XX" in item["prices"]:
            price = item["prices"].get("XX")
            region_in_store = True
        else:
            region_in_store = False
        if region_in_store == True:
            title = item.get("title")
            description = item.get("description")
            # temporary for school lol
            if school:
                description = description.replace("fuc", "duc")
            image = item.get("imageUrl")
            buy_url = item.get("purchaseUrl")
            item_id = item.get("id")

            card_html += f"""
            <div class="card" id="card_{item_id}">
                <img src="{image}" loading="lazy" class="item_image" id="img_{item_id}"/>
                <div class="card-content">
                    <h2 class="item_title" id="title_{item_id}">{title}</h2>
                    <p class="item_description" id="desc_{item_id}">{description}</p>
                    <a href="{buy_url}" class="buy-link">
                        <button type="button" class="buy_button">
                            <img class="shell-icon" style="padding: 0.2rem" src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/6c0178740fa623a059182d076f44031600d079d5_shell.png"/>
                            <span>{price} needed</span>
                        </button>
                    </a>
                </div>
            </div>        
            """

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {{css|safe}}
        <link rel="stylesheet" href="static/style.css">
        <title>orpheus market</title>
    </head>
    <body>
        <div class="bar">
            <a href="https://summer.hackclub.com/shop/black_market"><h1 class="orpheusmarket">orpheusmarket</h1><img src="/static/orpheus.png" class="dino"/></a>
        </div>
        <div class="region">
            <h3>Choose your region</h3>
            <p>Prices and availability vary by region</p>
            <div class="region-container">
                <form method="get" action="/">
                    <select id="region-selector" class="region-selector" name="region" onchange="this.form.submit()">
                        <option value="US" {% if region == 'US' %}selected{% endif %}> United States </option>
                        <option value="EU" {% if region == 'EU' %}selected{% endif %}> EU + UK </option>
                        <option value="IN" {% if region == 'IN' %}selected{% endif %}> India </option>
                        <option value="CA" {% if region == 'CA' %}selected{% endif %}> Canada </option>
                        <option value="AU" {% if region == 'AU' %}selected{% endif %}> Australia </option>
                        <option value="XX" {% if region == 'XX' %}selected{% endif %}> Rest of World </option>
                    </select>
                </form>
            </div>
        </div>
        {{card_html|safe}}
        <div class="footer"><a href="https://github.com/DaBlower">Made with ❤️ by obob!</a></div>
    </body>
    </html>
    """

    return render_template_string(html, card_html=card_html, region=region)




if __name__ == "__main__":
    app.run()