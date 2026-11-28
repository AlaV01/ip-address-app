"""Version site web de l'application (reutilise IPClient et IPInfo).

Lancer :  python web.py   (le navigateur s'ouvre tout seul)
Arreter : Ctrl + C dans le terminal
"""
import json
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from ip_client import IPClient, APIError
from ip_info import IPInfo

PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IP Address Application</title>
<style>
  :root { --bg:#eef3f9; --card:#ffffff; --text:#14233b; --muted:#5a6b82; --line:#dbe4ef;
          --accent:#1f5fd1; --accent-2:#5b8def; --accent-text:#ffffff; --soft:#e8f0fd;
          --error-bg:#fdeceb; --error:#b3261e; --shadow:0 8px 30px rgba(20,35,59,.10); }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#0e141b; --card:#16202b; --text:#e8eff7; --muted:#94a3b5; --line:#263444;
            --accent:#5b9cf0; --accent-2:#2f6fd6; --accent-text:#08111b; --soft:#1b2a3d;
            --error-bg:#3a1f1d; --error:#ff9a90; --shadow:0 8px 30px rgba(0,0,0,.35); }
  }
  * { box-sizing:border-box; }
  body { margin:0; font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;
         background:var(--bg); color:var(--text); min-height:100vh; }
  header { background:linear-gradient(135deg,var(--accent-2),var(--accent)); color:#fff; padding:34px 16px 70px; }
  .wrap { max-width:720px; margin:0 auto; }
  header h1 { margin:0 0 6px; font-size:28px; letter-spacing:-.01em; }
  header p { margin:0; opacity:.9; }
  main { max-width:720px; margin:-48px auto 40px; padding:0 16px; }
  .card { background:var(--card); border:1px solid var(--line); border-radius:16px; box-shadow:var(--shadow); }
  .tabs { display:flex; gap:6px; padding:6px; margin-bottom:16px; }
  .tab { flex:1; background:transparent; color:var(--muted); border:0; border-radius:11px; padding:12px 8px;
         font-size:14.5px; font-weight:600; cursor:pointer; transition:background .15s,color .15s; }
  .tab:hover { background:var(--soft); color:var(--text); }
  .tab.active { background:var(--accent); color:var(--accent-text); }
  .tab:disabled { cursor:wait; }
  .hero { padding:26px 24px; text-align:center; min-height:168px; display:flex; flex-direction:column;
          align-items:center; justify-content:center; gap:8px; }
  .label { color:var(--muted); font-size:13px; text-transform:uppercase; letter-spacing:.08em; font-weight:600; }
  .ip { font-family:ui-monospace,"Cascadia Mono",Consolas,monospace; font-size:clamp(22px,5.4vw,38px);
        font-weight:700; word-break:break-all; line-height:1.2; }
  .row { display:flex; gap:10px; align-items:center; justify-content:center; flex-wrap:wrap; }
  .badge { background:var(--soft); color:var(--accent); border-radius:999px; padding:4px 12px; font-size:13px; font-weight:700; }
  .ghost { background:transparent; color:var(--accent); border:1px solid var(--line); border-radius:9px;
           padding:6px 12px; font-size:13px; cursor:pointer; text-decoration:none; font-family:inherit; }
  .ghost:hover { background:var(--soft); }
  .msg { color:var(--muted); font-size:16px; max-width:40ch; }
  .error { background:var(--error-bg); color:var(--error); border-radius:10px; padding:12px 16px; font-weight:600; }
  .grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:12px; margin-top:16px; }
  .item { padding:14px 16px; }
  .item .label { font-size:11.5px; }
  .item .value { margin-top:4px; font-size:16px; font-weight:600; word-break:break-word; }
  .spinner { width:30px; height:30px; border:3px solid var(--line); border-top-color:var(--accent);
             border-radius:50%; animation:spin .8s linear infinite; }
  @keyframes spin { to { transform:rotate(360deg); } }
  .fade { animation:fade .25s ease; }
  @keyframes fade { from { opacity:0; transform:translateY(4px); } to { opacity:1; transform:none; } }
  footer { text-align:center; color:var(--muted); font-size:12.5px; margin-top:22px; }
</style>
</head>
<body>
<header><div class="wrap">
  <h1>IP Address Application</h1>
  <p>Votre adresse IP publique et les informations qui lui sont associ&eacute;es</p>
</div></header>
<main>
  <div class="card tabs">
    <button class="tab" data-action="details">Tout afficher</button>
    <button class="tab" data-action="ipv4">IPv4</button>
    <button class="tab" data-action="ipv6">IPv6</button>
  </div>
  <div class="card hero" id="hero"></div>
  <div class="grid" id="grid"></div>
  <footer>Projet Cisco DevNet 4.9.4 &middot; donn&eacute;es : ipify.org et ipinfo.io</footer>
</main>
<script>
const hero = document.getElementById("hero");
const grid = document.getElementById("grid");
const tabs = document.querySelectorAll(".tab");
const FIELDS = [["city","Ville"],["region","R\u00e9gion"],["country","Pays"],
                ["isp","Fournisseur"],["timezone","Fuseau horaire"],["loc","Coordonn\u00e9es"]];

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function setHero(nodes) {
  hero.replaceChildren(...nodes);
  hero.classList.remove("fade"); void hero.offsetWidth; hero.classList.add("fade");
}

function ipBlock(label, ip, version) {
  const copy = el("button", "ghost", "Copier");
  copy.addEventListener("click", async function () {
    try { await navigator.clipboard.writeText(ip); copy.textContent = "Copi\u00e9 !"; }
    catch (e) { copy.textContent = "Impossible de copier"; }
    setTimeout(function () { copy.textContent = "Copier"; }, 1500);
  });
  const row = el("div", "row");
  if (version) row.appendChild(el("span", "badge", version));
  row.appendChild(copy);
  return [el("div", "label", label), el("div", "ip", ip), row];
}

function show(action, data) {
  grid.replaceChildren();
  if (data.error) {
    setHero([el("div", "error", data.error)]);
  } else if (data.message) {
    setHero([el("div", "msg", data.message)]);
  } else if (action === "details") {
    setHero(ipBlock("Votre adresse IP publique", data.ip, data.version));
    FIELDS.forEach(function (field) {
      const item = el("div", "card item fade");
      item.appendChild(el("div", "label", field[1]));
      const value = el("div", "value", data[field[0]] || "-");
      item.appendChild(value);
      if (field[0] === "loc" && data.loc) {
        const parts = data.loc.split(",");
        const link = el("a", "ghost", "Voir sur la carte");
        link.href = "https://www.openstreetmap.org/?mlat=" + parts[0] + "&mlon=" + parts[1] +
                    "#map=11/" + parts[0] + "/" + parts[1];
        link.target = "_blank"; link.rel = "noopener";
        link.style.display = "inline-block"; link.style.marginTop = "8px";
        item.appendChild(link);
      }
      grid.appendChild(item);
    });
  } else {
    setHero(ipBlock(action === "ipv4" ? "Votre IPv4 publique" : "Votre IPv6 publique", data.ip,
                    action === "ipv4" ? "IPv4" : "IPv6"));
  }
}

async function load(action) {
  tabs.forEach(function (t) { t.disabled = true; t.classList.toggle("active", t.dataset.action === action); });
  grid.replaceChildren();
  setHero([el("div", "spinner"), el("div", "label", "Chargement...")]);
  try {
    const response = await fetch("/api/" + action);
    show(action, await response.json());
  } catch (err) {
    show(action, { error: "Impossible de contacter le programme." });
  }
  tabs.forEach(function (t) { t.disabled = false; });
}

tabs.forEach(function (t) { t.addEventListener("click", function () { load(t.dataset.action); }); });
load("details");
</script>
</body>
</html>
"""


class WebApplication:
    """Logique de l'application : meme travail que main.py, mais renvoie des dictionnaires."""

    def __init__(self, client=None):
        self._client = client or IPClient()

    def ipv4(self):
        return {"ip": self._client.get_ipv4()}

    def ipv6(self):
        ip = self._client.get_ipv6()
        # api64.ipify.org renvoie une IPv4 si le reseau n'a pas d'IPv6
        if IPInfo(ip).ip_version != 6:
            return {"message": "Aucune adresse IPv6 disponible sur ce reseau."}
        return {"ip": ip}

    def details(self):
        ip = self._client.get_ipv4()
        data = self._client.get_details(ip)
        info = IPInfo(
            ip=ip,
            city=data.get("city"),
            region=data.get("region"),
            country=data.get("country"),
            isp=data.get("org"),  # ipinfo.io appelle le fournisseur "org"
            timezone=data.get("timezone"),
            loc=data.get("loc"),
        )
        result = info.to_dict()
        result["version"] = "IPv" + str(info.ip_version)
        return result


def make_handler(app):
    """Cree la classe qui repond aux requetes du navigateur."""

    routes = {"/api/ipv4": app.ipv4, "/api/ipv6": app.ipv6, "/api/details": app.details}

    class Handler(BaseHTTPRequestHandler):

        def _send(self, status, content_type, body):
            data = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type + "; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                self._send(200, "text/html", PAGE)
            elif self.path in routes:
                try:
                    payload, status = routes[self.path](), 200
                except (APIError, ValueError) as error:
                    payload, status = {"error": str(error)}, 502
                self._send(status, "application/json", json.dumps(payload, ensure_ascii=False))
            else:
                self._send(404, "text/plain", "Page introuvable")

        def log_message(self, format, *args):
            pass  # garde le terminal propre

    return Handler


def run(app=None, port=8000, open_browser=True):
    app = app or WebApplication()
    server = None
    for candidate in range(port, port + 10):  # essaie quelques ports si l'un est pris
        try:
            server = ThreadingHTTPServer(("127.0.0.1", candidate), make_handler(app))
            break
        except OSError:
            continue
    if server is None:
        print("Aucun port libre trouve.")
        return
    url = f"http://127.0.0.1:{server.server_address[1]}"
    print(f"Application disponible sur {url}  (Ctrl + C pour arreter)")
    if open_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArret.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
