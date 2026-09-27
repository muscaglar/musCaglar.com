---
title: "Great crested newts: predicting habitats"
date: 2019-01-01
summary: "Scoring ponds along the rail network for how likely they are to hold a protected species, to cut down on costly site visits."
kind: research
tags: [R, Logistic regression, Naive Bayes, GIS]
figure: figure.svg
figure_caption: "An invented plan of ponds beside a railway line, with a ring around one pond and the sightings recorded near it. Each pond is scored for how likely it is to be occupied."
cover: gis-boundaries.png
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/GCN
aliases:
  - /posts_GCN
  - /posts_GCN.html
---

As a protected species, knowledge of the extent and distribution of habitats of the great crested newt (GCN) is of paramount importance within both the rail and construction sectors. Using data sourced from Network Rail, I apply an adjusted 10-point scale (Oldham et al.) to determine the likelihood of areas being occupied by GCNs — alleviating the need for costly site visits.

![A map of fields and ponds with a railway line running through it; bands either side of the line mark the habitats of interest.](gis-boundaries.png "GIS boundaries of habitats of interest.")

{{< figures >}}
![Box plots of pond area, on a logarithmic scale, for urban, vegetation, woodland and grassland habitats.](habitat-types.png "Spread of habitat types with respective pond areas.")
![Box plots of pond area for bare ground, housing, landfill and quarry.](urban-habitats.png "Types of habitats within the 'Urban' category.")
{{< /figures >}}

## Results

| | Pond count | Inhabited ponds | GCN sightings within 300 m | Share of all GCN recordings |
|---|---:|---:|---:|---:|
| Score < 0.6 | 161 | 0% | 50 | 1% |
| Score ≥ 0.6 | 7863 | 6% | 3031 | 91% |

Ponds were scored with the habitat suitability index of Oldham et al. using the factors that were available: pond area, pond density and terrestrial habitat. Ponds scoring 0.6 or more are deemed suitable for great crested newts; 6% of them have recorded sightings, which make up 91% of all available recordings.

{{< figures >}}
![Two bar charts of feature importance scores; pond area dominates.](regression-tree.png "Regression tree analysis showing feature importance.")
![Confusion matrices for naive Bayes, logistic regression, regression tree, random forest and support vector machine models.](model-results.png "Results of the predictive models.")
{{< /figures >}}
