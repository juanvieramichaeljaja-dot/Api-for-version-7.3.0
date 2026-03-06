from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# -----------------------------
# RECURSOS Y CONSTANTES
# -----------------------------
BASE_URL = "http://127.0.0.1:5000"
VIDEO_URL_TEMPLATE = "http://127.0.0.1:5000/static/v{vid}.mp4"
THUMB_URL = "http://127.0.0.1:5000/static/thumb.jpg"
VIDEO_THUMB_URL = "http://127.0.0.1:5000/static/thumbvideo.jpg"
MUSIC_MP3_LIBRARY = "http://127.0.0.1:5000/static/sound.mp3"
UID = "12"
TOTAL_AWEMES = 29

VIDEO_TITLES = [
    "Hold on😡!@jennaortega #2016 #old","Welcome to Hell",
    "Duet with @arianagrande#2016 #old","Hi Beach","DAB😎",
    "Yeah yeah Yeah 😎","Dollar me 😎","Snapchat?😜",
    "Sad girllll😭","To myself 😗","","😜","And you are",
    "Hey hey hey hey😆","Sorry 😭 #justin biber","i wish x x x x",
    "","Love me ❤️","","Its you😣? #transitions",
    "I need you love ☹️","🔫","@milliebobbybrown","Flower😉",
    "Leg out","Nah nah nah😄","Hola como esta?",
    "duet with @arianagrande","mama mia ma ma mia😁#family"
]

# -----------------------------
# GENERADOR DE VIDEOS
# -----------------------------
def generate_aweme_list(count=TOTAL_AWEMES, start_id=10000):
    aweme_list = []
    for i in range(count):
        vid = i + 1
        aweme_list.append({
            "aweme_id": str(start_id + i),
            "desc": VIDEO_TITLES,
            "create_time": int(time.time()),
            "author_user_id": UID,
            "author": {
                "uid": UID,
                "unique_id": "musica.ly.old.2014",
                "nickname": "musical.ly back🔥",
                "avatar_thumb": {"url_list": ["http://127.0.0.1:5000/static/thumb.jpg"]},
                "verified": True,
                "reviewed": True,
                "custom_verify": 1,
            },
            "statistics": {
                "digg_count": 12,
                "comment_count": 20,
                "share_count": 12,
                "play_count": 100
            },
            "video": {
                "play_addr": {
                    "uri": f"v{vid}.mp4",
                    "url_list": [f"{BASE_URL}/static/v{vid}.mp4"]
                },
                "cover": {"url_list": ["http://127.0.0.1:5000/static/thumbvideo.jpg"]},
                "duration": 15500,
                "status": 1,
            }
        })
    return aweme_list

# -----------------------------
# LOGIN
# -----------------------------
@app.route("/passport/user/login/", methods=["POST", "GET"])
def login():
    password = request.values.get("password")
    if password != "juan123":
        return jsonify({"status_code": 1, "message": "Incorrect password"})
    return jsonify({
        "status_code": 0,
        "user_id": UID,
        "session_key": "juan_session_spot_ly"
    })

# -----------------------------
# FEED
# -----------------------------
@app.route("/aweme/v1/feed/")
@app.route("/aweme/v1/fresh/feed/")
def feed():
    return jsonify({
        "status_code": 0,
        "aweme_list": generate_aweme_list(),
        "cursor": 0,
        "has_more": 0
    })

# -----------------------------
# USER
# -----------------------------
@app.route("/aweme/v1/user/")
def user_endpoint():
    return jsonify({
        "status_code": 0,
        "user": {
            "uid": UID,
            "unique_id": "musica.ly.old.2014",
            "nickname": "musical.ly back🔥",
            "aweme_count": TOTAL_AWEMES,
            "avatar_larger": {
                "url_list": ["http://127.0.0.1:5000/static/thumb.jpg"]
            },
            "verified": True,
            "reviewed": True,
            "custom_verify": 1,
            "following_count": 150,
            "follower_count": 2000000,        # 2 millones
            "total_favorited": 15000000, 

        }
    })

@app.route("/aweme/v1/aweme/post/")
def user_posts():
    return jsonify({
        "status_code": 0,
        "aweme_list": generate_aweme_list(),
        "cursor": 0,
        "has_more": 0
    })

# -----------------------------
# CHALLENGES
# -----------------------------
@app.route("/aweme/v1/challenge/search/")
def challenge_search():
    keyword = request.args.get("keyword", "")
    return jsonify({
        "status_code": 0,
        "challenge_list": [
            {
                "cid": "1",
                "cha_name": f"{keyword} 1",
                "desc": "Demo challenge",
                "video_count": 10,
                "cover": {"url_list": ["http://127.0.0.1:5000/static/thumbvideo.jpg"]}
            }
        ]
    })

# -----------------------------
# DISCOVER
# -----------------------------
@app.route("/aweme/v1/find/")
def fetch_banners():
    return jsonify({
        "status_code": 0,
        "items": [
            {"banner_id": "1", "title": "Banner 1", "image_url": "http://127.0.0.1:5000/static/thumb.jpg"},
            {"banner_id": "2", "title": "Banner 2", "image_url": "http://127.0.0.1:5000/static/thumb.jpg"}
        ]
    })
@app.route("/effect/api/v3/effect/my", methods=["GET"])
def get_effect_my():
    # Este es el JSON que devolverá el endpoint
    response_json = {
        "access_key": "ABCD1234EFGH5678",
        "device_id": "device-9876543210",
        "device_type": "Samsung",
        "device_platform": "android",
        "region": "UY",
        "sdk_version": "2.4.3",
        "app_version": "7.5.0",
        "channel": "googleplay",
        "panel": "default"
    }

    # Opcional: puedes usar request.args si quieres recibir parámetros GET
    # por ejemplo: ?device_id=otro_id
    for key in response_json.keys():
        if key in request.args:
            response_json[key] = request.args[key]

    return jsonify(response_json)
@app.route("/aweme/v1/music/create", methods=["POST"])
def create_music():
    data = request.json
    payload = {
        "song_id": data.get("song_id"),
        "source_platform": str(data.get("source_platform", 0)),
        "duration": str(data.get("duration", 0)),
        "is_collect": str(data.get("is_collect", 0)),
    }
    optional_fields = ["title", "author", "album", "cover_url", "all_rate", "pic_small"]
    for field in optional_fields:
        if data.get(field):
            payload[field] = data[field]

    url = BASE_URL + "music/create/"
    try:
        resp = requests.post(url, data=payload)
        resp.raise_for_status()
        result = resp.json()
        return jsonify({"song_id": data.get("song_id"), "mid": result.get("mid", "")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------
# Listas de música
# ----------------------
@app.route("/aweme/v1/music/collection", methods=["GET"])
def fetch_music_collection():
    cursor = request.args.get("cursor", 0)
    count = request.args.get("count", 20)
    url = BASE_URL + "music/collection/"
    resp = requests.get(url, params={"cursor": cursor, "count": count})
    return jsonify(resp.json())

@app.route("/aweme/v1/music/hot", methods=["GET"])
def fetch_music_hot_list():
    cursor = request.args.get("cursor", 0)
    count = request.args.get("count", 20)
    timestamp = request.args.get("timestamp", 0)
    url = BASE_URL + "hot/aweme/v1/music/"
    resp = requests.get(url, params={"cursor": timestamp, "count": count})
    return jsonify(resp.json())

@app.route("/aweme/v1/music/list", methods=["GET"])
def fetch_music_list():
    mc_id = request.args.get("mc_id")
    cursor = request.args.get("cursor", 0)
    count = request.args.get("count", 20)
    url = BASE_URL + "music/list/"
    resp = requests.get(url, params={"mc_id": mc_id, "cursor": cursor, "count": count})
    return jsonify(resp.json())

@app.route("/aweme/v1/music/original", methods=["GET"])
def fetch_original_music_list():
    user_id = request.args.get("user_id")
    cursor = request.args.get("cursor", 0)
    count = request.args.get("count", 20)
    url = BASE_URL + "original/aweme/v1/music/list/"
    resp = requests.get(url, params={"user_id": user_id, "cursor": cursor, "count": count})
    return jsonify(resp.json())

# ----------------------
# Comprobaciones de colección
# ----------------------
@app.route("/aweme/v1/music/check_collect", methods=["GET"])
def fetch_user_collected_baidu_music():
    music_ids = request.args.get("music_ids")
    url = BASE_URL + "music/check/collect/"
    resp = requests.get(url, params={"music_ids": music_ids})
    return jsonify(resp.json())

@app.route("/aweme/v1/music/user_collect", methods=["GET"])
def fetch_user_collected_music_list():
    cursor = request.args.get("cursor", 0)
    count = request.args.get("count", 20)
    url = BASE_URL + "user/aweme/v1/music/collect/"
    resp = requests.get(url, params={"cursor": cursor, "count": count})
    return jsonify(resp.json())

@app.route("/aweme/v1/music/collect", methods=["GET"])
def on_user_collect_music():
    music_id = request.args.get("music_id")
    collect_type = request.args.get("type", 0)
    url = BASE_URL + "music/collect/"
    requests.get(url, params={"music_id": music_id, "type": collect_type})
    return jsonify({"music_id": music_id, "type": collect_type})

# ----------------------
# Detalles y videos por música
# ----------------------
@app.route("/aweme/v1/music/detail", methods=["GET"])
def query_music():
    music_id = request.args.get("music_id")
    click_reason = request.args.get("click_reason", 0)
    url = BASE_URL + "music/detail/"
    resp = requests.get(url, params={"music_id": music_id, "click_reason": click_reason})
    return jsonify(resp.json())
@app.route("/aweme/v1/comment/delete/", methods=["POST"])
def delete_comment():
    cid = request.form.get("cid")
    return jsonify({"cid": cid})

# DIGG COMMENT
@app.route("/aweme/v1/comment/digg/", methods=["POST"])
def digg_comment():
    return jsonify({
        "cid": request.form.get("cid"),
        "aweme_id": request.form.get("aweme_id"),
        "digg_type": request.form.get("digg_type")
    })

# FETCH COMMENT LIST
@app.route("/aweme/v1/comment/list/", methods=["GET"])
def fetch_comment_list():
    return jsonify({
        "aweme_id": request.args.get("aweme_id"),
        "cursor": request.args.get("cursor"),
        "count": request.args.get("count"),
        "comment_style": request.args.get("comment_style"),
        "digged_cid": request.args.get("digged_cid"),
        "insert_cids": request.args.get("insert_cids")
    })

# FETCH STORY REPLY COMMENT LIST
@app.route("/aweme/v1/comment/story/replylist/", methods=["GET"])
def fetch_story_reply_comment_list():
    return jsonify({
        "comment_id": request.args.get("comment_id")
    })

# PUBLISH COMMENT
@app.route("/aweme/v1/comment/publish/", methods=["POST"])
def publish_comment():
    return jsonify({
        "aweme_id": request.form.get("aweme_id"),
        "text": request.form.get("text"),
        "reply_id": request.form.get("reply_id"),
        "text_extra": request.form.get("text_extra"),
        "is_self_see": request.form.get("is_self_see")
    })
@app.route("/aweme/v1/music/aweme", methods=["GET"])
def query_music_aweme_list():
    music_id = request.args.get("music_id")
    cursor = int(request.args.get("cursor", 0))
    timestamp = int(request.args.get("timestamp", 0))
    count = int(request.args.get("count", 20))
    fresh = request.args.get("fresh", "0") == "1"

    if fresh:
        url = BASE_URL + "music/fresh/aweme/"
    else:
        url = BASE_URL + "music/aweme/"

    params = {
        "music_id": music_id,
        "cursor": timestamp,
        "count": count,
        "type": 6
    }
    resp = requests.get(url, params=params)
    return jsonify(resp.json())
@app.route("/aweme/v1/category/list/", methods=["GET"])
def challenge_recommend():
    hashtags = [
        "musically", "foryou", "fyp", "duet", "funny", "love", "dance", "cute",
        "sing", "friends", "like4like", "followme", "happy", "fun", "smile",
        "muser", "challenge", "viral", "trend", "cool"
    ]

    category_list = []

    for i, tag in enumerate(hashtags):
        category_list.append({
            "aweme_list": [
                {
                    "aweme_id": str(i+1),
                    "aweme_type": 0,
                    "create_time": int(time.time()) - i*1000,
                    "desc": f"#{tag} challenge",
                    "is_pgcshow": False,
                    "status": {
                        "allow_comment": True,
                        "allow_share": True,
                        "download_status": 0,
                        "is_delete": False,
                        "is_private": False,
                        "with_goods": False
                    },
                    "video": {
                        "play_addr": {
                            "uri": f"v{i+1}.mp4",
                            "url_list": [f"http://127.0.0.1:5000/static/v{i+1}.mp4"]
                        },
                        "cover": {"url_list": ["http://127.0.0.1:5000/static/thumbvideo.jpg"]},
                        "height": 1920,
                        "width": 1080
                    }
                }
            ],
            "category_type": 0,
            "challenge_info": {
                "author": {},
                "cha_name": f"#{tag}",
                "cid": str(i+1),
                "desc": f"Trending #{tag} challenge",
                "is_pgcshow": False,
                "schema": f"aweme://aweme/challenge/detail?cid={i+1}",
                "type": 0,
                "user_count": 0
            },
            "desc": f"Trending #{tag}"
        })

    response = {
        "extra": {"now": int(time.time())},
        "category_list": category_list,
        "cursor": len(hashtags),
        "has_more": 0,
        "status_code": 0
    }

    return jsonify(response)

# -----------------------------
# RECOMMEND
@app.route("/aweme/v1/user/recommend/")
def user_recommend():
    return jsonify({
        "status_code": 0,
        "type": 1,
        "aweme_list": generate_aweme_list(),
        "cursor": 0,
        "has_more": 0
    })
@app.route("/aweme/v1/thrid/platform/share/", methods=["POST"])
def share_video():
    data = request.json

    # Campos que se mencionan en autoShare
    platform_type = data.get("platform_type")
    share_url = data.get("share_url")
    share_message = data.get("share_message")
    fb_access_token = data.get("fb_access_token")
    twitter_access_token = data.get("twitter_access_token")
    access_token_secret = data.get("access_token_secret")
    youtube_code = data.get("youtube_code")
    item_id = data.get("item_id")
    youtube_title = data.get("youtube_title")
    youtube_desc = data.get("youtube_desc")

    # Respuesta simulada
    return jsonify({
        "platform_type": "Facebook",
        "share_url": "https://transactions-control-owen-territories.trycloudflare.com/v1.mp4",
        "share_message": "hi",
        "fb_access_token": "FACEBOOKTOKEN=126EVEB282JENE",
        "twitter_access_token": "TWITTERSESSIONID=1827241HSMLADHW",
        "access_token_secret": "ACCESSTOKEN=1827MLMLGQGWVW",
        "youtube_code": "12",
        "item_id": "1",
        "youtube_title": "HITEST",
        "youtube_desc": "HI",
        "status": "ok",
        "message": "Video shared successfully"
    })
@app.route("/aweme/v1/aweme/modify/visibility/", methods=["POST"])
def modify_visibility():
    data = request.json

    aweme_id = data.get("aweme_id")
    visibility_type = data.get("type")  # 0 = privado, 1 = público, etc.

    # Respuesta simulada siguiendo la clase PrivateUrlModel
    return jsonify({
        "aweme_id": f"http://127.0.0.1:5000/v{i+1}",
        "type": 1,
    })
@app.route("/aweme/v1/aweme/stats/", methods=["POST"])
def aweme_stats():
    return jsonify({
        "app_language": "es",
        "manifest_version_code": "2018053001",
        "_rticket": "1772586578750",
        "channel": "googleplay",
        "language": "es",
        "fp": "",
        "device_type": "SM-A035M",
        "resolution": "720*1527",
        "openudid": "4f58dc6d30375814",
        "update_version_code": "2018053001",
        "sys_region": "US",
        "os_api": "33",
        "is_my_cn": "0",
        "timezone_name": "America/Montevideo",
        "dpi": "300",
        "carrier_region": "UY",
        "ac": "wifi",
        "mcc_mnc": "74807",
        "timezone_offset": "-10800",
        "os_version": "13",
        "version_code": "730",
        "app_name": "musical_ly",
        "version_name": "7.3.0",
        "device_brand": "samsung",
        "ssmix": "a",
        "build_number": "7.3.0",
        "device_platform": "android",
        "region": "ES",
        "aid": "1233",
        "ts": "1772586578",
        "as": "a1d6d8ea8285f976b74355",
        "cp": "855b9460237ea969e1OyWc",
        "mas": "00dc099b1aa8f006de8574e657e09a9bceacaccc2cec466cec9c66"
    })
@app.route("/aweme/v1/recommend/user/dislike/", methods=["POST", "GET"])
def dislike_user():
    return jsonify({"status_code": 0})

# -----------------------------
# CATCH ALL
# -----------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return jsonify({"status_code": 0})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)