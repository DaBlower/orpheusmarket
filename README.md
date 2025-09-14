# orpheusmarket
this is a _replica_ with the actual stock and products in the real SOM heidimarket!

## What I used
I used [`@mahad`](https://hackclub.slack.com/team/U059VC0UDEU)'s [api](https://summer.skyfall.dev/api/shop) to get the list of items and their properties (like price and image) and Flask as the framework.

## Features
- Up-to-date items
- Real images
- Region selector with prices accurate to your region
- A buy link that's functional *if* you already have heidmarket acess
- A cool UI with no horizontal scrolling for you mobile users! 


## Test it out!
You can test it out at [orpheus.olive.hackclub.app](https://orpheus.olive.hackclub.app)

*OR*

You can setup a Flask development server by
1. Creating a virtual environment
`python3 -m venv venv`
2. Activating it
Windows: `venv\Scripts\activate`
Linux/MacOS: `source venv/bin/activate`
3. Installing dependencies
`pip install -r requirements.txt`
4. Running Flask
`flask --app app run`
You can now access it at the location that Flask provides! (i.e. localhost:5000)
