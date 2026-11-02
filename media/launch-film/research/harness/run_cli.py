"""Run the repo's interact.py against a local stand-in for the API Gateway stage (127.0.0.1 only).
The stand-in passes the JSON body to the real handler (Rekognition stubbed) and returns the handler's dict as the
JSON body, as the repo's non-proxy (type AWS) integration does. Usage: python -I run_cli.py <repo_dir> <case>"""
import sys, os, json, threading, base64, importlib.util, subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from botocore.stub import Stubber
os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1"); os.environ["AWS_EC2_METADATA_DISABLED"] = "true"
repo, case = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("h", os.path.join(repo, "python", "rekognition.py")); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
class Ctx: invoked_function_arn = "arn:aws:lambda:us-east-1:<account>:function:Detection_Lambda_Function"
FD = {"good": [{"Smile": {"Value": True}, "EyesOpen": {"Value": True}, "Emotions": []}],
      "bad": [{"Smile": {"Value": False}, "EyesOpen": {"Value": False}, "Emotions": []}],
      "two": [{"Smile": {"Value": True}, "EyesOpen": {"Value": True}, "Emotions": []}] * 2}[case]
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        st = Stubber(mod.rekognition); st.add_response("detect_faces", {"FaceDetails": FD})
        with st: out = mod.lambda_handler(body, Ctx())
        data = json.dumps(out).encode(); self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(data)
srv = HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_port}/dev/friendly"
img = "goodphoto.jpeg" if case != "bad" else "badphoto.png"
r = subprocess.run([sys.executable, "-I", os.path.join(repo, "interact.py"), url, img], cwd=repo, capture_output=True, text=True)
print(f"$ python interact.py <url> {img}\n{r.stdout}{r.stderr}")
srv.shutdown()
