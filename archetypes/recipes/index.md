---
title: "{{ replace .File.ContentBaseName "-" " " | humanize }}"
date: {{ .Date }}
summary: "One line about the dish."
course: main                    # snack | breakfast | main | side | dessert | coffee: the heading it is listed under
status: tested                  # tested | developing (made, not settled yet) | concept (an idea, not made yet)
time: ""                        # for example "45 min"
makes: ""                       # for example "Serves 4"
tags: []
# figure: figure.svg            # optional: a drawing in this folder (see "Drawings" in README.md)
# figure_caption: "What the drawing shows."
# cover: picture.jpg            # optional: a picture in this folder
ingredients:
  - 
# develop:                      # optional: what is still to be worked out. The page shows the list.
#   - "How long the dough rests."
draft: true
---

1. 
