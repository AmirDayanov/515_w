import os
import flask

app = flask.Flask(__name__)

VIDEOS_DIR = 'static/videos'
PREVIEWS_DIR = 'static/previews'

def extract_video_metadata(filename):
    # Assume that video metadata is stored in the filename as "name_author.mp4"
    # Example: "vacation_john.mp4" would be a video named "vacation" by "john"
    base_name = os.path.splitext(filename)[0]
    parts = base_name.split('_')
    if len(parts) >= 2:
        name = parts[0]
        author_name = parts[1]
    else:
        name = base_name
        author_name = 'Unknown'
    return name, author_name

def get_videos_from_filesystem():
    videos = []
    for filename in os.listdir(VIDEOS_DIR):
        if filename.endswith(('.mp4', '.avi', '.mov')):
            video_id = os.path.splitext(filename)[0]
            preview_path = os.path.join(PREVIEWS_DIR, f"{video_id}.png")
            name, author_name = extract_video_metadata(filename)
            videos.append({
                'id': video_id,
                'filename': filename,
                'preview': preview_path if os.path.exists(preview_path) else None,
                'name': name,
                'author_name': author_name
            })
    return videos

@app.route('/')
def root():
    videos = get_videos_from_filesystem()
    return flask.render_template('index.html', videos=videos)

@app.route('/<video_id>')
def video_page(video_id):
    videos = get_videos_from_filesystem()
    video = next((v for v in videos if v['id'] == video_id), None)

    if video is None:
        return 'Видео не найдено'

    return flask.render_template('video_page.html', video=video)

@app.route('/<video_id>/like', methods=['POST'])
def like_video(video_id):
    # Implement like functionality if needed
    return 'ok'

@app.route('/<video_id>/dislike', methods=['POST'])
def dislike_video(video_id):
    # Implement dislike functionality if needed
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True)