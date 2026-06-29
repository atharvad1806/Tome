from ebooklib import epub

book = epub.EpubBook()
book.set_identifier('test123')
book.set_title('Test Book')
book.set_language('en')
book.add_author('Test Author')

c1 = epub.EpubHtml(title='Chapter 1', file_name='chap1.xhtml', lang='en')
c1.content = '<h1>Chapter 1: The Beginning</h1><p>' + ('Once upon a time there was a small dragon named Ember who lived in a cave. ' * 40) + '</p>'

c2 = epub.EpubHtml(title='Chapter 2', file_name='chap2.xhtml', lang='en')
c2.content = '<h1>Chapter 2: The Journey</h1><p>' + ('Ember decided to leave the cave and explore the world beyond the mountains. ' * 40) + '</p>'

book.add_item(c1)
book.add_item(c2)
book.toc = (c1, c2)
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
book.spine = ['nav', c1, c2]

epub.write_epub('sample_books/test.epub', book)
print('created test epub')