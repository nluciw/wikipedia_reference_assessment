import argparse
from bs4 import BeautifulSoup
from utils import parse_html, gen_report
import requests

arg_parser = argparse.ArgumentParser(description='Generate a report of the references in a Wikipedia article')
arg_parser.add_argument('wiki_link', help='link to the Wikipedia article', type=str)
arg_parser.add_argument('--output_report', default='wiki-article_report', help='name of the report to output')

args = arg_parser.parse_args()

html = requests.get(url=args.wiki_link)
soup = BeautifulSoup(html.content, 'html.parser')

# Get title string
title = parse_html.get_title(soup)

references = parse_html.get_references(soup)

report = gen_report.Report(filename = args.output_report + '.md')

report.gen_report(title, references, use_hyperlinks=True)