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
We call this branch _workflow_.

On this workflow branch, we create a new workflow, called _generate_ranking.yaml_.

Parts of the workflow we need to get working:

1. Run the workflow on a schedule
2. checkout the existing code
3. set up python
4. install dependencies
5. run python file(s)
6. commit changed files

We also want to find out how to create different jobs, that depend on eachother.
If there are no new results to scrape, we want the workflow to stop: there is nothing to do.
 
