import re
import urllib

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
        self.raw_headings = raw_headings
        self.raw_text = raw_text

        self.prev_url = prev_url
        self.next_url = next_url

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
        self.clean_headings = []
        for heading in self.raw_headings:
            clean_heading = heading.strip()
            self.clean_headings.append(clean_heading)

    def _clean_text(self):
        """
        Clean up the text by removing all the extra newlines and interpolated
        letter markup.
        """
        tmp = re.sub(r'\-\n +\n +', '', self.raw_text)
        tmp = re.sub(r'\n +', ' ', tmp)
        tmp = re.sub(r' {2,}', ' ', tmp)
        tmp = re.sub(r'<(.+?)>', '\\1', tmp)
        tmp = tmp.strip()

        self.clean_text = tmp

        
class PageURLFactory:
    """
    Factory to create a page from a url.
    """

    TITLE_CLASS = 'title'
    LINE_QUERY = '//tr[not(@class)]/td[1]'

    PREV_ID = 'prev'
    NEXT_ID = 'next'

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
        for title_row in root.find_class(cls.TITLE_CLASS):
            title = title_row.text_content()
            titles.append(title)

        lines = []
        for line in root.xpath(cls.LINE_QUERY):
            line_text = line.text_content()
            lines.append(line_text)
        raw_text = ''.join(lines)

        parse = urllib.parse.urlparse(url)
        base = parse.scheme + '://' + parse.netloc

        p = root.get_element_by_id(cls.PREV_ID)
        prev_url = p.get('href')
        if prev_url:
            prev_url = urllib.parse.urljoin(base, prev_url)

        n = root.get_element_by_id(cls.NEXT_ID)
        next_url = n.get('href')
        if next_url:
            next_url = urllib.parse.urljoin(base, next_url)
        
        return Page(raw_text, titles, prev_url, next_url)
