import sys
import pypandoc

def make_row(row):
    print('| ', end='')
    for item in row:
        print(f'{item} | ', end='')
    print(' ')

def make_table(data, blank_lines=False):
    columns = list(data.columns)

    make_row(columns)
    
    make_row(['-']+['-----' for _ in range(len(columns)-1)])

    for idx, row in data.iterrows():
        make_row(row)
        if blank_lines:
            make_row([' ']*len(row))

def links_to_hyperlinks(links):

    new_links = []
    for link in links:
        if link=='NA':
            new_links.append('No link found.')
        else:
            text = link.split('/')[2]
            new_links.append(f'[Link on {text}]({link})')
    return new_links 

class Report:
    def __init__(self, filename='wiki_report.md'):
        self.filename = filename

    def gen_report(self, article_title, 
                   references, keep_raw=False,
                   use_hyperlinks=False):

        original_stdout = sys.stdout

        if use_hyperlinks:
            references.Link = links_to_hyperlinks(list(references.Link))

        with open(self.filename, 'w') as file:
            sys.stdout = file

            print(f'### Report on references of *{article_title}* Wikipedia article.')
            make_table(references, blank_lines=True)

            sys.stdout = original_stdout

        if not keep_raw:
            output = pypandoc.convert(self.filename, 'pdf', 
                outputfile=self.filename.replace('md','pdf'))
    