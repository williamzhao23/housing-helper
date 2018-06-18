"""
Module for reading Facebook posts.
"""
from bs4 import BeautifulSoup
from typing import List, Union
from comment import Comment


class Post:
    """
    Essential textual information of a Facebook post, specifically renters.

    comments - comments on post
    author - author of post
    link - permalink of the post
    timestamp - when the post was made
    price - lowest realistic price of the product
    content - the text content of the post
    seller - True if the post is likely a seller
    """
    comments: List[Comment]
    author: str
    link: str
    timestamp: str
    price: Union[int, None]
    content: Union[str, None]
    seller: bool

    # Facebook webpage elements may be changed later, so update constants
    # LOW_PRICE filters noise from other, cheaper items or features
    CLASS = {'time': 'fsm fwn fcg', 't_stamp': 'timestampContent',
             'author': 'fwn fcg', 'comment': 'UFICommentContentBlock',
             'product': '_l52', 'price': '_l57', 'regular': '_5pbx'}
    LOW_PRICE = 300

    def __init__(self, tag: 'Tag') -> None:
        """
        Initialize a new post using a Beautiful Soup tag object.

        Note: currently, the tag should have class userContentWrapper, but any
        encompassing tag that is independent of other posts should work.
        Note: if price/content are None, either they couldn't be found or they
        are not worthwhile and set to None
        """
        # Finding comment tags and creating a list of Comment objects
        comments = tag.find_all(class_=self.CLASS['comment'])
        self.comments = [Comment(x) for x in comments]

        # Finding author name
        # Note: not all have the same class, but all contain href attribute
        # Note: if 'author' class can't be found, it's likely an ad was scraped
        author = tag.find(class_=self.CLASS['author'])
        if author is None or author.find(href=True) is None:
            self.author = '!NOT A USER POST!'
        else:
            self.author = author.find(href=True).getText()

        # Finding permalink and timestamp
        time = tag.find(class_=self.CLASS['time'])
        self.link = 'http://www.facebook.com' + time.a.attrs['href']
        self.timestamp = time.find(class_=self.CLASS['t_stamp']).getText()

        # Finding content from products, then regular posts, and None otherwise
        product = tag.find(class_=self.CLASS['product'])
        post = tag.find(class_=self.CLASS['regular'])
        if product is not None:  # Product found
            price = product.find(class_=self.CLASS['price']).getText()
            # A 'FREE' product is a waste of time and breaks integer comparisons
            if 'free' in price.lower() or product_price(price) < self.LOW_PRICE:
                self.price = self.content = None
                self.seller = True
            else:
                self.price = product_price(price)
                self.content = product.getText()
                self.seller = True
        elif post is not None:  # Regular post found
            lowest = lowest_price(extract_prices(post.getText()))
            if lowest is None:  # Likely not a seller
                self.price = self.content = None
                self.seller = False
            else:
                self.price = lowest
                self.content = post.getText()
                self.seller = self.is_seller()
        else:  # Probably some other format that a seller would not use
            self.price = self.content = None
            self.seller = False

    def __eq__(self, other: 'Post') -> bool:
        """
        Returns True iff self and other are functionally the same posts.
        """
        return (type(self) == type(other) and self.comments == other.comments
                and self.author == other.author and self.link == other.link
                and self.timestamp == other.timestamp
                and self.price == other.price and self.content == other.content
                and self.seller == other.seller)

    def __str__(self) -> str:
        """
        Returns a barebones string representation of self.
        """
        if self.content is None:
            blurb = None
        else:
            blurb_length = min(len(self.content), 180)
            blurb = self.content[:blurb_length]
        return ('${} - {} - {}\n\"{}...\"\n'.format(self.price, self.author,
                                                    self.timestamp, blurb) +
                '{}+ interested!\n'.format(self.gauge_interest()) +
                ('{}\n' * len(self.followups())).format(*self.followups()) +
                '{}\n\n'.format(self.link))

    def is_seller(self) -> bool:
        """
        Returns True iff the content of the post is likely a seller. All product
        posts are sellers.
        """
        keywords = ['budget']
        for word in keywords:
            if word in self.content.lower():
                return False
        return True

    def is_sublet(self) -> bool:
        """
        Returns True iff the content of the post is likely a sublet.
        """
        keywords = ['sublet', 'sublease']
        for word in keywords:
            if word in self.content.lower():
                return True
        return False

    def in_price_range(self, upper: int, lower: int=0) -> bool:
        """
        Returns True iff the price of the post is between the lower and upper
        bounds, inclusive.
        """
        return lower <= self.price <= upper

    def gauge_interest(self) -> int:
        """
        Returns the number of people who are likely interested in the post.
        """
        return sum([x.messaged for x in self.comments])

    def followups(self) -> List[Comment]:
        """
        Returns comments in the post made by the post author.
        """
        return [x for x in self.comments if x.author == self.author]


def product_price(price: str) -> int:
    """
    Returns the number of dollars of price.

    >>> product_price('$200')
    200
    >>> product_price('$1,299.99')
    1299
    """
    value = ''
    for character in price[1:]:
        if character.isnumeric():
            value += character
        elif character != ',':
            break
    if value == '':
        return -1
    return int(value)


def extract_prices(body: str) -> List[int]:
    """
    Returns a list of prices found in a body of text. Prices must be preceded by
    a dollar sign.

    >>> text = 'It is $1,000.50/month total; the bedroom is $500.'
    >>> extract_prices(text)
    [1000, 500]
    """
    prices = []
    price = ''
    i = 0
    while i < len(body):
        if body[i] == '$':
            price += body[i]
        elif len(price) > 0 and body[i].isnumeric():
            price += body[i]
        elif len(price) > 0 and body[i] != ',':
            prices.append(product_price(price))
            price = ''
        i += 1
    return prices


def lowest_price(prices: List[int]) -> Union[int, None]:
    """
    Returns the lowest price in prices, as long it surpasses LOW_PRICE. Returns
    None if there are no suitable prices.

    >>> lowest_price([2000, 1000, 1500])
    1000
    >>> lowest_price([10, 25, 1000])
    1000
    >>> print(lowest_price([10]))
    None
    """
    new_prices = [x for x in prices if x > Post.LOW_PRICE]
    if new_prices != []:
        return min(new_prices)
    return None


if __name__ == '__main__':
    file_ = open('GROUP_PAGE.html', 'rb')
    soup_ = BeautifulSoup(file_, 'html.parser')
    tags_ = soup_.find_all(class_='userContentWrapper')
    posts_ = [Post(x) for x in tags_]
    for item in posts_:
        print(item)
    print('All done!')
