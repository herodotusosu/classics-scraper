import re

import lxml.html

class Page:
    """
    A page from the phi Latin texts. This page will have the headings on the
    page if any exist in list format. This page will also have the raw text as
    seen on the page (not including line number markings). So newlines, dashes,
    and interpolated letter marks are supposed to be present in this
    representation.
    """
    def __init__(self, raw_text, raw_headings, prev_url, next_url):
        """
        Create a new page with the given headings and text.

        Args:
        raw_text: The main text on this page.
        raw_headings: The headings, if any on this page. Should be as a list. If
                  there are no headings simply pass in an empty list.
        prev_url: The url to the previous page before this one.
        next_url: The url to the page after this one.
        """
        self._raw_headings = raw_headings
        self._raw_text = raw_text
        self._prev_url = prev_url
        self._next_url = next_url

        self._clean()

    def _clean(self):
        """
        Clean the raw text and headings that were provided. Modifies self by
        storing the results in clean_headings and clean_text.
        """
        self._clean_headings()
        self._clean_text()

    def _clean_headings(self):
        """
        Clean up each heading by removing superfluous whitespace.
        """
        self._cleaned_headings = []
        for heading in self._raw_headings:
            cleaned_heading = heading.strip()
            self._cleaned_headings.append(cleaned_heading)

    def _clean_text(self):
        """
        Clean up the text by removing all the extra newlines and interpolated
        letter markup.
        """
        tmp = self._raw_text.strip()
        tmp = re.sub(r'\-\n {2,}', '', tmp)
        tmp = re.sub(r'\n +', ' ', tmp)
        tmp = re.sub(r'  ', ' ', tmp)
        tmp = re.sub(r'<(\w+)>', '\\1', tmp)

        self._cleaned_text = tmp

    def clean_headings(self):
        """
        Provide a clean versions of the headings of this page.

        Returns:
        The clean headings.
        """
        return self._cleaned_headings

    def clean_text(self):
        """
        Provide a clean version of the text of this page.

        Returns:
        The clean text.
        """
        return self._cleaned_text

        
class URLFactory:
    """
    Factory to create a page from a url.
    """

    TITLE_CLASS = 'title'
    LINE_QUERY = '//tr[not(@class)]/td[1]'

    @classmethod
    def create(cls, url):
        """
        Create a new page from the given url.

        Args:
        url: The phi Latin url to create the page from.

        Returns:
        The created page from the url.
        """
        root = lxml.html.parse(url).getroot()
        titles = []
        for title_row in root.find_class(URLFactory.TITLE_CLASS):
            title = title_row.text_content()
            titles.append(title)

        lines = []
        for line in root.xpath(URLFactory.LINE_QUERY):
            line_text = line.text_content()
            lines.append(line_text)
        raw_text = ''.join(lines)
        
        return Page(raw_text, titles, '', '')
