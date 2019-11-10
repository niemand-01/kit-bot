#event type

EVENT_USR_1 = 'friend_request'
EVENT_USR_2 = 'want_join_group'
EVENT_USR_3 = 'want_contact_through_serialID'
EVENT_USR_4 = 'robot_info'
EVENT_USR_5 = 'other_functions'


EVENT_GRP_1 = 'auto_share_info'
EVENT_GRP_2 = 'temp_share_info'
EVENT_GRP_3 = 'user_misbehavior'
EVENT_GRP_4 = 'build_small_group' #automated triggered by event_usr_3
EVENT_GRP_5 = 'time_up'# to controll small group time?
EVENT_GRP_6 = 'group_expire' #triggered by event_grp_5 or user word

#specify the share info with offer and beg ==> tobe stored in databank
EVENT_SHARE_1 = 'ZUFANG_OFFER'
EVENT_SHARE_2 = 'ZUFANG_BEG'
EVENT_SHARE_3 = 'ERSHOU_OFFER'
EVENT_SHARE_4 = 'ERSHOU_BEG'

EVENT_SHARE_5 = 'BANGDAI_OFFER'
EVENT_SHARE_6 = 'BANGDAI_BEG'
EVENT_SHARE_7 = 'JIANZHI_OFFER'
EVENT_SHARE_8 = 'JIANZHI_BEG'

EVENT_SHARE = [EVENT_SHARE_1,EVENT_SHARE_2,EVENT_SHARE_3,EVENT_SHARE_4,
               EVENT_SHARE_5,EVENT_SHARE_6,EVENT_SHARE_7,EVENT_SHARE_8]
