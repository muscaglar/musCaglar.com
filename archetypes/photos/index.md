---
title: "{{ replace .File.ContentBaseName "-" " " | humanize }}"
date: {{ .Date }}
summary: ""
# cover: picture.jpg             # optional: the first picture is used when this is left out
# location: ""                   # optional
# photos:                        # optional: captions, matched by file name
#   - file: picture.jpg
#     caption: ""
draft: true
---
