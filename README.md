[![Python package](https://github.com/LSARP/ms-conc/actions/workflows/python-package.yml/badge.svg)](https://github.com/LSARP/ms-conc/actions/workflows/python-package.yml)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/LewisResearchGroup/ms-conc.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LewisResearchGroup/ms-conc/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/LewisResearchGroup/ms-conc.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LewisResearchGroup/ms-conc/context:python)

  
This repository contains an app for standardizing metabolomics data by using standard samples that incorporates a novel algorithm for detecting linear ranges in a set of (x,y) points covering several orders of magnitude. The algorithm uses the log-scale to perform a search of the linear range by iteratively fitting a linear curve to the set of points. The points that are further from the fitted curve are removed from the range until reaching a proper fitting. The parameters controlling the goodness of fit and the criteria for stopping the iterative points elimination were selected by using real mass spectrometry generated metabolomics data.

The app was created for mass spectrometry generated data although it can be used in data with similar structure.
The app can work with data generated from Maven or Mint program although that information should be provided.
The app can be used freely online at https://lewisresearchgroup-ms-conc-streamlit-app-w9e64f.streamlit.app/, or locally by cloning this repo. Running localy allows for modifying parameters controlling the algorithm performance to better adjust your data.

# Add here.
- contributors
- link to documentation
- installation instructions
