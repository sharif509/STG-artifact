## Data Collection
After extracting the sustainability-related software metrics from the paper synthesis, we investigated public GitHub research software repositories. 

 ### Project Selection
DOE-sponsored CASS organization fosters collaboration among diverse Software Stewardship Organizations (SSOs), each responsible for advancing parts of the scientific software ecosystem (e.g., math libraries, data tools, performance tools, etc.). 
We explored the DOE-sponsored Software Stewardship Organizations (SSOs) and randomly selected 10 projects that are open and active on GitHub. 
In the process of project selection, 
Here, we excluded the projects that are mirrored on GitHub from social coding or other platforms because the mirrored repositories entirely or partially lack many of the GitHub-provided metrics like issues and pull requests (PRs). 

In our paper, we anonymized the project names to avoid bias, endorsement, and criticism that may impact their reputations.

### Data Mining
The software metrics shown in TABLE 1 (in paper) are grouped into the two leading factors  
- 🧑‍🤝‍🧑  community engagement and
- ✨  software quality.

They are also highlighted as primary or secondary metrics.
The metrics data directly available or computable from the GitHub REST API responses or PyDriller are named `primary metrics' in our paper.
The process of collecting primary metrics data is detailed in the steps below.

- We collected the GitHub issues, PRs, issue comments, and review comments data using GitHub APIs. 
- We chose PyDriller to mine commits instead of GitHub REST APIs due to API usage restrictions and the enormous amount of commits data. 
By cloning the selected GitHub projects, we were able to use PyDriller to mine the commit messages, code patches, and other metrics. 
- We proceeded to gather the GitHub user profile data for developers involved in our selected projects. Our hope was to establish a link between the mined commit data and the user profile data from GitHub, but we were unable to do so. Unfortunately however, the primary data obtained for commits did not have consistent GitHub usernames or email IDs, and the GitHub user profile data contains only the current email ID for each developer. 

- We processed the mined primary data and obtained secondary metrics data as described in Section~\ref{meth_dataprocess}.



## Data Processing

After collecting the primary metrics data, we computed most secondary metrics data using existing tools and artifacts from other research.
We detail the methods to compute the secondary metrics that required additional computations.

### Repository Metrics
We obtained primary metrics data directly from the data mined in Section~\ref{meth_data_collection}.
These included an aggregated enumeration of issues, PRs, issue comments, pull request comments, commits, labels, new labels, emoji reactions on issue/PR, and commits authored.    
We also enumerated the PRs with merged, closed, or open and issues with open or closed sub-categories. 
Since the calendar month is more studied than the week, quarter, or year, we used only the month for the aggregation period.
TABLE~\ref{tbl_metrics} shows these metric names preceded with `#`.

Included among categorical metrics are **affiliation, user type,**  and **association**. 
We found that the user types contained **USER, ADMIN, BOT,** etc., and association consisted of **CONTRIBUTOR, MEMBER,** and **NONE**.
For the company domination factor, we considered the domain part of the commit-authors' email ID. 
We could not use the GitHub usernames and mine their profiles because many of the commit authors do not provide this information.  
We describe the **gender** and **location** categorical metrics in the following subsections.



### Temporal Metrics
The GitHub REST API provideed time information on PRs, issue, commit, and comment creation;  PR, issue, commit, and comment modification;  PR and issue closure; and PR merge. 
We converted all of the times into UTC zones.
For the issue and PR response time calculation,  we ignored self-comments as a response. In particular, we considered the length of time between an issue reporter, PR submitter's report or submission, and the comment reply by another developer. 
For closed PR/issue enumeration, we selected the calendar month from the GitHub **closed at** timestamp values. 
For PR and issue closure duration metrics, we subtracted the creation timestamp from the closure timestamp.

### Model-computed Metrics
To evaluate the sentiment, usefulness, toxicity, and readability of PRs and issue comments, we selected a state-of-the-art sentiment analyzer, useful/not-useful predictor, toxicity detector, and readability tool  respectively. 
We measured the maintainability of these projects using PyDriller over the mined commits, which provided scores for delta-maintainability-model's (dmm) cyclomatic complexity, unit interfacing, and method size. These scores range from 0 to 1.

### Approximated Metrics
GitHub user profiles do not have specific attributes for the developer's gender, but gender diversity has been studied and found to be an important metric for community engagement and software sustainability. 
We employed an open-source gender-guessing technique (https://pypi.org/project/gender-guesser) that is able to predict gender nearly 98\% of the time correctly[1]. 
The tool is able to predict a person's gender from their name using the categories **male, mostly male, female, mostly female, androgynous,** or **unknown**. 
After determining the guessed gender, we transformed ``mostly male" and ``mostly female" into male and female respectively, and unpredicted genders into the ``unknown" category. 

### Normalized Metrics
We observed the GitHub users' location data and found that a specific location had multiple values for example `US`, `USA`, `U.S.`, or `United States`. 
Additionally, some GitHub users shared city names without their country names, for example, `London` instead of `London, United Kingdom.`  
To unify the geo-location of the developers, we used GeoPy, an open-source geocoding python client, to obtain a full address from OpenStreetMap Nominatim geocoder.
Lastly, for maximum coverage, we took only the country name from the obtained address as location data for every developer who publicly shared their location information at the time of our GitHub data mining.

### Diversity Metrics 
TABLE I in our paper shows that **affiliation, user type, association, gender,** and **location** secondary metrics are related to measuring diversity.
We opted for Shannon's Diversity Index to calculate the diversity of given software metrics categorical values:

$H' = -\sum_{i=1}^{R} p_i \ln(p_i)$

Here, $p_i$ is the proportion of belonging to the $i^{th}$ category. 


## REFERENCES

1. L. Santamar´ıa and H. Mihaljevi´c, “Comparison and benchmark of name-
to-gender inference services,” PeerJ Computer Science, vol. 4, p. e156,
2018