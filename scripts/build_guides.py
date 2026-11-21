"""Builds the how-to guide pages (how-to-*.html) and guides.html from the content below.

    python scripts/build_guides.py

Guides are honest how-tos: they mention the free built-in options first and our app as one option, so they are
useful to readers and to search engines. Each page carries HowTo + FAQPage structured data.
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://sc-software-tools.github.io/sc-utility-suite-dist/"
UPDATED = "2026-11-21"

GUIDES = [
 dict(slug="how-to-open-heic-on-windows", app="HeicStudio", app_name="HEIC Studio", landing="heic-to-jpg.html",
  title="How to Open and Convert HEIC Photos on Windows 10 and 11",
  desc="Three ways to open iPhone HEIC photos on a Windows PC: Microsoft's extensions, an iPhone setting, or converting them to JPG offline with HEIC Studio.",
  intro="Photos copied from an iPhone or iPad usually end in .HEIC. Windows often shows them as blank icons or says it needs an extension. Here are three ways to fix it, from the quickest to the most flexible.",
  sections=[
   ("Option 1: Install Microsoft's HEIF and HEVC extensions",
    "Windows can open HEIC photos in the Photos app once two extensions from the Microsoft Store are installed: <strong>HEIF Image Extensions</strong> (free) and <strong>HEVC Video Extensions</strong> (a small one-off charge). This lets you view photos, but other programs and websites still may not accept HEIC files."),
   ("Option 2: Make your iPhone save JPG in future",
    "On the iPhone open <strong>Settings &gt; Camera &gt; Formats</strong> and choose <strong>Most Compatible</strong>. New photos are saved as JPG. This doesn't change photos you've already taken, and the files are larger."),
   ("Option 3: Convert HEIC to JPG on your PC (free, offline)",
    "If you need ordinary JPG or PNG files for email, printing or uploading, convert them. Online converters work, but they upload your personal photos to someone else's server. <a href=\"heic-to-jpg.html\">HEIC Studio</a> converts on your own PC and includes its own decoder, so it works without the paid extensions."),
  ],
  steps=[("Install HEIC Studio", "Get it free from the Microsoft Store or as an installer, portable ZIP or Linux package from the HEIC Studio page."),
         ("Add your photos", "Drag HEIC photos, or a whole folder, into the window, or click Add Files."),
         ("Choose a format", "Pick JPG (best for sharing), PNG, WebP or PDF, and set the quality."),
         ("Remove location if sharing", "Tick Remove location (GPS) to strip where the photo was taken."),
         ("Convert", "Click Convert Files. The date taken, camera and colour profile are kept and photos are turned upright.")],
  faq=[("Is converting HEIC to JPG free?", "Yes. HEIC Studio converts up to 5 photos per batch for free, with every format. A one-time PRO upgrade removes the batch limit."),
       ("Will I lose quality?", "JPG is compressed, so set the quality slider to 90 or higher for near-identical results, or choose PNG for no further loss."),
       ("Do my photos get uploaded?", "No. HEIC Studio runs entirely on your computer.")]),
 dict(slug="how-to-merge-pdf-files-offline", app="PdfKnife", app_name="PDF Knife", landing="pdf-tools.html",
  title="How to Merge PDF Files Offline on Windows and Linux",
  desc="Combine several PDFs into one document without uploading them to a website. Step-by-step for Windows and Linux, plus how to split and extract pages.",
  intro="Merging PDFs is easy on websites, but those sites see every page you upload: contracts, payslips, medical letters. Here's how to do it on your own computer instead.",
  sections=[
   ("Why not use an online PDF merger?", "Online tools upload your files to their servers. Even with good intentions, you can't check what happens to them afterwards. For anything personal or confidential, an offline tool is the safer choice."),
   ("On Linux, there's also a command line option", "If you're comfortable with a terminal, <code>qpdf --empty --pages a.pdf b.pdf -- merged.pdf</code> merges files (install the <code>qpdf</code> package first). PDF Knife does the same with drag and drop."),
  ],
  steps=[("Install PDF Knife", "Free from the Microsoft Store, or as an installer, portable ZIP or Linux package from the PDF Knife page."),
         ("Add the PDFs", "Drag the files into the window in any order."),
         ("Put them in order", "Use the arrows to move each file up or down. The merged document follows this order."),
         ("Merge", "Choose Merge and save. Your new PDF opens in the output folder."),
         ("Need only some pages?", "Use Extract and type a range such as 3-7, or Burst to save every page as its own file.")],
  faq=[("Is it free?", "Merging 2 PDFs at a time and extracting one page range are free. A one-time PRO upgrade merges any number of files, extracts several ranges at once and bursts whole documents."),
       ("Does it add a watermark?", "No. Nothing is added to your documents."),
       ("Does it work offline?", "Yes, completely. Nothing is uploaded.")]),
 dict(slug="how-to-open-rar-and-7z-files", app="ArchiveUnpacker", app_name="Archive Unpacker", landing="archive-extractor.html",
  title="How to Open RAR and 7z Files on Windows and Linux",
  desc="Open and extract RAR, 7z, ZIP, TAR and GZ archives on Windows 10, Windows 11 and Linux, including password-protected archives, without trial software.",
  intro="RAR and 7z are common for downloads and shared folders, but older Windows versions can't open them, and some tools nag you to buy a licence. Here's what works.",
  sections=[
   ("Windows 11: try File Explorer first", "Recent Windows 11 updates can extract RAR and 7z files from File Explorer: right-click the file and choose <strong>Extract All</strong>. If that option is missing (Windows 10 or older Windows 11), or the archive is password-protected or split into parts, use a dedicated tool."),
   ("Linux: use your package manager or a desktop app", "Most desktops open ZIP and TAR out of the box. For RAR and 7z install <code>unrar</code> and <code>7zip</code> (or <code>p7zip</code>), or use Archive Unpacker from the Snap Store, a .deb or a .tar.gz."),
   ("Watch out for unsafe archives", "A badly made or malicious archive can try to write files outside the folder you chose. Archive Unpacker checks every path and blocks this."),
  ],
  steps=[("Install Archive Unpacker", "Free from the Microsoft Store, the Snap Store, or as an installer or package from the Archive Unpacker page."),
         ("Open the archive", "Double-click it, drag it into the window, or right-click it in File Explorer and choose Extract."),
         ("Check what's inside", "Browse the file list before extracting."),
         ("Enter the password if asked", "Password-protected archives prompt for the password."),
         ("Extract", "Pick a folder and extract. You can also create ZIP files from your own folders.")],
  faq=[("Is it free?", "Extracting one archive at a time and creating ZIP files are free. A one-time PRO upgrade extracts many archives at once and adds TAR.GZ creation and maximum compression."),
       ("Does it open RAR5?", "Yes, both RAR4 and RAR5."),
       ("Is there a trial period or nag screen?", "No. The free features stay free.")]),
 dict(slug="how-to-make-a-bootable-usb", app="UsbFlasher", app_name="USB Flasher", landing="usb-imager.html",
  title="How to Make a Bootable USB Drive from an ISO (Windows and Linux)",
  desc="Write a Linux or Windows ISO to a USB stick safely on Windows or Linux, verify it, and avoid erasing the wrong drive.",
  intro="To install Linux, reinstall Windows or run a rescue tool, you need the ISO image written to a USB stick, not just copied onto it. Here's how to do it safely.",
  sections=[
   ("Before you start", "You need the ISO file, a USB stick at least as big as the image (8 GB is usually enough), and a backup of anything on the stick: <strong>writing an image erases the whole drive</strong>."),
   ("Choosing a tool", "Well-known free tools include Rufus (Windows) and balenaEtcher. USB Flasher focuses on safety: it lists only removable USB drives, never your system disks, and asks you to confirm the exact drive before erasing anything."),
   ("Windows installer ISOs", "Microsoft's own Media Creation Tool is the simplest way to make a Windows 10 or 11 installer, because Windows ISOs contain a file too large for some USB formats."),
  ],
  steps=[("Install USB Flasher", "Free for Windows (installer or portable) and Linux (Snap Store, .deb, .tar.gz) from the USB Flasher page."),
         ("Choose the image", "Select your .iso, .img or .bin file."),
         ("Pick the USB drive", "Only removable drives are listed. Check the size and name carefully."),
         ("Confirm and write", "Confirm the drive. Everything on it is replaced by the image."),
         ("Verify", "Let USB Flasher verify the drive after writing, then boot from it.")],
  faq=[("Is it free?", "Writing and verifying one drive at a time is free. A one-time PRO upgrade writes several drives at once and backs up a USB drive to an image."),
       ("Can it erase my hard drive by mistake?", "It only lists removable USB drives and asks you to confirm the exact one."),
       ("Does it work on Linux?", "Yes, as a snap, a .deb or a portable .tar.gz.")]),
]


def page(g):
    url = SITE + g["slug"] + ".html"
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": g["title"], "description": g["desc"],
             "step": [{"@type": "HowToStep", "position": i, "name": n, "text": t} for i, (n, t) in enumerate(g["steps"], 1)]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in g["faq"]]}
    e = html.escape
    sections = "\n".join(f'      <h2>{e(h)}</h2>\n      <p>{body}</p>' for h, body in g["sections"])
    steps = "\n".join(f'        <li><strong>{e(n)}.</strong> {e(t)}</li>' for n, t in g["steps"])
    faqs = "\n".join(f'      <details class="guide-faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in g["faq"])
    others = " · ".join(f'<a href="{o["slug"]}.html">{e(o["title"].split(" (")[0])}</a>' for o in GUIDES if o is not g)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(g["title"])} | SC Utility Suite</title>
  <meta name="description" content="{e(g["desc"])}">
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{e(g["title"])}">
  <meta property="og:description" content="{e(g["desc"])}">
  <meta property="og:image" content="{SITE}assets/screenshots/{g["app"]}.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="shortcut icon" href="favicon.ico?v=4">
  <link rel="stylesheet" href="style.css?v=20261111.3">
  <link rel="stylesheet" href="assets/redesign.css?v=20261117.5">
  <script type="application/ld+json">{json.dumps(howto)}</script>
  <script type="application/ld+json">{json.dumps(faq)}</script>
  <style>
    .guide {{ max-width: 760px; margin: 0 auto; padding: 48px 16px 64px; }}
    .guide h1 {{ font-size: clamp(1.7rem, 4vw, 2.4rem); line-height: 1.2; margin-bottom: 12px; }}
    .guide h2 {{ font-size: 1.3rem; margin: 32px 0 10px; }}
    .guide p, .guide li {{ line-height: 1.7; color: var(--text-secondary, #c7cbd4); }}
    .guide ol {{ padding-left: 22px; }} .guide li {{ margin: 8px 0; }}
    .guide .updated {{ color: var(--text-muted, #8b90a0); font-size: 0.85rem; }}
    .guide-cta {{ margin: 28px 0; padding: 18px; border: 1px solid var(--border-subtle, #2a2f3a); border-radius: 12px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between; }}
    .guide-faq {{ border-bottom: 1px solid var(--border-subtle, #2a2f3a); padding: 12px 0; }}
    .guide-faq summary {{ cursor: pointer; font-weight: 600; }}
    .guide code {{ background: rgba(255,255,255,0.07); padding: 1px 6px; border-radius: 4px; overflow-wrap: anywhere; }}
    .guide-more {{ margin-top: 40px; font-size: 0.92rem; }}
    .guide p a, .guide li a {{ color: #38BDF8; }}
  </style>
</head>
<body data-app-theme="{g["app"]}">
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="navbar">
    <div class="nav-container container">
      <a class="brand" href="index.html" aria-label="SC Utility Suite Home"><img src="favicon-32x32.png" width="30" height="30" alt=""><span>SC Utility Suite</span></a>
      <nav class="nav-links" aria-label="Main navigation">
        <a href="index.html#applications">All 7 Apps</a>
        <a href="guides.html">Guides</a>
        <a href="{g["landing"]}">{e(g["app_name"])}</a>
      </nav>
      <a class="nav-download" href="{g["landing"]}#download">Download <span aria-hidden="true">↓</span></a>
    </div>
  </header>
  <main id="main">
    <article class="guide">
      <p class="updated">Guide · Updated {UPDATED}</p>
      <h1>{e(g["title"])}</h1>
      <p>{e(g["intro"])}</p>
{sections}
      <h2>Step by step with {e(g["app_name"])}</h2>
      <ol>
{steps}
      </ol>
      <div class="guide-cta">
        <span><strong>{e(g["app_name"])}</strong> is free, works offline and runs on Windows and Linux.</span>
        <a class="btn btn-fluent-primary" href="{g["landing"]}#download">Get {e(g["app_name"])}</a>
      </div>
      <h2>Questions</h2>
{faqs}
      <p class="guide-more">More guides: {others}</p>
    </article>
  </main>
  <footer class="footer">
    <div class="container footer-content">
      <div><a class="brand" href="index.html"><img src="favicon-32x32.png" width="24" height="24" alt=""><span>SC Utility Suite</span></a>
        <p class="copyright">© 2026 SC Software</p></div>
      <nav class="footer-links" aria-label="Footer navigation">
        <a href="index.html">Home</a><a href="guides.html">Guides</a><a href="privacy/">Privacy Policy</a><a href="mailto:sc-developer@outlook.com">Contact</a>
      </nav>
    </div>
    <p class="container trademark-note">Windows and Microsoft Store are trademarks of Microsoft Corporation.</p>
  </footer>
  <script data-goatcounter="https://sc-software.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</body>
</html>
"""


def index_page():
    items = "\n".join(f'        <li><a href="{g["slug"]}.html"><strong>{html.escape(g["title"])}</strong></a><br><span>{html.escape(g["desc"])}</span></li>' for g in GUIDES)
    body = page(dict(GUIDES[0], slug="guides", title="How-to Guides", desc="Plain guides for everyday PC jobs: HEIC photos, PDFs, RAR and 7z archives and bootable USB drives.",
                     intro="", sections=[], steps=[], faq=[]))
    start, end = body.index('<article class="guide">'), body.index('</article>')
    article = f"""<article class="guide">
      <h1>How-to Guides</h1>
      <p>Plain, honest guides for everyday PC jobs. Each one covers the free built-in options first.</p>
      <ul style="list-style:none;padding:0;display:grid;gap:18px;">
{items}
      </ul>
    """
    body = body[:start] + article + body[end:]
    import re
    return re.sub(r'  <script type="application/ld\+json">.*?</script>\n', '', body)   # no HowTo/FAQ data on the index


def main():
    for g in GUIDES:
        (ROOT / f'{g["slug"]}.html').write_text(page(g), encoding="utf-8")
    (ROOT / "guides.html").write_text(index_page(), encoding="utf-8")
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for slug in ["guides"] + [g["slug"] for g in GUIDES]:
        loc = f"{SITE}{slug}.html"
        if loc not in sitemap:
            sitemap = sitemap.replace("</urlset>", f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{UPDATED}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n</urlset>")
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print("built", len(GUIDES), "guides + guides.html; sitemap updated")


if __name__ == "__main__":
    main()
