from flask import Flask, request
import nlp_feature_by_w2v
from waitress import serve


app = Flask(__name__)

FEATURE_SIZE = 25


@app.route("/get_nlp_feature", methods=["POST"])
def get_nlt_feature():
    ret = {"feature": None, "valid": 0}
    try:
        sentence = request.form["sentence"]
        sentence_feature = nlp_feature_by_w2v.generate_w2v_feature(sentence, FEATURE_SIZE)
        ret["feature"] = sentence_feature.tolist()
        ret["valid"] = 1
    except:
        return ret
    return ret


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # serve(app, host='0.0.0.0', port=5000)

