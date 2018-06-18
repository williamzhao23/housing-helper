Housing Helper - William Zhao

    This program uses Selenium and a Firefox browser to scroll through a
Facebook group page. After scrolling through, the page's html is downloaded to
GROUP_PAGE.html. Then, the program uses Beautiful Soup to parse the html and
isolate posts and comments. The posts are filtered and then printed.
    To use the program, just run housing_helper.py.
    A future goal is to write an html file so the results are more readable and
can be easily preserved. Also, a search by proximity would be helpful for the
posts that do give a location.



Extended notes on some functions:

page_to_html:
 - The initialize_facebook function clicks on a 'generic' part of the page,
because upon logging in, Facebook asks to send notifications and dims the
screen. This line can be commented out if the screen does not dim.

post:
 - The initializer for Post sometimes fails, when a post tag
(class_=userContentWrapper) fails to have the author tag (class_=fwn fcg). In
this case, Post.author is set to something arbitrary. These "posts" are likely
ads, which means that all relevant user posts are still properly processed.
 - A product with price 'FREE' is filtered since free rooms do not exist. To
include them without breaking comparisons, set Post.price to 0 instead.

housing_helper:
 - page_to_html.view_comments can take a lot of time for just a bit more
information, which may not be a good tradeoff, so comment out the line if speed
is more valued.
