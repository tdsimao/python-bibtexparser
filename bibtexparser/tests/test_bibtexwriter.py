# coding: utf-8
import tempfile
import unittest
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase


class TestBibTexWriter(unittest.TestCase):
    def test_content_entries_only(self):
        with open('bibtexparser/tests/data/multiple_entries_and_comments.bib') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        writer = BibTexWriter()
        writer.contents = ['entries']
        result = bibtexparser.dumps(bib_database, writer)
        expected = \
"""@book{Toto3000,
 author = {Toto, A and Titi, B},
 title = {A title}
}

@article{Wigner1938,
 author = {Wigner, E.},
 doi = {10.1039/TF9383400029},
 issn = {0014-7672},
 journal = {Trans. Faraday Soc.},
 owner = {fr},
 pages = {29--41},
 publisher = {The Royal Society of Chemistry},
 title = {The transition state method},
 volume = {34},
 year = {1938}
}

@book{Yablon2005,
 author = {Yablon, A.D.},
 publisher = {Springer},
 title = {Optical fiber fusion slicing},
 year = {2005}
}
"""
        self.assertEqual(result, expected)

    def test_content_comment_only(self):
        with open('bibtexparser/tests/data/multiple_entries_and_comments.bib') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        writer = BibTexWriter()
        writer.contents = ['comments']
        result = bibtexparser.dumps(bib_database, writer)
        expected = \
"""@comment{}

@comment{A comment}

"""
        self.assertEqual(result, expected)

    def test_indent(self):
        bib_database = BibDatabase()
        bib_database.entries = [{'ID': 'abc123',
                                 'ENTRYTYPE': 'book',
                                 'author': 'test'}]
        writer = BibTexWriter()
        writer.indent = '  '
        result = bibtexparser.dumps(bib_database, writer)
        expected = \
"""@book{abc123,
  author = {test}
}
"""
        self.assertEqual(result, expected)

    def test_align(self):
        bib_database = BibDatabase()
        bib_database.entries = [{'ID': 'abc123',
                                 'ENTRYTYPE': 'book',
                                 'author': 'test',
                                 'thisisaverylongkey': 'longvalue'}]
        writer = BibTexWriter()
        writer.align_values = True
        result = bibtexparser.dumps(bib_database, writer)
        expected = \
"""@book{abc123,
 author             = {test},
 thisisaverylongkey = {longvalue}
}
"""
        self.assertEqual(result, expected)

        with open('bibtexparser/tests/data/multiple_entries_and_comments.bib') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        writer = BibTexWriter()
        writer.contents = ['entries']
        writer.align_values = True
        result = bibtexparser.dumps(bib_database, writer)
        expected = \
"""@book{Toto3000,
 author    = {Toto, A and Titi, B},
 title     = {A title}
}

@article{Wigner1938,
 author    = {Wigner, E.},
 doi       = {10.1039/TF9383400029},
 issn      = {0014-7672},
 journal   = {Trans. Faraday Soc.},
 owner     = {fr},
 pages     = {29--41},
 publisher = {The Royal Society of Chemistry},
 title     = {The transition state method},
 volume    = {34},
 year      = {1938}
}

@book{Yablon2005,
 author    = {Yablon, A.D.},
 publisher = {Springer},
 title     = {Optical fiber fusion slicing},
 year      = {2005}
}
"""
        self.assertEqual(result, expected)


    def test_entry_separator(self):
        bib_database = BibDatabase()
        bib_database.entries = [{'ID': 'abc123',
                                 'ENTRYTYPE': 'book',
                                 'author': 'test'}]
        writer = BibTexWriter()
        writer.entry_separator = ''
        result = bibtexparser.dumps(bib_database, writer)
        expected = \
"""@book{abc123,
 author = {test}
}
"""
        self.assertEqual(result, expected)

    def test_display_order(self):
        with open('bibtexparser/tests/data/multiple_entries_and_comments.bib') as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        writer = BibTexWriter()
        writer.contents = ['entries']
        writer.display_order = ['year', 'publisher', 'title']
        result = bibtexparser.dumps(bib_database, writer)
        expected = \
"""@book{Toto3000,
 title = {A title},
 author = {Toto, A and Titi, B}
}

@article{Wigner1938,
 year = {1938},
 publisher = {The Royal Society of Chemistry},
 title = {The transition state method},
 author = {Wigner, E.},
 doi = {10.1039/TF9383400029},
 issn = {0014-7672},
 journal = {Trans. Faraday Soc.},
 owner = {fr},
 pages = {29--41},
 volume = {34}
}

@book{Yablon2005,
 year = {2005},
 publisher = {Springer},
 title = {Optical fiber fusion slicing},
 author = {Yablon, A.D.}
}
"""
        self.assertEqual(result, expected)


class TestEntrySorting(unittest.TestCase):
    bib_database = BibDatabase()
    bib_database.entries = [{'ID': 'b',
                             'ENTRYTYPE': 'article'},
                            {'ID': 'c',
                             'ENTRYTYPE': 'book'},
                            {'ID': 'a',
                             'ENTRYTYPE': 'book'}]

    def test_sort_default(self):
        result = bibtexparser.dumps(self.bib_database)
        expected = "@book{a\n}\n\n@article{b\n}\n\n@book{c\n}\n"
        self.assertEqual(result, expected)

    def test_sort_none(self):
        writer = BibTexWriter()
        writer.order_entries_by = None
        result = bibtexparser.dumps(self.bib_database, writer)
        expected = "@article{b\n}\n\n@book{c\n}\n\n@book{a\n}\n"
        self.assertEqual(result, expected)

    def test_sort_id(self):
        writer = BibTexWriter()
        writer.order_entries_by = ('ID', )
        result = bibtexparser.dumps(self.bib_database, writer)
        expected = "@book{a\n}\n\n@article{b\n}\n\n@book{c\n}\n"
        self.assertEqual(result, expected)

    def test_sort_type(self):
        writer = BibTexWriter()
        writer.order_entries_by = ('ENTRYTYPE', )
        result = bibtexparser.dumps(self.bib_database, writer)
        expected = "@article{b\n}\n\n@book{c\n}\n\n@book{a\n}\n"
        self.assertEqual(result, expected)

    def test_sort_type_id(self):
        writer = BibTexWriter()
        writer.order_entries_by = ('ENTRYTYPE', 'ID')
        result = bibtexparser.dumps(self.bib_database, writer)
        expected = "@article{b\n}\n\n@book{a\n}\n\n@book{c\n}\n"
        self.assertEqual(result, expected)

    def test_sort_missing_field(self):
        bib_database = BibDatabase()
        bib_database.entries = [{'ID': 'b',
                                 'ENTRYTYPE': 'article',
                                 'year': '2000'},
                                {'ID': 'c',
                                 'ENTRYTYPE': 'book',
                                 'year': '2010'},
                                {'ID': 'a',
                                 'ENTRYTYPE': 'book'}]
        writer = BibTexWriter()
        writer.order_entries_by = ('year', )
        result = bibtexparser.dumps(bib_database, writer)
        expected = "@book{a\n}\n\n@article{b,\n year = {2000}\n}\n\n@book{c,\n year = {2010}\n}\n"
        self.assertEqual(result, expected)

    def test_unicode_problems(self):
        # See #51
        bibtex = """
        @article{Mesa-Gresa2013,
            abstract = {During a 4-week period half the mice (n = 16) were exposed to EE and the other half (n = 16) remained in a standard environment (SE). Aggr. Behav. 9999:XX-XX, 2013. © 2013 Wiley Periodicals, Inc.},
            author = {Mesa-Gresa, Patricia and P\'{e}rez-Martinez, Asunci\'{o}n and Redolat, Rosa},
            doi = {10.1002/ab.21481},
            file = {:Users/jscholz/Documents/mendeley/Mesa-Gresa, P\'{e}rez-Martinez, Redolat - 2013 - Environmental Enrichment Improves Novel Object Recognition and Enhances Agonistic Behavior.pdf:pdf},
            issn = {1098-2337},
            journal = {Aggressive behavior},
            month = "apr",
            number = {April},
            pages = {269--279},
            pmid = {23588702},
            title = {{Environmental Enrichment Improves Novel Object Recognition and Enhances Agonistic Behavior in Male Mice.}},
            url = {http://www.ncbi.nlm.nih.gov/pubmed/23588702},
            volume = {39},
            year = {2013}
        }
        """
        bibdb = bibtexparser.loads(bibtex)
        with tempfile.TemporaryFile(mode='w+') as bibtex_file:
            bibtexparser.dump(bibdb, bibtex_file)
            # No exception should be raised

