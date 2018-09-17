# AppNet
AppNet is a lexical database for Apps.
# crawler
Environment: python3+pymysql.  
To facilitate debugging, delete the foreign key constraint table is created.
# dataset
Use the crawler to get 20,000 app descriptions and comments from the AppStore, and then text processing to get the tag of each app.
# data_preparation
Word segmentation and topic extraction
# build_index
Use the wordnet's inference mechanism to build the index of the tag. This index refers to the association of semantic information including synonymous relations, upper and lower positions, and antisense relationships.
# model
Through the website, you can see the label network. The nodes of this network are tags, and the edges contain the same App. Click on a specific node to see the details of the app that the node contains.
