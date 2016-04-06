# Insight-Challenge

#Author:
Erica Cunqian Li / cli12@illinois.edu

#License:
Please see LICENSE file

#Dependencies:
Ubuntu 14.04.3 LTS (any recent version should work)
Python > 2.7.6 (not tested on python 3)
Python modules:
sys,json,numpy,time,igraph,itertools,matplotlib

It is recomened you get the latest versions of each module (as of 4/4/2016) using pip

#Comments:
The Hash_Tag_Graph class has a draw_graph method that will display and save a .png image. This was implemented to allow visualization of the graph and to help with debugging. draw.sh operates the same way as run.sh but will draw the graph using a Kamada & Kawai force directed layout. code was developed for and tested with ubuntu 14.04.3 LTS

I used the igraph module becuase it supports a lot of graph operations. The challenge only requested the mean degree, so I could have gotten away using some lower level data structures but in a real application, we would want more than just the average degree. Igraph supports many other graph operations so I think its a good tradeoff. 

