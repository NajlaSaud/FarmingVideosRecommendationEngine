
# Farming Videos Recommendation Engine

Farming Videos Recommendation Engine is a project done at Farming by Faith Company, South Africa. This project aims to rank videos about farming when the user enter a search word, it returns a list of videos that is most related to the search word. All videos and video data is taken from YouTube, which requires using YouTube Data API. 

The project consists of tow stages:

# Stage 1: Building the database for search and YouTube videos.
The database consists of three tables: VIDEO, SEARCH and SEARCH_VIDEO. The VIDEO tables contains data about YouTube videos, such as title, tags and URL id. The SEARCH table contains a list of all search terms that are used during building the database. Finally, the SEARCH_VIDEO table is an alignment between each search term and its corresponding resulted videos. The codes of creating the database can be found in the file 'DB_Video.py'.

The steps of building this database is as follow:
- First, Start with a search term and Search the YouTube and get a set of results and add the search term to the database.

- Then, Filter this result with a machine learning model that check whether a video is about farming or not. If it is about farming, this video will be added to the database. Otherwise, it will be ignored. All codes and files of the machine learning problem (Classify each video into farming or not farming based on the title of the video) can be found in the folder: Farming Videos Detection. 

- For each video from the search result: Take the title and perform the search again with the title. The same filtering mechanism is applied to the new search results. The machine learning model checks the video before adding it to the database. 

This operation is continuing until the Developer Key for YouTube API Data exceeds the number of requests specified for this key.
The code of building this database can be found in the file 'build_reco_db_iterate_search.py'.

After building the database of farming videos, the data must be converted to csv files to be ready for the next stage, which is building the recommendation engine. The code od converting database tables into csv files can be found in the file 'upload_to_csv.py'.

# Stage 2: Building a recommendation engine based on the search history:
The database is designed in a way that stores every search term aligned with its corresponding video results. Therefore, we can benefit from this search-video alignment in ranking videos. 

The input to the video recommendation engine is a video, and the output is a ranked list of the most related videos. But this is not the ideal solution for our problem as we need the input to be the search term, not the video. 

Therefore, we follow these steps to get a ranked list of related videos:

- First, start with the search term and perform a YouTube search.
- Second, take the first video from the search result and input it to the recommendation engine
- return a ranked list of the most related videos. 

The codes of the recommendation engine can be found in these files: 'main.py' and 'engine.py'

The idea of the recommendation engine is inspired by products recommendation engine in e-commerce websites. When you order a product,  it recommends products that people usually buy with this product. So, the input is a product, and the output is a ranked list of the most related products.
 The same is applied to mimic the YouTube search engine. Where the order in product recommendation engine is the search term in video recommendation engine and the product is the video, accordingly. 
 
(See: https://github.com/scottfitzcodes/rec-engine-example)

## Screenshots
The final result of the project is shown in the following screenshot, where we enter a search word: "Farming in the desert", and as we can see, it returns a list of video URL ids. This list is ranked based on the relatedness of the videos to the search word.


![App Screenshot](https://github.com/NajlaSaud/FarmingVideosRecommendationEngine/blob/master/images/search%20word.png?raw=true)
![App Screenshot](https://github.com/NajlaSaud/FarmingVideosRecommendationEngine/blob/master/images/run%20result.png?raw=true)


# Conclusion
We reach the end of the project. Thanks for your patience. We hope that you benefit from this project.


