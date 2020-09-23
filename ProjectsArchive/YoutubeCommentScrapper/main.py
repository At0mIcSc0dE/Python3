import googleapiclient.discovery
import sys


def main():
    """Main Function"""

    # videoURL = sys.argv[1]
    # videoURL = "https://www.youtube.com/watch?v=NSI4kYIkf80"
    # videoID = videoURL.split("=")[1]
    videoID = "6Dh-RL__uN4"

    apiKey = "<APIKEYHERE>"
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=apiKey)

    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=videoID,
        maxResults=4294967295
    )
    response = request.execute()

    # print(response)
    # print("\n\n\n\n\n\n\n\n")

    for result in range(response["pageInfo"]["totalResults"]):
        print(str(result) + ": " + response["items"][result]["snippet"]
              ["topLevelComment"]["snippet"]["textDisplay"])
        print("\n")

    input()


if __name__ == "__main__":
    main()
