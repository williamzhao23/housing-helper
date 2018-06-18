"""
Module for reading Facebook comments.
"""
from bs4 import BeautifulSoup


class Comment:
    """
    Essential textual information of a Facebook comment.

    author - author of the ocmment
    content - the content of the comment
    messaged - whether the commenter messaged for the offer
    """
    author: str
    content: str
    messaged: bool

    # Facebook webpage elements may be changed later, so update constants
    CLASS = {'author': 'UFICommentActorName', 'content': 'UFICommentBody'}

    def __init__(self, tag: 'Tag') -> None:
        """
        Initiliaze a new comment using a Beautiful Soup tag object.

        Note: currently, the tag should have class UFICommentContentBlock, but
        any encompassing tag that is independent of other comments should work.
        """
        self.author = tag.find(class_=self.CLASS['author']).getText()
        self.content = tag.find(class_=self.CLASS['content']).getText()
        self.messaged = self.has_messaged()

    def __eq__(self, other: 'Comment') -> bool:
        """
        Returns True iff self and other are functionally the same comments.
        """
        return (type(self) == type(other) and self.author == other.author
                and self.content == other.content
                and self.messaged == other.messaged)

    def __str__(self) -> str:
        """
        Returns a string representation of self formatted like a comment.
        """
        return '{}: {}'.format(self.author, self.content)

    def has_messaged(self) -> bool:
        """
        Returns True iff the author of the comment has likely messaged the
        original poster.
        """
        keywords = ['messaged', 'interested', 'pm\'ed', 'pm ed']
        for word in keywords:
            if word in self.content.lower():
                return True
        return False


if __name__ == '__main__':
    file_ = open('GROUP_PAGE.html', 'rb')
    soup_ = BeautifulSoup(file_, 'html.parser')
    tags_ = soup_.find_all(class_='UFICommentContentBlock')
    comments_ = [Comment(x) for x in tags_]
    for item in comments_:
        print(item)
    print('All done!')
