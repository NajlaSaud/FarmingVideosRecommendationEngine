import pandas as pd


def get_recommendations(id):
    results = pd.read_csv("search_video.csv")

    results_for_video = results[results.video_id == id].search_id.unique()

    relevant_results = results[results.search_id.isin(results_for_video)]

    accompanying_videos_by_search = relevant_results[relevant_results.video_id != id]
    num_instance_by_accompanying_video = accompanying_videos_by_search.groupby("video_id")[
        "video_id"].count().reset_index(name="instances")

    num_results_for_video = results_for_video.size
    video_instances = pd.DataFrame(num_instance_by_accompanying_video)
    video_instances["frequency"] = video_instances["instances"] / num_results_for_video

    recommended_videos = pd.DataFrame(video_instances.sort_values("frequency", ascending=False))

    videos = pd.read_csv("video.csv")
    recommended_videos = pd.merge(recommended_videos, videos, on="video_id")

    # return recommended_products.to_json(orient="table")
    return recommended_videos
