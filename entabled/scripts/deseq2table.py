"""
GUI, in a web browser, for exploring DESeq results using DataTables + jQuery
+ Bootstrap.

Converts a DESeq results file, as saved from R with::

    write.table(res, sep='\\t', row.names=FALSE)`

into a JavaScript array and places it in an HTML template.
"""
import entabled
import argparse
import os

if __name__ == "__main__":
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument(
        '--deseq',
        default=entabled.helpers.data_file("example_results.txt"),
        help='DESeq results text file (default: "example_results.txt"')
    ap.add_argument(
        '--output',
        default="example",
        help='Output directory to populate with HTML file plus '
        'JavaScript and CSS (default: "./example")')
    ap.add_argument(
        '--limit', type=int,
        help='Optional number of rows to limit output to (useful for testing')
    args = ap.parse_args()

    parser = entabled.DESeqResultsParser(args.deseq)
    data, header = parser.parse(limit=args.limit)
    d = entabled.DataTableCreator(
        data,
        header,
        title="DESeq results",
        minmax=['baseMeanA', 'baseMeanB', 'foldChange', 'log2FoldChange', 'padj'],
        above_text_rst=open(entabled.helpers.data_file('usage.rst')).read(),
    )
    d.render(
        outdir=args.output,
        html='deseq.html',
    )
