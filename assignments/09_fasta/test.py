#!/usr/bin/env python3
"""tests for au_pair.py"""

import os
import re
import random
import string
from subprocess import getstatusoutput
from shutil import rmtree
from Bio import SeqIO

prg = './au_pair.py'
small_fa = 'inputs/reads1.fa'
large_fa = 'inputs/reads2.fasta'


# --------------------------------------------------
def random_filename():
    """generate a random filename"""

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['', '-h', '--help']:
        rv, out = getstatusoutput('{} {}'.format(prg, flag))
        assert (rv > 0) if flag == '' else (rv == 0)
        assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_bad_input():
    """bad input"""

    bad = random_filename()
    rv, out = getstatusoutput(f'{prg} {bad}')
    assert rv != 0
    assert re.search(f"No such file or directory: '{bad}'", out)


# --------------------------------------------------
def test_good_input1():
    """fasta to fasta"""

    out_dir = 'split'
    if os.path.isdir(out_dir):
        rmtree(out_dir)

    try:
        print('{} {}'.format(prg, small_fa))
        rv, _ = getstatusoutput('{} {}'.format(prg, small_fa))
        assert rv == 0
        assert os.path.isdir(out_dir)

        assert len(list(SeqIO.parse(small_fa, 'fasta'))) == 4

        forward = os.path.join(out_dir, 'reads1_1.fa')
        reverse = os.path.join(out_dir, 'reads1_2.fa')

        assert os.path.isfile(forward)
        assert os.path.isfile(reverse)

        assert len(list(SeqIO.parse(forward, 'fasta'))) == 2
        assert len(list(SeqIO.parse(reverse, 'fasta'))) == 2

    finally:
        rmtree(out_dir)


# --------------------------------------------------
def test_good_input2():
    """fasta to fasta"""

    out_dir = random_filename()
    if os.path.isdir(out_dir):
        rmtree(out_dir)

    try:
        out_flag = '-o' if random.choice([True, False]) else '--outdir'
        rv, out = getstatusoutput('{} {} {} {}'.format(prg, out_flag, out_dir,
                                                       large_fa))
        assert rv == 0
        assert os.path.isdir(out_dir)

        assert len(list(SeqIO.parse(large_fa, 'fasta'))) == 500

        forward = os.path.join(out_dir, 'reads2_1.fasta')
        reverse = os.path.join(out_dir, 'reads2_2.fasta')
        print(forward)
        print(reverse)

        assert os.path.isfile(forward)
        assert os.path.isfile(reverse)

        assert len(list(SeqIO.parse(forward, 'fasta'))) == 250
        assert len(list(SeqIO.parse(reverse, 'fasta'))) == 250

    finally:
        rmtree(out_dir)
