## Housing Helper

Housing groups on Facebook require a lot of interaction such as logging in, scrolling, and sorting. In addition, many housing groups require an approved account to see its contents. This program scrolls through a Facebook group page on your account, simulating user input. After scrolling through, the page's HTML is downloaded and parsed to isolate posts and comments. Finally, the posts are filtered and printed. To use the program, just run `housing_helper.py`.

Requires Python, Beautiful Soup, Selenium (and geckodriver), and Firefox. Version numbers were not initially recorded, but updating all of them made this fully functional again after a year. However, due to the changing nature of websites and the fact that loading the posts takes a non-negligible amount of time, this program sometimes breaks. Here is some info on the different modules and common bugs:

`page_to_html`: Upon logging in, Facebook asks to send notifications and dims the screen, at least on Firefox. `initialize_facebook` clicks on a "generic" part of the page to remove this notification. This line can be commented out if the screen does not dim.

`post`: The initializer for Post sometimes fails when a post tag fails to have an author tag. These posts are likely ads. In this case, `Post.author` is set to something arbitrary. A product with price "FREE" is filtered since free rooms don't exist... To include them without breaking comparisons, set `Post.price` to 0 instead.

`housing_helper`: `page_to_html.view_comments` slows down the results and its value is relativey low, so comment out the line if you want an easy speed increase.

Bugs:
- If you get no/few results, it's likely the program was not able to scroll. The reason is unknown, but it may have to do with the notifications pop-up. Manually clicking seems to solve it, or maybe setting a sight delay on clicking.
- Changes to the names of buttons (sort by "new" vs "recent") breaks post sorting, but is easily detected and fixed.
- It is possible that the obfuscated class or ids will change in the future
