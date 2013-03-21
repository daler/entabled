import simplejson
import os
import jinja2
from textwrap import dedent
from docutils.core import publish_string
import tempfile
import helpers

HERE = os.path.dirname(__file__)

# copy these over to destination
REQUIRED_FILES = [
    'static/js/DataTables-1.9.4/media/js/jquery.js',
    'static/bootstrap/js/bootstrap.min.js',
    'static/js/DataTables-1.9.4/media/js/jquery.dataTables.js',
    'static/js/tools.js',
    'static/bootstrap/css/bootstrap.css',
    'static/css/deseq.css',
    'static/js/DataTables-1.9.4/media/images/sort_asc.png',
    'static/js/DataTables-1.9.4/media/images/sort_both.png',
    'static/js/DataTables-1.9.4/media/images/sort_desc.png',
]
REQUIRED_FILES = [helpers.data_file(i) for i in REQUIRED_FILES]


def rst2html(rst, header_level=3):
    """
    Converts ReStructured Text `rst` to a block of HTML for incorporation into
    another HTML file -- so it strips html/head/body tags.  Use higher
    `header_level` values if you already have <h1> in the destination HTML.
    """
    # Make a custom template for rst2thml that does not insert the
    # html/head/body tags.
    tmp = tempfile.mktemp()
    fout = open(tmp, 'w')
    fout.write(dedent(
        '''
        %(body_pre_docinfo)s
        %(body)s
        '''))
    fout.close()
    settings_overrides = {
        'template': tmp,
        'initial_header_level': header_level,
        'doctitle_xform': False,
        'strip_classes': 'simple',
    }
    return publish_string(
        rst,
        writer_name='html',
        settings_overrides=settings_overrides
    )


class DESeqResultsParser(object):
    def __init__(self, results_file):
        """
        Assumes you've saved your data in R like this::

            write.table(res, file='results.txt', sep='\\t', row.names=FALSE)

        """
        self.results_file = results_file

    def parse(self, limit=None):
        """
        Returns a tuple (data, header) ready for inserting into a template.
        """
        # Save the header, and convert the rest of the text file into a list of
        # lists which will be placed into the template as a JavaScript array.
        #
        # However, we need to keep non-floats as strings in order to keep
        # JavaScript happy, hence the extra handling.
        f = open(self.results_file)
        while True:
            line = f.readline()
            if line.startswith('#'):
                continue
            header = line.strip().replace('"', '').split('\t')
            break
        deseqs = []
        for i, line in enumerate(f):
            if line.startswith('#'):
                continue
            if limit and (i == limit):
                break
            newrow = []
            line = line.strip().replace('"', '')
            for field in line.split('\t'):
                if field not in ('NA', '-Inf', 'Inf', 'nan', 'NaN'):
                    try:
                        field = float(field)
                    except ValueError, TypeError:
                        pass
                newrow.append(field)
            deseqs.append(newrow)
        return (deseqs, header)


class DataTableCreator(object):
    def __init__(self, data, header, title="Data table", minmax=None,
                 above_text_rst=None, below_text_rst=None):
        """
        :param data:
            A list of lists.

        :param header:
            A list as long as one of the lists in `data`, used for labeling
            columns


        :param title:
            Used for HTML title and for the navbar along the top

        :param minmax:
            A list that is a subset of `header` for which min/max controls will
            be created

        :param above_text_rst, below_text_rst:
            ReStructured Text strings that will be converted to HTML and then
            inserted into the template above and below the trable respectively.
        """

        above_text = ""
        if above_text_rst:
            above_text = rst2html(above_text_rst)

        below_text = ""
        if below_text_rst:
            below_text = rst2html(below_text_rst)

        context = {
            'data': data,
            'header': header,
            'title': title,
            'minmax': minmax or [],
            'above_text': above_text,
            'below_text': below_text,
        }

        self.context = context

    def render(self, outdir='.', html='table.html', additional_css=None):
        """
        :param outdir:
            HTML file and additional required files will be copied here.
            Directories will be created as needed.

        :param html:
            Name of the actual HTML file.
        """

        files_to_copy = []
        for req in REQUIRED_FILES:
            dest = os.path.join(
                outdir,
                (
                    os.path.relpath(req, start=helpers.data_dir())
                )
            )
            files_to_copy.append((req, dest))

        if additional_css:
            additional_css_dest = os.path.join(
                outdir, os.path.basename(additional_css))
            files_to_copy.append(
                (
                    additional_css,
                    additional_css_dest
                )
            )

        # Get template
        loader = jinja2.FileSystemLoader(helpers.data_file('templates'))

        if not additional_css:
            additional_css_string = ""
        else:

            additional_css_string = (
                '<link rel="stylesheet" type="text/css" href="%s">'
                % additional_css_dest)

        self.context['additional_css'] = additional_css_string

        env = jinja2.Environment(loader=loader)
        template = env.get_template('template.html')
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        fout = open(os.path.join(outdir, html), 'w')
        fout.write(template.render(**self.context))
        fout.close()

        for source, dest in files_to_copy:
            subdir = os.path.dirname(dest)
            if not os.path.exists(subdir):
                os.makedirs(subdir)
            cmds = 'cp %s %s' % (source, dest)
            os.system(cmds)


if __name__ == "__main__":
    data, header = DESeqResultsParser('example_results.txt').parse(limit=100)
    t = DataTableCreator(
        data,
        header,
        minmax=['baseMeanA', 'baseMeanB', 'log2FoldChange', 'padj'],
        above_text_rst=open('usage.rst').read(),
        below_text_rst="Some example text",
    )
    t.render(additional_css='add.css')
