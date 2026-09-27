---
title: "{{ replace .File.ContentBaseName "-" " " | humanize }}"
date: {{ .Date }}
# period: "March – June 2026"   # optional: shown instead of the date
summary: "One or two sentences. Shown in lists and in link previews."
kind: tinkering                  # research | tinkering
tags: []
# cover: picture.jpg             # optional: a picture in this folder, used in lists and link previews
# featured: true                 # optional: show on the home page
# status: ongoing                # optional
links: []
#  - name: Code on GitHub
#    url: https://github.com/muscaglar/
draft: true
---

Write the project up here. To add a picture, put the file in this folder and write:

    ![What the picture shows](picture.jpg "An optional caption")
