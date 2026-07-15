import json
import re
import sys

CH_TITLES = {
    1: ("वयं वर्णमालां पठामः", "We Study the Alphabet"),
    2: ("संयुक्त-व्यञ्जनानि", "Conjunct Consonants"),
}

def build(ch_num):
    with open("chapter1.html", encoding="utf-8") as f:
        html = f.read()

    with open(f"content/sanskrit{ch_num}_qa.json", encoding="utf-8") as f:
        data = json.load(f)

    sa_title, en_title = CH_TITLES[ch_num]
    data_js = json.dumps(data, ensure_ascii=False)

    # Title / meta
    html = html.replace(
        "<title>Chapter 1: Patterns in Mathematics — Maths Buddy</title>",
        f"<title>Chapter {ch_num}: {sa_title} — Sanskrit Buddy</title>"
    )
    html = re.sub(
        r'<meta name="description"[^>]*/>',
        f'<meta name="description" content="Practice questions and answers for Class 6 Sanskrit Chapter {ch_num}: {sa_title} ({en_title}) — NCERT Deepakam"/>',
        html, count=1
    )

    # Emoji + header text + back link target
    html = html.replace('🧮 Maths Buddy', '🕉️ Sanskrit Buddy')
    html = html.replace(
        f'<p>Class 6 · Chapter 1: Patterns in Mathematics</p>',
        f'<p>Class 6 · अध्यायः {ch_num}: {sa_title} ({en_title})</p>'
    )
    html = html.replace('href="index.html"', 'href="sanskrit_index.html"')

    # Devanagari-friendly font stack
    html = html.replace(
        "font-family: 'Segoe UI', Tahoma, sans-serif;",
        "font-family: 'Nirmala UI', 'Noto Sans Devanagari', 'Segoe UI', Tahoma, sans-serif;"
    )

    # English-translation styling
    html = html.replace(
        "    .card-imgs {",
        "    .en-translation {\n"
        "      font-size: 0.82rem;\n"
        "      color: #6b7280;\n"
        "      font-style: italic;\n"
        "      margin-top: 10px;\n"
        "      line-height: 1.5;\n"
        "      white-space: pre-wrap;\n"
        "    }\n\n"
        "    .card-imgs {"
    )

    # Insert translation paragraphs under the question and answer text
    html = html.replace(
        '<p id="q-text"></p>',
        '<p id="q-text"></p>\n      <p class="en-translation" id="q-text-en"></p>'
    )
    html = html.replace(
        '<p id="a-text"></p>',
        '<p id="a-text"></p>\n      <p class="en-translation" id="a-text-en"></p>'
    )

    # Inject DATA (lambda replacement avoids re.sub backslash-escape corruption)
    html = re.sub(
        r"const DATA = \[.*?\];\n",
        lambda m: f"const DATA = {data_js};\n",
        html, count=1, flags=re.DOTALL
    )

    # No images for Sanskrit chapters — empty IMAGE_MAP
    html = re.sub(
        r"const IMAGE_MAP = \{.*?\};\n",
        lambda m: "const IMAGE_MAP = {};\n",
        html, count=1, flags=re.DOTALL
    )
    html = html.replace("'images/ch1/' + f", "'images/sanskrit" + str(ch_num) + "/' + f")

    # Render English translations alongside q-text / a-text
    html = html.replace(
        "document.getElementById('q-text').textContent = q.q;",
        "document.getElementById('q-text').textContent = q.q;\n"
        "    document.getElementById('q-text-en').textContent = q.qEn || '';"
    )
    html = html.replace(
        "document.getElementById('a-text').textContent = q.a;",
        "document.getElementById('a-text').textContent = q.a;\n"
        "    document.getElementById('a-text-en').textContent = q.aEn || '';"
    )

    out_path = f"sanskrit{ch_num}.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {out_path}")

if __name__ == "__main__":
    for n in (1, 2):
        build(n)
