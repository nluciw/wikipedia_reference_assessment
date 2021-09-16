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

    # Go through all list items in the ordered list
    for ref in references.findAll('li'):
        ref_text = ref.find(class_='reference-text')

        # Sometimes they don't use the reference-text class
        if ref_text is not None:
            citations.append(ref_text.text)
        else:
            # Sometimes they use a cite class
            for subref in ref.findAll('cite'):
                citations.append(subref.text)

        # Sometimes there's no link
        try:
            link = ref.find(class_='external text').get('href')
        except:
            link = 'NA'
        
        links.append(link)

    # Put into DataFrame for easier handling
    df = pd.DataFrame({'Ref #':range(1,1+len(citations)), 
                       'Citation': citations, 
                       'Link': links})

    return df