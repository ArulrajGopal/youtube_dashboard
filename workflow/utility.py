from googleapiclient.discovery import build
from Credentials import *

youtube =  build("youtube","v3",developerKey=api_key)



def get_channel_details(channel_id_dict):
  all_data = []
  filtered_data = []
  for i,j in channel_id_dict.items():
    request =youtube.channels().list(part="snippet,contentDetails,statistics", id=j)
    response = request.execute()
    all_data.append(response)
    data = dict(
              Channel_name = response['items'][0]['snippet']['title'],
              Subcribers = response['items'][0]['statistics']['subscriberCount'],
              views = response['items'][0]['statistics']['viewCount'],
              videos = response['items'][0]['statistics']['videoCount'],
              upload_plylst_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
              )
    filtered_data.append(data)

  return filtered_data





def get_videos_list(playlist_id):
  video_id_list = []

  request = youtube.playlistItems().list(part='contentDetails',playlistId = playlist_id)
  response = request.execute()

  for i in range(len(response['items'])):
    video_id_list.append(response['items'][i]['contentDetails']['videoId'])

  next_page_token = response.get('nextPageToken')
  more_pages = True

  while more_pages:
    if next_page_token is None:
      more_pages = False
    else:
        request = youtube.playlistItems().list(part='contentDetails',playlistId = playlist_id,maxResults = 50, pageToken = next_page_token)
        response = request.execute()

        for i in range(len(response['items'])):
          video_id_list.append(response['items'][i]['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')

  return video_id_list






def get_video_details(video_id_lst):
  #dislikecount not available in the API
  all_video_stats = []

  for i in range(0, len(video_id_lst), 50):
    request = youtube.videos().list(part="snippet,contentDetails,statistics",id=','.join(video_id_lst[i:i+50]))
    response = request.execute()

    for video in response['items']:
      try:
        video_stats = dict(
                        Title = video['snippet']['title'],
                        Published_date = video['snippet']['publishedAt'],
                        Views = video['statistics']['viewCount'],
                        Likes = video['statistics']['likeCount'],
                        Comments = video['statistics']['commentCount'],
                        Duration = video['contentDetails']['duration'])
        all_video_stats.append(video_stats)
      except KeyError:
        video_stats = dict(
                        Title = video['snippet']['title'],
                        Published_date = video['snippet']['publishedAt'],
                        Views = video['statistics']['viewCount'],
                        Likes = video['statistics']['likeCount'],
                        Comments = '0',
                        Duration = video['contentDetails']['duration'])
        all_video_stats.append(video_stats)

  return all_video_stats






def get_popular_comments(video_id):
  popular_comments_lst = []

  request = youtube.commentThreads().list(part="snippet,replies", maxResults=100,order="relevance",videoId=video_id)
  response = request.execute()

  for video in response['items']:
      video_stats = dict(
                      VideoId = video['snippet']['videoId'],
                      Author = video['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                      Comment = video['snippet']['topLevelComment']['snippet']['textDisplay'],
                      CommentId = video['snippet']['topLevelComment']['id'],
                      CommentLike = video['snippet']['topLevelComment']['snippet']['likeCount'],
                      Replies = video['snippet']['totalReplyCount'],
                      PublishedAt = video['snippet']['topLevelComment']['snippet']['publishedAt'],
                      UpdatedAt = video['snippet']['topLevelComment']['snippet']['updatedAt']
                      )
      popular_comments_lst.append(video_stats)

  return popular_comments_lst