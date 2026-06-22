from flask import Flask, request, jsonify, render_template_string
from bot import handle

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>microgpt name generator</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #f5f5f5; display: flex; justify-content: center; align-items: center;
    min-height: 100vh; padding: 1rem;
  }
  .card {
    background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    padding: 2rem; max-width: 520px; width: 100%;
  }
  h1 { font-size: 1.4rem; margin-bottom: 0.25rem; }
  p { color: #666; font-size: 0.9rem; margin-bottom: 1.25rem; }
  label { font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.35rem; }
  input[type="text"] {
    width: 100%; padding: 0.6rem 0.75rem; border: 1px solid #ccc; border-radius: 6px;
    font-size: 1rem;
  }
  input[type="text"]:focus { outline: none; border-color: #0066cc; box-shadow: 0 0 0 2px rgba(0,102,204,0.15); }
  .hint { font-size: 0.8rem; color: #888; margin-top: 0.25rem; margin-bottom: 1rem; }
  button {
    background: #0066cc; color: #fff; border: none; border-radius: 6px;
    padding: 0.6rem 1.5rem; font-size: 1rem; cursor: pointer; width: 100%;
  }
  button:hover { background: #0052a3; }
  button:disabled { opacity: 0.6; cursor: not-allowed; }
  #result { margin-top: 1.25rem; padding: 1rem; border-radius: 6px; display: none; }
  #result.ok { background: #e6f7e6; display: block; }
  #result.refuse { background: #fff0f0; display: block; }
  #result.error { background: #fff3cd; display: block; }
  #result pre { margin: 0; white-space: pre-wrap; word-break: break-word; font-family: inherit; }
  #spinner { display: none; text-align: center; margin-top: 1rem; color: #888; font-size: 0.85rem; }
  hr { margin: 1.5rem 0; border: none; border-top: 1px solid #eee; }
  .examples { font-size: 0.85rem; }
  .examples code { background: #f0f0f0; padding: 0.15rem 0.4rem; border-radius: 3px; cursor: pointer; }
  .examples code:hover { background: #ddd; }
</style>
</head>
<body>
<div class="card">
  <h1>microgpt name generator</h1>
  <p>A tiny character-level GPT that generates names. Type letter prefixes below.</p>

  <label for="prefixes">Letter prefix(es)</label>
  <input type="text" id="prefixes" placeholder="e.g. j  or  a b c" autofocus>
  <div class="hint">Separate multiple prefixes with spaces. Leave blank for a random name.</div>
  <button id="generate" onclick="generate()">Generate</button>
  <div id="spinner">Generating…</div>
  <div id="result"></div>

  <hr>
  <div class="examples">
    <strong>Try:</strong>
    <code onclick="use('j')">j</code>
    <code onclick="use('ab')">ab</code>
    <code onclick="use('a b c')">a b c</code>
    <code onclick="use('')">(random)</code>
  </div>
</div>

<script>
function use(v) { document.getElementById('prefixes').value = v; generate(); }

async function generate() {
  const btn = document.getElementById('generate');
  const spinner = document.getElementById('spinner');
  const result = document.getElementById('result');
  const prefixes = document.getElementById('prefixes').value;

  btn.disabled = true;
  spinner.style.display = 'block';
  result.style.display = 'none';
  result.className = '';

  try {
    const resp = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prefixes })
    });
    const data = await resp.json();

    result.className = data.status;
    result.innerHTML = '<pre>' + escapeHtml(data.output) + '</pre>';
    result.style.display = 'block';
  } catch (e) {
    result.className = 'error';
    result.innerHTML = '<pre>Error: ' + escapeHtml(e.message) + '</pre>';
    result.style.display = 'block';
  } finally {
    btn.disabled = false;
    spinner.style.display = 'none';
  }
}

function escapeHtml(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.get_json(silent=True) or {}
    prefixes = (data.get("prefixes") or "").strip()
    try:
        output = handle(prefixes)
        if output.startswith("REFUSE:"):
            return jsonify(status="refuse", output=output)
        return jsonify(status="ok", output=output)
    except Exception as e:
        return jsonify(status="error", output=f"Error: {e}")


if __name__ == "__main__":
    print("Open http://127.0.0.1:5050 in your browser")
    app.run(host="0.0.0.0", port=5050, debug=True)
