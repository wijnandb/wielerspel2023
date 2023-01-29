---
title: Generate site straight from Github
author: Wijnand
---

This site is a Jekyll site, running on Github.
The content is taken (mostly) from CSV files, containing information about UCI cyclists and their results, combined with the points they earn for their virtual teamcaptains, resulting in a ranking of those teamcaptains.

The content of the CSV files is generated through the scraping of site(s) containing the results of UCI races. 
The process of scraping is initiated and run from my local computer, as is the processing of those results (adding points to results, adding points to riders, adding up points per teamcaptain, generating a ranking). The obtained results are then (automatically) pushed to Github, where the Jekyll pages are (automatically) generated. 

What we want, is that the process of scraping and the processing of points, are run via Github workflows.

How do we do that?

First, we create a new branch on which we can run the workflow.

