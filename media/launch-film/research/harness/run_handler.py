"""Run the repo's real Lambda handler locally, with botocore's Stubber standing in for Rekognition.
No network, no credentials: the Stubber answers detect_faces before any request is signed or sent.
Usage: python -I run_handler.py <repo_dir>"""
import sys, os, json, base64, logging, importlib.util, io
from botocore.stub import Stubber
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ["AWS_EC2_METADATA_DISABLED"] = "true"
repo = sys.argv[1]
spec = importlib.util.spec_from_file_location("rekognition_handler", os.path.join(repo, "python", "rekognition.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
logbuf = io.StringIO(); h = logging.StreamHandler(logbuf); h.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
mod.logger.addHandler(h); mod.logger.setLevel(logging.INFO)
class Ctx: invoked_function_arn = "arn:aws:lambda:us-east-1:<account>:function:Detection_Lambda_Function"
good = open(os.path.join(repo, "goodphoto.jpeg"), "rb").read()
bad = open(os.path.join(repo, "badphoto.png"), "rb").read()
def face(smile, eyes): return {"Smile": {"Value": smile}, "EyesOpen": {"Value": eyes}, "Emotions": []}
cases = [
  ("one face, smiling, eyes open", good, [face(True, True)]),
  ("one face, not smiling, eyes closed", bad, [face(False, False)]),
  ("one face, smiling, eyes closed", good, [face(True, False)]),
  ("two faces", good, [face(True, True), face(True, True)]),
  ("no face", good, []),
]
results = []
for name, img, fds in cases:
    st = Stubber(mod.rekognition)
    st.add_response("detect_faces", {"FaceDetails": fds}, expected_params={"Image": {"Bytes": img}, "Attributes": ["ALL"]})
    with st:
        event = {"image": base64.b64encode(img).decode("utf8")}
        out = mod.lambda_handler(event, Ctx())
        st.assert_no_pending_responses()
    results.append((name, len(event["image"]), out))
# no image key
out = mod.lambda_handler({"S3Object": {}}, Ctx()); results.append(("event without 'image'", 0, out))
# Rekognition refuses the call (ClientError)
st = Stubber(mod.rekognition)
st.add_client_error("detect_faces", service_error_code="InvalidImageFormatException", service_message="<message from Rekognition>", http_status_code=400)
with st:
    out = mod.lambda_handler({"image": base64.b64encode(b"not an image").decode()}, Ctx())
results.append(("Rekognition ClientError", 0, out))
for name, n, out in results:
    print(f"[{name}] request image chars={n}\n  -> {json.dumps(out)}")
print("--- log lines"); print(logbuf.getvalue().strip())
