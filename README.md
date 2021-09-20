# MVPA analysis of the sparse-dense Experiment.

This repository contains scripts for the analysis of behavioral part of the fMRI data using R [[1]](#1), 
scripts for GLM based Beta-Series least-squares-separate (LSS) estimation [[2]](#2) and scripts for a whole-brain 
searchlight [[3]](#3) analysis using a support-vector-classifier implemented in Nilearn [[4]](#4).

GLM and MVPA analysis use HTCondor .submit files for parallel computing on a HPC.

## References
<a id="1">[1]</a> 
Singmann, H., & Kellen, D. (2019).
An introduction to mixed models for experimental psychology. 
In New methods in cognitive psychology (pp. 4-31). Routledge.

<a id="2">[2]</a> 
Mumford, J. A., Turner, B. O., Ashby, F. G., & Poldrack, R. A. (2012). 
Deconvolving BOLD activation in event-related designs for multivoxel pattern classification analyses. 
Neuroimage, 59(3), 2636-2643.

<a id="3">[3]</a> 
Kriegeskorte, N., Goebel, R., & Bandettini, P. (2006). 
Information-based functional brain mapping. 
Proceedings of the National Academy of Sciences, 103(10), 3863-3868.

<a id="4">[4]</a> 
Abraham, A., Pedregosa, F., Eickenberg, M., Gervais, P., Mueller, A., Kossaifi, J., ... & Varoquaux, G. (2014). 
Machine learning for neuroimaging with scikit-learn. 
Frontiers in neuroinformatics, 8, 14.
