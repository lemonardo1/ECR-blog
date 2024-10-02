from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import markdown
from pathlib import Path
import re


app = FastAPI()

# Set up static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Path to the folder where Markdown files are stored
POSTS_PATH = Path("data")



def convert_youtube_links(content):
    # Regular expression to find YouTube links in the format [YouTube 링크](...)
    youtube_regex = r'\[YouTube 링크\]\((https://www\.youtube\.com/watch\?[\w=&;-]+)\)'
    
    # Replace YouTube links with iframe embed code
    def embed_youtube(match):
        url = match.group(1)
        query_string = url.split('watch?')[-1]  # Get everything after 'watch?'
        return f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{query_string}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
    
    # Substitute YouTube links with embed code
    return re.sub(youtube_regex, embed_youtube, content)


# Modify the get_blog_posts function
def get_blog_posts():
    posts = []
    for markdown_file in POSTS_PATH.glob("**/*.md"):  # Recursive search
        # Extract post id from folder structure and filename
        relative_path = markdown_file.relative_to(POSTS_PATH)
        post_id = str(relative_path).replace("/", "_")  # Keep dots in the filename intact
        title = markdown_file.stem.replace("-", " ").title()
        folder = str(relative_path.parent) if relative_path.parent != Path() else None
        
        posts.append({
            "id": post_id, 
            "title": title,
            "folder": folder  # Add folder info for grouping in the list
        })
    return posts

# Read the content of a specific Markdown file
def get_post_content(post_id):
    # Reconstruct the path while keeping dots in filenames
    post_path = POSTS_PATH / post_id.replace("_", "/")  # Reconstruct path
    post_path = post_path.with_suffix(".md")  # Ensure it has the .md suffix
    
    if post_path.exists():
        with open(post_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Pre-process content to convert YouTube links before passing to markdown parser
            if "youtube" in str(post_path):  # Only for files in the youtube folder
                content = convert_youtube_links(content)
            html_content = markdown.markdown(content)
            return html_content
    return None

@app.get("/")
def read_blog(request: Request):
    posts = get_blog_posts()
    # Group posts by folders
    grouped_posts = {}
    for post in posts:
        folder = post["folder"] or "Root"  # Group posts in "Root" if no folder
        if folder not in grouped_posts:
            grouped_posts[folder] = []
        grouped_posts[folder].append(post)
    
    return templates.TemplateResponse("index.html", {"request": request, "grouped_posts": grouped_posts})


# 게시글을 읽는 엔드포인트
@app.get("/post/{post_id}")
def read_post(request: Request, post_id: str):
    post_content = get_post_content(post_id)
    if post_content is None:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    
    title = post_id.split("_")[-1].replace("-", " ").title()
    
    # 폴더가 'CPX'인지 확인
    folder = post_id.split("_")[0]  # 경로의 첫 번째 부분을 폴더로 가정
    is_cpx = folder == "CPX"
    
    # YouTube 링크를 iframe으로 변환
    post_content = convert_youtube_links(post_content)
    
    return templates.TemplateResponse("post.html", {"request": request, "post_content": post_content, "title": title, "is_cpx": is_cpx})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
