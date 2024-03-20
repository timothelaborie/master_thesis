# bitcointalk_crawler

---

## DataFrame Columns Description

### 1. `start_edit`
- **Description**: This column represents the date when the post or content was initially created.
- **Type**: Date (format: YYYY-MM-DD)
- **Example**: `2013-11-02`

### 2. `last_edit`
- **Description**: This column represents the last date when the post or content was edited.
- **Type**: Date (format: YYYY-MM-DD)
- **Example**: `2013-11-02`

### 3. `author`
- **Description**: The user who created the post.
- **Type**: String
- **Example**: `guyver`

### 4. `post`
- **Description**: The actual content or message of the post.
- **Type**: String
- **Example**: `before we all get excited about the second batch...`

### 5. `topic`
- **Description**: The topic or title of the thread in which the post was made.
- **Type**: String
- **Example**: `[EU/UK GROUP BUY] Blue Fury USB miner 2.2 ...`

### 6. `attachment`
- **Description**:  Indicates whether the post has an attachment or not. A value of `1` means there's an attachment(image or video), and `0` means there isn't. In the website, it using img tag to show the emoji but seems not to be an attachment, such that it also ignring the emojis.
- **Type**: Integer (0 or 1)
- **Example**: `0`
- **Note**: The script 'attachment_fix.py' is run subsequent to the crawling process, as the initial values populated in this column post-crawling are not accurate.

### 7. `link`
- **Description**: Indicates whether the post contains a link or not. A value of `1` means there's a link, and `0` means there isn't.
- **Type**: Integer (0 or 1)
- **Example**: `0`

### 8. `original_info`
- **Description**: This column contains raw HTML or metadata related to the post. It may contain styling and layout information.
- **Type**: String (HTML format)
- **Example**: `<td class="td_headerandpost" height="100%" sty...`

### 9. `preprocessed_post`
- **Description**: Preprocessed of `post` column that for analysis or other tasks.
- **Type**: String
- **Example**: `get excited second batch.let us wait first bat...`

---

## Usage

### 1. `main.py` and `auto_crawl.sh`
- **Description**: The `main.py` script is the full script that is used to crawl the Bitcointalk forum with given the first board page. The `auto_crawl.sh` script is used to automate the process of running the `main.py` script.
- **example**: 
```python 
python main.py 
https://bitcointalk.org/index.php?board=40.0 # board url
--board mining_support # board name
-pages 183 # number of pages in the board
```

### 2. `topic_craawling.py` and `auto_crawl_topic.sh`

- **Description**: The `topic_crawling.py` script is used to crawl exact topic from  Bitcointalk forum with given the first  page url of the topic. The `auto_crawl_topic.sh` script is used to automate the process of running the `topic_craawling.py` script.

- **example**: 
```python
python topic_crawling.py 
https://bitcointalk.org/index.php?topic=168174.0 # topic url
--board miners # board name that topic belongs to
--num_of_pages 165 # total pages of this topic
```
