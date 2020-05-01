## bible_chapter_template.mako
<%inherit file="base.mako"/>
    <main id="main_content" role="main" tabindex="-1">
        <h2>${words_in_chapter} word occurrences in ${book_abbrev} ${chapter} in the KJV (${words_in_bible} word occurrences in the entire KJV):</h2>
        <a download="${book_abbrev}${str(chapter).zfill(3)}_word_freq.csv" href="${book_abbrev}${str(chapter).zfill(3)}_word_freq.csv" target="_blank">Open or download ${book_abbrev}${str(chapter).zfill(3)}_word_freq.csv</a><br>
        <p>
            The columns in the sortable table below are:
            <ul>
                <li>Word: A word which occurs in this chapter of the KJV Bible</li>
                <li>In chapter: The number of occurrences of that word in this chapter of the KJV</li>
                <li>In KJV: The number of occurrences of that word in the entire KJV</li>
                <li>Weighted Freq: The weighted relative frequency of that word in this chapter of the KJV</li>
                <li>Unweighted Freq: The unweighted relative frequency of that word in this chapter of the KJV</li>
            </ul>
            ## TODO: Replace TBD below with ...
            (See TBD for further explanation of both types of relative frequency.)
        </p>

        <!-- Table sorting uses the following script, as explained at
        https://stackoverflow.com/questions/10683712/html-table-sort/51648529 -->
        <script src="https://www.kryogenix.org/code/browser/sorttable/sorttable.js"></script>

        <table class="sortable">
            <thead>
                <tr>
                    <th title="Field #1">Word</th>
                    <th title="Field #2">In chapter</th>
                    <th title="Field #3">In KJV</th>
                    <th title="Field #4">Weighted Freq</th>
                    <th title="Field #4">Unweighted Freq</th>
                </tr>
            </thead>
            <tbody>
                % for row in rows:
                <tr>
                    <td>${row[0]}</td>
                    <td class="integer">${row[1]}</td>
                    <td class="integer">${row[2]}</td>
                    <td>${row[3]}</td>
                    <td>${row[4]}</td>
                </tr>
                % endfor
            </tbody>
        </table>
    </main>