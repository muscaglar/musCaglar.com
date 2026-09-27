---
title: "Exit wave reconstruction of TEM images"
date: 2019-05-01
summary: "Removing lens aberrations from transmission electron microscope images by reconstructing the exit wave from a focal series."
kind: research
tags: [Python, Image processing, Microscopy]
figure: figure.svg
figure_caption: "A focal series of images, taken above, in and below focus, is combined through the inverse of the contrast transfer function. The result is one image in which the atoms are resolved."
cover: focal-series.png
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/HRTEM_Recon
  - name: Paper (Nano Letters)
    url: https://doi.org/10.1021/acs.nanolett.9b03026
aliases:
  - /posts_tem_recon
  - /posts_tem_recon.html
---

Since the majority of my work involves 2D materials, studying the surface morphology and defects within the materials is important. I use Raman spectroscopy to infer some of the properties within the material, such as how many layers I am working with or how many holes or defects the material has, but imaging the surface morphology and defects within the material can be far more useful and convincing.

The highest resolution we can obtain using an optical microscope is around 200 nm; using electrons instead of photons can greatly improve this resolution. With the scanning electron microscopes (SEM) that we have in Cambridge, we can bring this limit closer to 20 nm. An SEM will use, mostly, surface-scattered electrons for detection, but by using electrons that penetrate through the sample, the resolution can be improved further. Transmission electron microscopy (TEM) does just that, and approaches resolutions close to 0.5 nm. This resolution is predominantly hampered by aberrations within the microscope lenses. If these aberrations are corrected for, the theoretical information limit from TEM approaches 42 pm (0.04 nm).

With knowledge of the microscope imaging conditions and the aberration factors, the contrast transfer function (CTF) can be found. This function describes the degrading factors imposed on the final image seen. By applying the inverse of this function to the image, we can get back the 'true', aberration-corrected image. Therefore, the more accurate the CTF, the better the resolution of the image which can be reconstructed.

![A stack of TEM images taken above, in and below focus is combined through the inverse contrast transfer function into a single reconstructed image.](focal-series.png "A focal series — images taken above, in and below focus — is combined through the inverse CTF.")

The CTF is obtained iteratively and requires a focal series of images, since the function is sensitive to phase.

![Reconstructed TEM images of an atomic lattice with holes outlined in red; the two outlined holes measure about 9 and 8 square nanometres.](reconstructed.png "Exit wave reconstructed images.")

## Reference

Caglar, M., Pandya, R., Xiao, J., Foster, S., Divitini, G., Chen, R., Greenham, N., Franze, K., Rao, A. and Keyser, U. All-Optical Detection of Neuronal Membrane Depolarization in Live Cells Using Colloidal Quantum Dots. *Nano Letters*. [doi:10.1021/acs.nanolett.9b03026](https://doi.org/10.1021/acs.nanolett.9b03026)
