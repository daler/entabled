``entabled``
------------
Convert a text file of data into a browser-viewable format with filtering,
sorting, and full-text searching.

Uses `DataTables <http://www.datatables.net/>`_, `jQuery <http://jquery.com/>`_,
and `Bootstrap <http://twitter.github.com/bootstrap/>`_.

You are responsible for converting your data into a list-of-lists, though
there's already a helper for DESeq results (``entabled.DESeqResultsParser``),
as long as you've saved your data as described in the docstring of that class.

``entabled`` ships with some data files you can experiment with, see the
example below.

Example usage
~~~~~~~~~~~~~

Get example data file::

    >>> import entabled
    >>> deseq_results = entabled.helpers.data_file('example_results.txt')

Get the data as a list-of-lists, as well as the header::

    >>> d = entabled.DESeqResultsParser(deseq_results)
    >>> data, header = d.parse()

Write some text (as ReST), which will be converted to HTML and inserted into
the template.  Or use the example::

    >>> rst = open(entabled.helpers.data_file('usage.rst')).read()

Set up a ``DataTableCreator`` object.  `minmax` is a list of columns that will
have accordion-foldable min/max text input for filtering.  `above_text_rst` and
`below_text_rst` will be converted to HTML and inserted above and below the
table respectively::

    >>> t = entabled.DataTableCreator(
    ... data,
    ... header,
    ... minmax=['baseMeanA', 'baseMeanB', 'log2FoldChange', 'padj'],
    ... above_text_rst=rst,
    ... below_text_rst='Some example text')

Render it to the directory ``example``, and supply some additional CSS
styling::

    >>> additional_css = entabled.helpers.data_file('add.css')
    >>> t.render(outdir="example", html='deseq.html', additional_css=additional_css)

Open up ``example/deseq.html`` in a browser.
