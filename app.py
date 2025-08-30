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
    css = """
    <style>
        body {
            font-family: sans-serif;
            background-color: #fff;
            margin: 0;
            padding: 20px;
        }
        .card{
            display: flex;
            align-items: center;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            padding: 16px;
            margin: 16px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            overflow: hidden;
        }
        .item_image{
            width: 120px;
            height: 120px;
            object-fit: cover;
            border-radius: 8px;
            margin-right: 32px;
        }
        .card-content{
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }
        .shell-icon{
            width: 1.2rem;
            height: 1.2rem;
            margin-right: 8px;
        }
        .buy-link{
            align-self: flex-start;
        }
        .buy_button{
            display: inline-flex;
            align-items: center;
            background-color: #8b60ad;
            color: white;
            border: none;
            padding: 10px 15px;
            font-size: 1em;
            cursor: pointer;
            text_decoration: none;
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