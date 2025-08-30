from flask import Flask, render_template_string
from get_data import get_data

app = Flask(__name__)

BM_ITEMS = get_data()

@app.route("/")
def home():
    card_html = ""
    for item in BM_ITEMS:
        price = item["prices"].get("XX")
        title = item.get("title")
        description = item.get("description")
        image = item.get("imageUrl")
        buy_url = item.get("purchaseUrl")
        item_id = item.get("id")

        card_html += f"""
        <div class="card" id="card_{item_id}">
            <img src="{image}" loading="lazy" class="item_image" id="img_{item_id}"/>
            <h2 class="item_title" id="title_{item_id}">{title}</h2>
            <p class="item_description" id="desc_{item_id}">{description}</p>
            <a href="{buy_url}"><button type="button"><img style="width: 1.5rem; padding: 0.2rem" src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/6c0178740fa623a059182d076f44031600d079d5_shell.png"/>{price} needed</button></a>
        </div>        
        """
    css = """
    <style>
        .card{
            display: flex;
            background-color: grey;
            border-color: grey;
        }
        .bar{
            position: sticky;
            top: 0;
            z-index: 10;
            background: white;
            
            } 
        .bar > a{
            text-decoration: none;
            color: inherit;
        }
    </style>"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        {{css|safe}}
        <title>orpheus market</title>
    </head>
    <body>
        <div class="bar">
            <a href="https://summer.hackclub.com/shop/black_market"><h1 class="orpheusmarket">orpheusmarket</h1></a>
        </div>
        {{card_html|safe}}
    </body>
    </html>

    """
    return render_template_string(html, card_html=card_html, css=css)




if __name__ == "__main__":
    app.run()