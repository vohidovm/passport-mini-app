from flask import Flask, request, jsonify
import cv2, pytesseract
from mrz.checker.td3 import TD3CodeChecker

app = Flask(__name__)

@app.route("/")
def home():
    return "Mini App ishlayapti ✅"

@app.route("/scan", methods=["POST"])
def scan():
    img = request.files["image"]
    img.save("img.jpg")

    image = cv2.imread("img.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    lines = [l for l in text.split("\n") if "<<" in l]

    if len(lines) >= 2:
        mrz = lines[0] + "\n" + lines[1]
        check = TD3CodeChecker(mrz)
        return jsonify({
            "result": "MRZ TO‘G‘RI ✅" if check.valid else "MRZ XATO ⚠️",
            "mrz": mrz
        })

    return jsonify({"result": "MRZ TOPILMADI ❌"})

app.run(host="0.0.0.0", port=10000)
