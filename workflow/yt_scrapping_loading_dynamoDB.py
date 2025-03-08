import json
from integrate_utils import *
from utility import *
from YTChannelConfig import *



channel_details_lst = get_channel_details(channel_id_dict)

for json in channel_details_lst:
    load_dyanmo_db("channel_details_tbl","channel_id",json)

for channel in channel_details_lst:
    channel_id = channel["channel_id"]
    ply_lst_id = channel["upload_plylst_id"]

    video_id_lst= get_videos_list(ply_lst_id)
    video_details_lst = get_video_details(video_id_lst)


    for json in video_details_lst:
        json["channel_id"] = channel_id
        json["playlist_id"] = ply_lst_id

        load_dyanmo_db("video_details_tbl","video_id",json)

