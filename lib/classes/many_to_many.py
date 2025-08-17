# classes/many_to_many.py

class Article:
    all = []

    def __init__(self, author, magazine, title: str):
        if not isinstance(author, Author):
            raise Exception("Article author must be an Author instance.")
        if not isinstance(magazine, Magazine):
            raise Exception("Article magazine must be a Magazine instance.")
        if not isinstance(title, str) or len(title.strip()) == 0:
            raise Exception("Article title must be a non-empty string.")

        self._author = author
        self._magazine = magazine
        self._title = title
        Article.all.append(self)

    @property
    def author(self):
        return self._author
    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value
        # ignore invalid changes

    @property
    def magazine(self):
        return self._magazine
    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value
        # ignore invalid changes

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        # Immutable
        pass


class Author:
    def __init__(self, name: str):
        if not isinstance(name, str) or len(name.strip()) == 0:
            raise Exception("Author name must be a non-empty string.")
        self._name = name

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        # Immutable
        pass  

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        if not self.articles():
            return None
        return list({magazine.category for magazine in self.magazines()})


class Magazine:
    all = []

    def __init__(self, name: str, category: str):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise Exception("Magazine name must be a string between 2 and 16 characters.")
        if not isinstance(category, str) or len(category.strip()) == 0:
            raise Exception("Magazine category must be a non-empty string.")

        self._name = name
        self._category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if isinstance(value, str) and (2 <= len(value) <= 16):
            self._name = value
        # ignore invalid changes

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value.strip()) > 0:
            self._category = value
        # ignore invalid changes

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list({article.author for article in self.articles()})

    def article_titles(self):
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        counts = {}
        for article in self.articles():
            counts[article.author] = counts.get(article.author, 0) + 1
        authors = [author for author, count in counts.items() if count > 2]
        return authors if authors else None

    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        return max(cls.all, key=lambda mag: len(mag.articles()), default=None)