# Instagram Scrapper

This is a tool I vibe coded to scrape information from a series of Instagram posts for a Marketing MBA student, enabling them to analyze the data for their thesis.

## Usage

1.  **Launch Chrome with Remote Debugging:** Start Chrome with remote debugging enabled.

* "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222

2.  **Log in to Instagram:** In the Chrome window, log in to your Instagram account.

3.  **Edit Post URLs:**  Modify the `post_urls` list in the `main()` function to include the URLs of the Instagram posts you want to scrape.

4.  **Run the Script:** Execute the script. It will connect to your Chrome session, scrape the data, and save it to `instagram_posts.csv`.

The `instagram_posts.csv` file will contain the following columns:

*   `name` (Instagram username)
*   `likes` (number of likes)
*   `comments` (number of comments)
*   `caption` (post caption)
*   `post_date` (when the post was published)
*   `scrape_date` (when the data was scraped)

This approach leverages an existing browser session to bypass Instagram's login requirements and handles various like/comment count formats (e.g., "744K").

```
This approach leverages an existing browser session to bypass Instagram's login requirements and handles various like/comment count formats (e.g., "744K").

**Note:** This code was written and used on 21/04/2025. It will probably break soon.
```
