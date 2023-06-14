import requests
from bs4 import BeautifulSoup

def get_citations_needed_count(url):
    """
    Count the number of citations needed on a Wikipedia page.

    Args:
        url (str): The URL of the Wikipedia page.

    Returns:
        int: The number of citations needed.
    """
    # Make a GET request to the URL
    response = requests.get(url)
    # Create a BeautifulSoup object from the response HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all the <sup> tags with the class 'noprint Inline-Template Template-Fact'
    citation_tags = soup.find_all('sup', class_='noprint Inline-Template Template-Fact')
    # Return the count of citation tags
    return len(citation_tags)

def get_citations_needed_report(url):
    """
    Generate a report of the passages that need citations on a Wikipedia page.

    Args:
        url (str): The URL of the Wikipedia page.

    Returns:
        str: The report containing the passages that need citations.
    """
    # Make a GET request to the URL
    response = requests.get(url)
    # Create a BeautifulSoup object from the response HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all the <sup> tags with the class 'noprint Inline-Template Template-Fact'
    citation_tags = soup.find_all('sup', class_='noprint Inline-Template Template-Fact')
    # Initialize an empty report string
    report = ""
    # Iterate over each citation tag
    for tag in citation_tags:
        # Find the parent <p> element of the citation tag
        parent_paragraph = tag.find_parent('p')
        # Append the text of the parent paragraph to the report string, stripping any extra whitespace
        report += parent_paragraph.text.strip() + '\n\n'
    # Return the report string
    return report


# stretch goal code:
def get_citations_needed_by_section(url):
    """
    Organize the passages that need citations on a Wikipedia page by section.

    Args:
        url (str): The URL of the Wikipedia page.

    Returns:
        dict: A dictionary where the keys are section names and the values are lists of passages that need citations.
    """
    # Make a GET request to the URL
    response = requests.get(url)
    # Create a BeautifulSoup object from the response HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all the <sup> tags with the class 'noprint Inline-Template Template-Fact'
    citation_tags = soup.find_all('sup', class_='noprint Inline-Template Template-Fact')
    # Create an empty dictionary to store citations by section
    citations_by_section = {}
    # Iterate over each citation tag
    for tag in citation_tags:
        # Find the parent heading element (e.g., <h1>, <h2>, etc.) of the citation tag
        parent_heading = tag.find_parent(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        # If a parent heading exists
        if parent_heading is not None:
            # Get the text of the parent heading, stripping any extra whitespace
            section_name = parent_heading.text.strip()
            # Find the parent <p> element of the citation tag
            parent_paragraph = tag.find_parent('p')
            # Get the text of the parent paragraph, stripping any extra whitespace
            citation_text = parent_paragraph.text.strip()
            # If the section name already exists in the citations dictionary, append the citation text to the existing list
            if section_name in citations_by_section:
                citations_by_section[section_name].append(citation_text)
            # Otherwise, create a new list with the citation text under the section name
            else:
                citations_by_section[section_name] = [citation_text]
    # Return the citations organized by section
    return citations_by_section

def main():
    """
    Main function to run the web scraping and generate reports.
    """
    url = 'https://en.wikipedia.org/wiki/History_of_Mexico'
    # Get the count of citations needed
    citations_count = get_citations_needed_count(url)
    # Generate the citations report
    citations_report = get_citations_needed_report(url)
    # Print the count and the report
    print(f"Number of citations needed: {citations_count}")
    print("Citations report:")
    print(citations_report)

    # Get the citations organized by section
    citations_by_section = get_citations_needed_by_section(url)
    # Print the citations by section
    print("Citations by section:")
    for section, citations in citations_by_section.items():
        print(f"Section: {section}")
        for citation in citations:
            print(citation)
        print()

if __name__ == '__main__':
    main()
