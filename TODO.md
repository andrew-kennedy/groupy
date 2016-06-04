### Ideas for grouping

###### Note: find some way to specify the amount of rooms and group based on this? for max flexibility

---
* So we first want to take each user and turn them into a node with a name
- Break the nodes into two groups, by gender.
- Proceed to build a bunch of subgraphs using fuzzy string matching. This will incur significant work because we have to check each name against each other name, pretty much no matter what. Whatever is the highest match of a node, if it's above 90% or something, add it as a connected node. 
- After this we should have a list of male graphs, and a list of female graphs.
- go through each graph, identify bridges and assign them a very high weight, and give every other edge the same weight, probably 1.
  - This is to prevent cutting bridges and isolating people from their friend groups. Otherwise bridges would always be the minimum cut.
  - but if cutting a bridge results in 2 (roughly) equal halves ($one\ half = \frac{original\ size}{2}$), we're okay with that
  - we may really need the sparse cut, not minimum cut, but this is NP-hard
- Then perform a mincut on each graph until all subgraphs are of a size $\leq 4$.
- Now we have 2 lists of various subgraphs of friends, all equal to room capacity or less than it.

- ***Time to figure out filling not-yet-filled rooms***

  - Do we just take the greedy route? start with the 3 person rooms and pick individuals until we fill all we can?
  - Some other algorithm?
  - perhaps the knapsack problem could be useful here. We have a capacity and different sized items to choose from (items being the groups of friends)
  - greedy probably easiest.
  - to actually group people, just add one random edge between groups
  - in the end group single people randomly.
  
- This should generate the optimum rooms. Then go through and generate CSV rows from subgraphs.

- Maybe have some way to easily export graphs in case a GUI could be useful

