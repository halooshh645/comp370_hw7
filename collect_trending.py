import argparse
from bs4 import BeautifulSoup as BS
import requests
import json
import subprocess
import os.path

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", required=True, help="Path to output jason file")
    args = parser.parse_args()


    with open("index.html", 'r') as f:
        html_content = f.read()

        parser_soup = BS(html_content, 'html.parser')

        trending_links = parser_soup.select('.secondary-navigation__link')

        articles = []
        for link in trending_links:
            article = {}
            url = link['href'] # href is an attribute => trying to retrieve value  of attribute => use [] VS. select searches for elements (using attributes or elements)

            filename = url.replace("https://", "").replace("/", "_") +".html"

            if not os.path.exists(filename):
                subprocess.run(["wget", "-q", "-O", filename, url], check=True) #access denied with requests

            with open(filename, "r") as f:
                html_info = f.read()

                parser_info = BS(html_info, 'html.parser')

                title = parser_info.select_one('.postmedia-article-topper__headline').text.strip()
                pub_date = parser_info.select_one('.author-meta__date').text.strip()
                author = parser_info.select_one('.author-meta__names').text.strip()
                blurb = parser_info.select_one('.postmedia-article-topper__excerpt').text.strip()

                article = {
                    "title": title,
                    "publication_date": pub_date,
                    "author": author,
                    "blurb": blurb
                    }

                articles.append(article)

    with open(args.output, 'w') as f:
        json.dump(articles, f, indent=4, ensure_ascii=False) # converts python objects to JSON format and writes JSON Into the file
        # ensure_ascii=False prevents json from converting non-ASCII characters into Unicode









if __name__ == "__main__":
    main()
