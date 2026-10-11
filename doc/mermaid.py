"""Aperçu en direct d'un fichier Mermaid (.mmd) dans le navigateur.

Le diagramme est redessiné automatiquement à chaque enregistrement du fichier.
N'utilise que la bibliothèque standard de Python : aucun IDE ni outil externe requis.

Utilisation (depuis la racine du projet) :
    python doc/apercu_mermaid.py doc/commande.mmd
    python doc/apercu_mermaid.py doc/commande.mmd --port 8080 --sans-navigateur
"""

import argparse
import html
import json
import sys
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

CDN = "https://cdn.jsdelivr.net/npm/mermaid@12/dist/mermaid.min.js"
MERMAID_LOCAL = Path(__file__).resolve().parent / "mermaid.min.js"
ROUTE_MERMAID = "/__mermaid__.js"

PAGE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>__TITRE__</title>
<script src="__SCRIPT__"></script>
<style>
html, body {
    height: 100%;
}
body {
    margin: 0;
}
#telecharger-png {
    position: absolute;
    top : 2%;
    left : 200px;
    margin-bottom: 1rem;
    padding: .5rem 1rem;
    cursor: pointer;
}

#telecharger-svg {
    position: absolute;
    top : 2%;
    left : 20px;
    margin-bottom: 1rem;
    padding: .5rem 1rem;
    cursor: pointer;
}

.container {
    width: 100%;
    padding: 0;
    margin: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  #diagramme svg {
    margin: auto;
    height: auto;
    display: block;
  }
  #diagramme { width: 100%;}
  #erreur { color: #c0392b; white-space: pre-wrap; font-family: monospace; }
</style>
</head>
<body>
<div class="container">
    <button id="telecharger-svg">Télécharger en SVG</button>
    <button id="telecharger-png">Télécharger en PNG</button>
    <div id="erreur"></div>
    <div id="diagramme"></div>
</div>
<script>
  mermaid.initialize({ startOnLoad: false });
  const fichier = __FICHIER_JS__;
  const zone = document.getElementById("diagramme");
  const erreur = document.getElementById("erreur");
  let dernier = null;
  let compteur = 0;

  async function verifier() {
    try {
      const url = encodeURIComponent(fichier) + "?t=" + Date.now();
      const rep = await fetch(url, { cache: "no-store" });
      if (!rep.ok) throw new Error("Fichier introuvable : " + fichier);
      const texte = await rep.text();
      if (texte === dernier) return;
      dernier = texte;

      const id = "graphe" + compteur++;
      try {
        const { svg } = await mermaid.render(id, texte);
        zone.innerHTML = svg;
        erreur.textContent = "";
      } catch (e) {
        document.getElementById("d" + id)?.remove();
        erreur.textContent = e.message || String(e);
      }
    } catch (e) {
      erreur.textContent = e.message;
    }
  }

  // Fonction utilitaire pour renommer l'extension proprement
  function getNomFichier(ext) {
      if (fichier.endsWith(".mmd")) {
          return fichier.slice(0, -4) + ext;
      }
      return fichier + ext;
  }

  document.getElementById("telecharger-svg").onclick = () => {
    const svg = zone.querySelector("svg");
    if (!svg) return;
    const contenu = new XMLSerializer().serializeToString(svg);
    const lien = document.createElement("a");
    lien.href = URL.createObjectURL(new Blob([contenu], { type: "image/svg+xml" }));
    lien.download = getNomFichier(".svg");
    lien.click();
  };

  document.getElementById("telecharger-png").onclick = () => {
      const svg = zone.querySelector("svg");
      if (!svg) return;

      // 1. Récupérer les dimensions exactes via le viewBox (plus précis que clientWidth)
      let width = 800;
      let height = 600;
      const viewBox = svg.getAttribute("viewBox");
      if (viewBox) {
          const parts = viewBox.split(/[\\s,]+/);
          if (parts.length === 4) {
              width = parseFloat(parts[2]);
              height = parseFloat(parts[3]);
          }
      } else {
          width = svg.clientWidth || 800;
          height = svg.clientHeight || 600;
      }

      // 2. Facteur de qualité (2x ou 3x) pour éviter le flou et la petite taille
      const scale = 2;

      // 3. Sérialiser le SVG en chaîne de caractères
      const contenu = new XMLSerializer().serializeToString(svg);
      const svgBlob = new Blob([contenu], { type: "image/svg+xml;charset=utf-8" });
      const url = URL.createObjectURL(svgBlob);

      const image = new Image();
      image.onload = () => {
          const canvas = document.createElement("canvas");
          canvas.width = width * scale;
          canvas.height = height * scale;

          const ctx = canvas.getContext("2d");

          ctx.fillStyle = "#ffffff"; // Définit la couleur blanche
          ctx.fillRect(0, 0, canvas.width, canvas.height); // Remplit tout le fond en blanc

          // Appliquer l'échelle pour garder la haute définition
          ctx.scale(scale, scale);
          ctx.drawImage(image, 0, 0, width, height);

          URL.revokeObjectURL(url);

          const lien = document.createElement("a");
          lien.href = canvas.toDataURL("image/png");
          lien.download = getNomFichier(".png");
          lien.click();
      };

      image.src = url;
  };

  verifier();
  setInterval(verifier, 1000);
</script>
</body>
</html>
"""


class Gestionnaire(SimpleHTTPRequestHandler):
    """Sert la page d'aperçu, Mermaid (si embarqué) et les fichiers du dossier."""

    page = b""

    def do_GET(self):
        chemin = self.path.split("?", 1)[0]
        if chemin in ("/", "/index.html"):
            self._envoyer(self.page, "text/html; charset=utf-8")
        elif chemin == ROUTE_MERMAID and MERMAID_LOCAL.exists():
            self._envoyer(MERMAID_LOCAL.read_bytes(), "text/javascript; charset=utf-8")
        else:
            super().do_GET()

    def _envoyer(self, contenu, type_mime):
        self.send_response(200)
        self.send_header("Content-Type", type_mime)
        self.send_header("Content-Length", str(len(contenu)))
        self.end_headers()
        self.wfile.write(contenu)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, format: str, *args: Any):
        pass  # évite d'afficher une ligne par requête


def construire_page(fichier):
    script = ROUTE_MERMAID if MERMAID_LOCAL.exists() else CDN
    return (
        PAGE.replace("__TITRE__", html.escape(fichier.name))
        .replace("__SCRIPT__", script)
        .replace("__FICHIER_JS__", json.dumps(fichier.name))
        .encode("utf8")
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="apercu_mermaid",
        description="Aperçu en direct d'un diagramme Mermaid dans le navigateur.",
    )
    parser.add_argument("fichier", type=Path, help="fichier Mermaid (.mmd) à afficher")
    parser.add_argument(
        "--port", type=int, default=8000, help="port du serveur (défaut : 8000)"
    )
    parser.add_argument(
        "--sans-navigateur",
        action="store_true",
        help="ne pas ouvrir le navigateur automatiquement",
    )
    args = parser.parse_args(argv)

    fichier = args.fichier.resolve()
    if not fichier.is_file():
        sys.exit(f"Fichier introuvable : {fichier}")

    Gestionnaire.page = construire_page(fichier)
    dossier = str(fichier.parent)

    def fabrique(*a, **k):
        return Gestionnaire(*a, directory=dossier, **k)

    try:
        serveur = ThreadingHTTPServer(("127.0.0.1", args.port), fabrique)
    except OSError:
        sys.exit(f"Le port {args.port} est déjà utilisé. Essaie avec --port 8001.")

    url = f"http://127.0.0.1:{args.port}/"
    print(f"Aperçu de {fichier.name} sur {url} (Ctrl+C pour arrêter)")
    if not args.sans_navigateur:
        webbrowser.open(url)

    try:
        serveur.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du serveur.")
    finally:
        serveur.server_close()


if __name__ == "__main__":
    main()
