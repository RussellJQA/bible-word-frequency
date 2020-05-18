## base.mako
<!doctype html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="description" content="${description}">
    <meta name="keywords" content="${keywords}">
    <meta name="date" content="${datestamp}">
    <meta name="last-modified" content="${datestamp}">
    <meta name="language" content="english">
    <meta name="author" content="${author} (${site})">
    <meta name="copyright" content="${year} ${author}. All rights reserved.">
    <meta name="generator" content="HTML">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta property="og:site_name" content="${og_site_name}">
    <title>${title_h1}</title>

    <link rel="stylesheet" type="text/css" href="${styles_path}/style.css">
##  I had originally just put the style sheet in the root.
##  That worked fine except if I just opened a downloaded copy of the Web site,
##  and opened 1 of its pages directly.
##  So, to allow even that to work, I'm passing the style sheet location as
##  parameter to the template.
</head>

<body>

    <header role="banner"><%block name="header">
        <h1>${title_h1}</h1>
    </%block></header>
    ${self.body()}
    <footer role="contentinfo"><%block name="footer">
        <nav>
            <a href="#top">Back to Top</a>
## In HTML5, no "top" anchor is needed
            <a href="https://github.com/RussellJQA/eberean-bible-word-frequency" target="_blank"><img src="${images_path}/github-mark-64px.png" height="16" width="16" alt="GitHub repository"><span class="github-link-text">Website source code</span></a>
        </nav>
        <p>Built with <a href="https://www.makotemplates.org/" target="_blank">Mako templates</a> in <a href="https://www.python.org/" target="_blank">Python</a></p>
        <p>Copyright &copy; ${year} by <a href="${github_account}" target="_blank">${author}</a></p>
    </%block></footer>

</body>

</html>