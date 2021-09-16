import pandas as pd

def get_title(soup):
    # Get title string
    title = soup.find(class_='firstHeading').text

    return title

def get_references(soup):
    # Get last ordered list from the HTML file
    references = soup.findAll('ol')[-1]

    citations = []
    links = []

    for ref in references.findAll('li'):
        name = ref.find(class_='reference-text').text

        try:
            link = ref.find(class_='external text').get('href')
        except:
            link = 'NA'

        citations.append(name)
        
        links.append(link)

    df = pd.DataFrame({'Ref #':range(1,1+len(citations)), 
                       'Citation': citations, 
                       'Link': links})

    return df