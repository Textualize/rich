import requests
from rich.progress import track

chunk_size = 1024
URL = 'http://localhost/file.pdf' # URL of the file to be downloaded

def richDownload(url: str, chunk_size: int):
    """
    A download function with progress bar using the track function (rick.progress.track)
    """
    request = requests.get(url, stream=True)
    total_size = int(request.headers['content-length'])
    
    with open('file.pdf', 'wb') as file:
        for data in track(request.iter_content(chunk_size=chunk_size), description='Downloading...', total=total_size/chunk_size):
            file.write(data)

richDownload(URL, chunk_size)
print("Download complete!!!")