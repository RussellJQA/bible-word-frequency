## bible-word-frequency_index.mako
<%inherit file="base.mako"/>
    <main id='main_content' role='main' tabindex='-1'>
        ${readme_html}
        % for bible_book in bible_books:
        <a href='${str(book_nums[bible_books[bible_book][0]]).zfill(2)}_${bible_books[bible_book][0]}/${bible_books[bible_book][0]}_index.html'>${bible_book}</a><br>
        % endfor
    </main>
