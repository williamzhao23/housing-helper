"""
Module for downloading Facebook group pages.
"""
from selenium import webdriver
from time import sleep


# Facebook webpage elements may be changed later, so update constants
ID = {'email': 'email', 'pass': 'pass', 'login': 'loginbutton',
      'generic': 'facebook'}
TEXT = {'view': ' more comment', 'one_reply': '1 Reply',
        'mult_reply': ' Replies', 'more_reply': 'View more replies',
        'activity': 'RECENT ACTIVITY', 'new': 'New Posts'}
TEST_USER = ''
TEST_PASS = ''


def initialize_facebook(url: str, username: str, password: str) -> 'WebDriver':
    """
    Returns a Selenium WebDriver after initializing it through Firefox, logging
    in on Facebook with username and password, and heading to url.
    """
    # Log in to Facebook
    browser = webdriver.Firefox()
    browser.get('http://www.facebook.com')
    user = browser.find_element_by_id(ID['email'])
    pass_ = browser.find_element_by_id(ID['pass'])
    user.send_keys(username)
    pass_.send_keys(password)
    browser.find_element_by_id(ID['login']).click()
    # Go to url, click anywhere to remove notification pop-up, then sort by new
    browser.get(url)
    sleep(1)
    browser.find_element_by_id(ID['generic']).click()
    browser.find_element_by_partial_link_text(TEXT['activity']).click()
    browser.find_element_by_partial_link_text(TEXT['new']).click()
    sleep(1)
    return browser


def scroll_through(browser: 'WebDriver', pages: int=10,
                   delay: float=2) -> 'WebDriver':
    """
    Returns a Selenium WebDriver after scrolling through browser and reaching
    the bottom of the continually loading page pages times. Pauses for delay
    seconds before scrolling, so slower browsers should increase delay.
    """
    height = browser.execute_script('return document.body.scrollHeight')
    for _ in range(pages):
        browser.execute_script('window.scrollTo(0, {})'.format(str(height)))
        sleep(delay)
        old_height = height
        height = browser.execute_script('return document.body.scrollHeight')
        if old_height == height:  # End of page reached
            break
    return browser


def view_comments(browser: 'WebDriver') -> 'WebDriver':
    """
    Returns a Selenium WebDriver after clicking all links that reveal more
    comments through browser.
    """
    comment_links = []

    # View all comments to a post
    try:
        links = browser.find_elements_by_partial_link_text(TEXT['view'])
        comment_links += links
    except Exception as e:
        print(e)
    # View singular reply to a comment
    try:
        links = browser.find_elements_by_partial_link_text(TEXT['one_reply'])
        comment_links += links
    except Exception as e:
        print(e)
    # View multiple replies to a comment
    try:
        links = browser.find_elements_by_partial_link_text(TEXT['mult_reply'])
        comment_links += links
    except Exception as e:
        print(e)
    # View unfinished reply chains
    try:
        links = browser.find_elements_by_partial_link_text(TEXT['more_reply'])
        comment_links += links
    except Exception as e:
        print(e)

    # Click on all links
    # Note: Scrolling to end may load more unprocessed comments
    for link in comment_links:
        sleep(0.01)
        link.click()
    return browser


def generate_facebook_html(browser: 'WebDriver') -> None:
    """
    Writes the file, GROUP_PAGE.html, using the browser's webpage.
    """
    text = browser.page_source
    file = open('GROUP_PAGE.html', 'wb')
    file.write(text.encode())


if __name__ == '__main__':
    browser_ = initialize_facebook('https://facebook.com/groups'
                                   + '/370115193161790/', TEST_PASS, TEST_PASS)
    browser_ = scroll_through(browser_, 5)
    browser_ = view_comments(browser_)
    generate_facebook_html(browser_)
    print('All done!')
