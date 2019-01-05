"""
Module for printing filtered housing offers from Facebook.
"""
from typing import List
from bs4 import BeautifulSoup
from post import Post
import page_to_html


# Facebook webpage elements may be changed later, so update constants
POST_CLASS = 'userContentWrapper'


def print_intro() -> None:
    """
    Prints the opening instructions.
    """
    print('--=== Welcome to Housing Helper! ===--')
    print('NOTE: you must be a member of the group you would like to search!')


def float_input(input_: str) -> bool:
    """
    Returns true if and only if the input can be converted to a float or int.
    """
    try:
        float(input_)
        return True
    except ValueError:
        return False


def find_bodies() -> List['Tag']:
    """
    Returns a list of tag objects from GROUP_PAGE.html, each object containing
    a separate post and its comments.
    """
    file = open('GROUP_PAGE.html', 'rb')
    soup = BeautifulSoup(file, 'html.parser')
    return soup.find_all(class_=POST_CLASS)


def create_posts(tags: List['Tag']) -> List[Post]:
    """
    Returns a list of Post objects with Comment objects as attributes, created
    from tags.
    """
    return [Post(tag) for tag in tags]


if __name__ == '__main__':
    print_intro()
    group_url = input('Type the full url of the group you\'d like to search: ')
    username = input('Type your Facebook username: ')
    password = input('Type your Facebook password 🙈: ')
    pages = input('How many pages do you want to search? Default is 10(pp): ')
    while not pages.isnumeric():
        pages = input('Enter a number!: ')
    delay = input('How long do you want the delay? Default is 2(s): ')
    while not float_input(delay):
        delay = input('Enter a number!: ')
    budget = input('What is your budget?: ')
    while not budget.isnumeric():
        budget = input('Enter a number!: ')
    sublet = input('Would you like to sublet? (y/n/idc): ')
    print('Don\'t touch anything!')

    driver = page_to_html.initialize_facebook(group_url, username, password)
    driver = page_to_html.scroll_through(driver, int(pages), float(delay))
    driver = page_to_html.view_comments(driver)
    page_to_html.generate_facebook_html(driver)

    tags = find_bodies()
    posts_ = create_posts(tags)
    # Filters out buyers and "unhelpful" posts
    posts_ = [x for x in posts_ if x.content is not None and x.seller]
    posts_ = [x for x in posts_ if x.in_price_range(int(budget))]
    if sublet.lower() == 'y':
        posts_ = [x for x in posts_ if x.is_sublet()]
    elif sublet.lower() == 'n':
        posts_ = [x for x in posts_ if not x.is_sublet()]

    print('\n\n\n\n')
    for post_ in posts_:
        print(post_)
    print('\n\n\nAll done!')
