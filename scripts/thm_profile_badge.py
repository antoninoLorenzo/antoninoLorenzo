"""
Fetches TryHackMe profile badge and exports it as an image.

Requires:
- os: wkhtmltopdf
- python: requests, imgkit

author: @antoninoLorenzo
"""
import os
import sys
import base64
import argparse

try:
    import requests
    import imgkit
except ImportError as err:
    print(f"Missing required library.\n{err}")
    exit()


def main():
    parser = argparse.ArgumentParser(description=__file__.__doc__)
    parser.add_argument(
        '--badge-url',
        required=True,
        help="URL of the TryHackMe profile badge"
    )
    parser.add_argument(
        '--output',
        default='../assets/thm_badge.jpg',
        help="output path for the badge image"
    )

    args = parser.parse_args()
    profile_url = args.badge_url
    output_path = args.output

    response = requests.get(
        profile_url,
        headers={
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"
        }
    )

    if response.status_code == 200:
        encoded = response.text.replace("document.write(window.atob(\"", "").replace("\"))", "")
        decoded = str(base64.b64decode(encoded).decode('utf-8'))
        decoded = f"<body>{decoded}</body>"

        tmp_html = 'tmp.html'
        with open(tmp_html, 'w', encoding='utf-8') as fp:
            fp.write(decoded)

        tmp_css = 'tmp.css'
        with open(tmp_css, 'w', encoding='utf-8') as fp:
            fp.write('body{background-color: #0d1117;}')

        # convert
        imgkit.from_file(
            tmp_html,
            output_path,
            options={
                'format': 'jpg',
                'quality': '100',
                'width': '200',  # hardcoded
                'user-style-sheet': tmp_css
            }
        )

        print(f"Badge saved: '{output_path}'")
        os.remove(tmp_html)
        os.remove(tmp_css)
    else:
        print("Request blocked by the TryHackMe.")
        exit()


if __name__ == "__main__":
    main()
