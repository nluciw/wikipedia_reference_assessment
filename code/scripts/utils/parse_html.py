import pandas as pd

def get_title(soup):
    # Get title string
    title = soup.find(class_='firstHeading').text

    return title

def get_link(ref):
    # Sometimes there's no link
    try:
        link = ref.find(class_='external text').get('href')
    except:
        link = 'NA'
    
    return link

def get_references(soup):
    # Get last ordered list from the HTML file
    references = soup.findAll('ol')[-1]

    citations = []
    links = []

    # Go through all list items in the ordered list
    for ref in references.findAll('li'):
        ref_texts = ref.findAll('cite')

        # Sometimes the cite tag is not used
        if len(ref_texts)!=0:
            for subref in ref.findAll('cite'):
                citations.append(subref.text)
                links.append(get_link(subref))
        # Sometimes they use this reference-text class
        elif ref.find(class_='reference-text') is not None:
            citations.append(ref.find(class_='reference-text').text)
            links.append(get_link(ref))
        else:
            citations.append('Could not parse citation.')
            links.append('Could not parse citation.')

    # Put into DataFrame for easier handling
    df = pd.DataFrame({'Ref #':range(1,1+len(citations)), 
                       'Citation': citations, 
                       'Link': links})

    return df