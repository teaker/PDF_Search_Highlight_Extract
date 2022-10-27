# PDF_Search_Highlight_Extract

This application will quickly search a PDF for user-defined search terms, will highlight all found terms, and will then save pages containing highlighted terms to a new file.

To build for windows, you can use the following command:

<pre>  pyinstaller --noconsole --onefile main.py </pre>

Terms entered into the first search term box will match all instances of the word/phrase.  
For instance, searching for "bot" would match **bot**, **bot**h, ro**bot**, etc.

Terms entered into the second search term box will only return whole words (exact matches).
For instance, entering "bot" into the second box would match **bot** but would not match both or robot.

You can enter search terms into both boxes simultaneously.

![alt text](https://github.com/teaker/PDF_Search_Highlight_Extract/blob/e488a57a74d6a0944dd9d7e28f253e3bb9aa2a9c/PDFsearch.jpg?raw=true)


