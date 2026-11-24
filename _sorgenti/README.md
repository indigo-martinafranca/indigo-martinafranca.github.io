# App inDigo – file di lavoro

Pubblicata su https://app.indigoshop.it (GitHub Pages, repo indigo-martinafranca.github.io, ramo main).

## Come si aggiorna
1. Modifica `app.template.html` (contenuti in `CONFIG`: negozi, banner, orari, Shopping List).
2. Da questa cartella: `python3 build.py` → crea `index.html` e `version.json`.
   Anteprima con contenuti in bozza/futuri: `python3 build.py --preview` → `preview.html`.
3. Copia `index.html` e `version.json` nella radice del repo, poi commit e push su main.
   L'app installata si aggiorna da sola quando cambia `version.json`.

## Note
- Banner: campi `from` / `until` (AAAA-MM-GG) per attivazione e scadenza automatiche; `draft:true` = solo anteprima.
- Shopping List Natale 2026: attiva automaticamente dal 2026-12-01 (oggetto `SL`, pagina `#shopping`), immagini in `/photos/sl/`.
- Foto negozi: `/photos/<negozio>/`. Favicon: cartella `fav/`.
- Loghi brand: `logos_embed.json`. Brand per negozio: `brands.json`.
- Dominio: CNAME `app` su indigoshop.it (DNS OVH gestito dalla web agency) → indigo-martinafranca.github.io.
