#!/usr/bin/env python3
"""Przelicza hashe SHA-256 skryptów inline w index.html i wpisuje politykę CSP
do index.html (<meta>), _headers (Netlify / Cloudflare Pages) i .htaccess (Apache).

Uruchom po KAŻDEJ zmianie treści dowolnego <script> w index.html:
    python3 tools/update-csp.py
"""
import base64, hashlib, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"

def build_csp(html: str, with_frame_ancestors: bool) -> str:
    hashes = []
    for m in re.finditer(r"<script>(.*?)</script>", html, re.S):
        d = hashlib.sha256(m.group(1).encode("utf-8")).digest()
        hashes.append("'sha256-%s'" % base64.b64encode(d).decode())
    parts = [
        "default-src 'self'",
        # hashe = tylko nasze skrypty; 'strict-dynamic' = mogą doładować AdSense;
        # 'unsafe-inline' https: to tylko zapas dla bardzo starych przeglądarek (nowe je ignorują)
        "script-src %s 'strict-dynamic' 'unsafe-inline' https:" % " ".join(hashes),
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' https://fonts.gstatic.com",
        "img-src 'self' data: https:",
        "connect-src 'self' https:",
        "frame-src https:",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'none'",
    ]
    if with_frame_ancestors:  # działa tylko jako nagłówek HTTP, nie w <meta>
        parts.append("frame-ancestors 'none'")
    parts.append("upgrade-insecure-requests")
    return "; ".join(parts)

def main():
    html = INDEX.read_text(encoding="utf-8")
    meta = build_csp(html, False)
    html2, n = re.subn(r'(<meta http-equiv="Content-Security-Policy" content=")[^"]*(")',
                       lambda m: m.group(1) + meta + m.group(2), html)
    assert n == 1, "Brak <meta http-equiv=Content-Security-Policy> w index.html"
    INDEX.write_text(html2, encoding="utf-8")
    hdr = build_csp(html2, True)
    for name, pat, fmt in [
        ("_headers", r"(?m)^(\s*Content-Security-Policy: ).*$", "{}"),
        (".htaccess", r'(?m)^(\s*Header always set Content-Security-Policy ").*$', '{}"'),
    ]:
        f = ROOT / name
        if f.exists():
            s, k = re.subn(pat, lambda m: m.group(1) + fmt.format(hdr), f.read_text(encoding="utf-8"))
            f.write_text(s, encoding="utf-8")
            print(f"{name}: {'zaktualizowano' if k else 'BRAK linii CSP!'}")
    print("index.html: zaktualizowano CSP")

if __name__ == "__main__":
    main()
