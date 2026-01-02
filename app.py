from flask import Flask, render_template, redirect, request
import json, random, csv, os
from datetime import datetime

app = Flask(__name__)

# Load offers and A/B testing variants
with open("offers.json") as f:
    offers = json.load(f)

with open("variants.json") as f:
    variants = json.load(f)

# Ensure clicks.csv exists
if not os.path.exists("clicks.csv"):
    with open("clicks.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "ip", "user_agent", "offer_shown", "variant_headline", "variant_cta"])

@app.route("/")
def index():
    headline = random.choice(variants["headlines"])
    cta_text = random.choice(variants["cta_texts"])
    return render_template("index.html", headline=headline, cta_text=cta_text)

@app.route("/go")
def go():
    offer = random.choice(offers)
    # Log click
    with open("clicks.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            request.remote_addr,
            request.user_agent.string,
            offer["name"],
            request.args.get("headline", ""),
            request.args.get("cta", "")
        ])
    return redirect(offer["url"])

if __name__ == "__main__":
    app.run(debug=True)
