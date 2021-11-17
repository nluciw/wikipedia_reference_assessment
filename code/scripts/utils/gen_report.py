import sys
import pypandoc

def make_row(row):
    '''Print a single row in a Markdown-formatted table
    with each element in the row list as a separate column'''

    print('| ', end='')
    for item in row:
        print(f'{item} | ', end='')
    print(' ')

def make_table(data, blank_lines=False):
    '''Make a Markdown table. Best to use with sys stdout
    as it uses the print() function.

    data: a pandas dataframe
    blank_lines: True/False insert blank lines between rows'''

    columns = list(data.columns)

    make_row(columns)
    
    make_row(['-']+['-----' for _ in range(len(columns)-1)])

    for idx, row in data.iterrows():
        make_row(row)
        if blank_lines:
            make_row([' ']*len(row))

def links_to_hyperlinks(links):
    '''Create a list of strings in Markdown formatting
    for hyperlinks.

    links: list of the links to be turned to Markdown'''

    new_links = []
    for link in links:
        if link=='NA':
            new_links.append('No link found.')
        else:
            text = link.split('/')[2]
            new_links.append(f'[Link on {text}]({link})')
    return new_links 

class Report:
    '''Create a report in Markdown for the article.
    init with filename corresponding to the report.'''

    def __init__(self, filename='wiki_report.md'):
        self.filename = filename

    def gen_report(self, article_title, 
                   references, keep_raw=False,
                   use_hyperlinks=False):
        ''' Generate the Markdown report.
        article_title: string with title of the report
        references: pandas dataframe from the get_references function
        keep_raw: bool to delete the raw .md file after generating pdf
        use_hyperlinks: bool to use hyperlinks in md instead of link text
        '''

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
    