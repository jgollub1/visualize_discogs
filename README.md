# visualize_discogs
Due to the record industry's eclectic nature, there still exists no central listing of all albums ever published. If you search for a particular artist's discography on cduniverse, discogs, gracenote, etc, you may find that no single source lists every recording by that musician (for example, try searching 'Kurt Rosenwinkel' on the above sources). However, Discogs has come pretty close, boasting over 8 million releases in its database. With plenty of information stored with each listed release, we can use the Discogs API to scrape relevant information about a particular artist's recording history.

For many of us, our relationship with a single artist serves as a starting point for many others. Over the past few years , I have discovered many of my favorite musicians via albums or live recordings with artists I already knew. Who a musician collaborates with also has a huge impact on their artistic vision. For these reasons, knowing an artist's most frequent collaborators is crucial to understanding their background and convenient in expanding our own listening prospects. This project allows us to query Discogs' releases database and visualize an artist's n most frequent collaborators via a node graph, using the open-source packages 'plotly' and 'networkx'. Instructions on running the code can be found in 'instructions.txt'. You may observe interactive visualizations of several artists' discographies via the below demo:

https://jgollub1.github.io/visualize_discogs/

Please provide attribution for any use of this code.

You can reach me at jacobgollub@college.harvard.edu