import requests

url = "picture url"
file_path = "demo.png"

response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Write the content of the response to a file
    with open(file_path, 'wb') as file:
        file.write(response.content)
    print(f"Image downloaded successfully: {file_path}")
else:
    print(f"Failed to download image. Status code: {response.status_code}")
