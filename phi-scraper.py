#!/usr/bin/env python

import phi

START_PAGE = 'http://latin.packhum.org/loc/978/1/0'

total_text = []

page = phi.PageURLFactory.create(START_PAGE)
for heading in page.clean_headings:
    total_text.append(heading)
total_text.append(page.clean_text)

while page.next_url:
    next_page = phi.PageURLFactory.create(page.next_url)
    for heading in next_page.clean_headings:
        total_text.append(heading)
    total_text.append(next_page.clean_text)

    page = next_page

final = '\n\n'.join(total_text)
print(final)
