from flask import Flask, request, render_template
import requests
import json
import os
from urllib.parse import urlparse, parse_qs, unquote

app = Flask(__name__, template_folder="templates")

COUNTER_FILE = "counter.json"

def read_counter():
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, "r") as f:
                return json.load(f).get("count", 0)
        except:
            return 0
    return 0

def write_counter(count):
    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": count}, f)

def http_get(url):
    try:
        resp = requests.get(url, timeout=8)
        return resp.text if resp is not None else ""
    except Exception:
        return ""

@app.route("/", methods=["GET"])
def home():
    total_count = read_counter()
    # The original form submits with GET and a 'submit' name on the button.
    # We'll trigger processing only when 'submit' is present (same behavior).
    if "submit" in request.args:
        url = request.args.get("url", "")
        if not url:
            return render_template("index.html", total_count=total_count, alert="PLEASE ENTER A VALID URL.")
        # Validate basic URL form
        try:
            decoded = unquote(url)
            parsed = urlparse(decoded)
            if not parsed.scheme or not parsed.netloc:
                return render_template("index.html", total_count=total_count, alert="PLEASE ENTER A VALID URL.")
        except Exception:
            return render_template("index.html", total_count=total_count, alert="PLEASE ENTER A VALID URL.")
        # extract clickid param
        qs = parsed.query
        params = parse_qs(qs)
        click_id = params.get("clickid", [""])[0] or params.get("click_id", [""])[0] or params.get("clickId", [""])[0]
        if not click_id:
            return render_template("index.html", total_count=total_count, alert="CLICK ID NOT FOUND.")
        # Prepare postbacks (copied from original logic)
        postback = f"https://paychat.fuse-cloud.com/pb?tid={click_id}"
        postback1 = f"https://paychat.fuse-cloud.com/pb?tid={click_id}&e_tkn=trial_successful"
        r = http_get(postback)
        r1 = http_get(postback1)
        # check for success indicators
        if ("conversion_status=Approved" in r1) or ("Success" in r1) or ("Success" in r):
            total_count += 1
            try:
                write_counter(total_count)
            except:
                pass
            return render_template("index.html", total_count=total_count, success=True)
        else:
            return render_template("index.html", total_count=total_count, alert="Postback was not successful.")
    return render_template("index.html", total_count=total_count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)