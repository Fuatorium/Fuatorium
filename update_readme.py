import feedparser
import requests
from PIL import Image
from io import BytesIO

# Medium kullanıcı adı
medium_username = "fuatdemirkolll"
rss_feed_url = f"https://medium.com/feed/@{medium_username}"

# RSS feed'i çek
feed = feedparser.parse(rss_feed_url)

# Son 4 yazıyı al
latest_posts = feed.entries[:4]

# README içeriğini oluştur
readme_content = """
# My Recent Medium Articles

"""

for post in latest_posts:
    title = post.title
    link = post.link
    # Medium makalelerinin kapak fotoğraflarını çekmek için tahmini bir URL oluştur
    image_url = post.media_content[0]['url'] if 'media_content' in post and post.media_content else "https://via.placeholder.com/150"
    
    response = requests.get(image_url)
    if response.headers['Content-Type'].startswith('image'):
        image = Image.open(BytesIO(response.content))
        image.save(f"{post.id}.png")  # Resmi kaydet

        # README içeriğine ekle
        readme_content += f"![{title}]({post.id}.png)\n\n"
    else:
        readme_content += f"[{title}]({link})\n\n"

# README dosyasını güncelle
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)
