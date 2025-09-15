from flask import Flask, render_template_string, session, request
from get_data import get_data
from dotenv import load_dotenv
import os

load_dotenv() # load env

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
BM_ITEMS = get_data(regular=False)
RG_ITEMS = get_data(regular=True) # regular shop

images = BM_ITEMS[2] # dict of images
warn = BM_ITEMS[1]
BM_ITEMS = BM_ITEMS[0]
RG_ITEMS = RG_ITEMS[0]

allowed_regions = {"US", "EU", "IN", "CA", "AU", "XX"}
allowed_shops = {"regular", "blackMarket"}

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__))) # for file operations (i.e. images)

@app.route("/.env")
@app.route("/.git/config")
@app.route("/js/lkk_ch.js")
@app.route("/config.php")
@app.route("/config.xml")
@app.route("/.ssh/id_ed25519")
@app.route("/database.sql")
def fu():
    return "flip you bot :D"


@app.route("/")
def home():
    # session stuff
    session.permanent = True
    card_html = ""
    region = request.args.get('region', session.get("region", "XX")).upper()
    shop = request.args.get('shop', session.get("shop", "blackMarket")).lower()

    school = request.args.get('school', type=bool, default=False)

    if region not in allowed_regions:
        region = "XX"

    if shop not in allowed_shops:
        shop = "blackMarket"

    session["region"] = region
    session["shop"] = shop

    warning_html = ""
    if warn == True:
        warning_html = """
        <div class="card">
            <img src="/static/noo.png" loading="lazy" class="item_image"/>
            <div class="card-content">
                <h2 class="item-title"><span style="color: orange;">Warning:</span> This is a backup!</h2>
                <p class="item_description">currently, the api i'm using is down D: so for now, this site will use a backup. It might be a bit outdated, so sorry for any inconvenience!</p>
            </div>
        </div>
        """

    shop_list = [] # used to carry either black market or regular shop items

    if shop == "blackMarket":
        shop_list = BM_ITEMS
    else:
        shop_list = RG_ITEMS

    for item in shop_list:
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
            item_id = item.get("id")
            title = item.get("title")
            description = item.get("description")
            # temporary for school lol
            if school:
                description = description.replace("fuc", "duc")

            item_images = images.get(str(item_id), {})
            backup_date = item_images.get("date", "")
            image_filename = item_images.get("localImage", "")
            image = os.path.join("static", "backups", backup_date, image_filename) if image_filename else item.get("imageUrl")
            
            full_image_path = os.path.join(project_root, image)
            if not os.path.isfile(full_image_path):
                image = item.get("imageUrl")

            buy_url = item.get("purchaseUrl")

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
        <link rel="stylesheet" href="static/style.css">
        <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-touch-icon.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/site.webmanifest">
        <title>orpheusmarket</title>
    </head>
    <body>
        <div class="bar">
            <a href="https://summer.hackclub.com/shop/black_market"><h1 class="orpheusmarket">orpheusmarket</h1><img src="/static/orpheus.png" class="dino"/></a>
        </div>
        <div class="region">
            <div>
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
            <div>
                <h3>Choose your shop</h3>
                <p>You can view items for both the regular shop and orpheusmarket!</p>
                <div class="region-container">
                    <form method="get" action="/">
                        <select id="shop-selector" class="region-selector" name="shop" onchange="this.form.submit()">
                            <option value="regular" {% if shop == 'regular' %}selected{% endif %}> regular shop </option>
                            <option value="blackMarket" {% if shop == 'blackMarket' %}selected{% endif %}> orpheusmarket </option>
                        </select>
                    </form>
                </div>
            </div>
        </div>
        {{warning_html|safe}}
        <div class="card">
            <img src="/static/orpheus.png" loading="lazy" class="item_image"/>
            <div class="card-content">
                <h2 class="item-title">Follow me on SOM!</h2>
                <p class="item_description">this was a project made for Hack Club's Summer of Making!</p>
                <a href="https://summer.hackclub.com/projects/12114" class="buy-link">
                    <button type="button" class="buy_button">
                        <span>Follow!</span>
                    </button>
                </a>
            </div>
        </div>
        <div class="card_container">
            {{card_html|safe}}
        </div>
        <div class="footer"><a href="https://github.com/DaBlower">Made with ❤️ by obob!</a></div>
    </body>
    </html>
    """

    return render_template_string(html, card_html=card_html, region=region, shop=shop, warning_html=warning_html)




if __name__ == "__main__":
    app.run(port=38015)
