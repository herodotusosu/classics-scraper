#!/usr/bin/env python

import phi

page = phi.URLFactory.create('http://latin.packhum.org/loc/978/1/0')
print(page._raw_text)
print()
print(page.clean_text())
