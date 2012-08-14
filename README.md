fastnetntlm.py
==============

This script will quickly crack netntlm LM hashes when given a John/Cain NTLMv1 hash or hashfile. It uses rcracki and rainbow tables to recover the first 7 characters, then uses John's netntlm.pl to bruteforce the remaining characters. Original code swiped from Tim Medin (http://pauldotcom.com/wiki/index.php/Episode270)

Usage: fastnetntlm.py [options] hash[or]hashfile

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -a RT_ALPHA, --alpha=RT_ALPHA
                        path to halflmchall_alpha-numeric rainbow tables
  -b RT_ALLSPACE, --all=RT_ALLSPACE
                        path to halflmchall_all-space rainbow tables
  -v, --verbose         print status messages
  -o OUTPUT, --output=OUTPUT
                        optional output file containing passwords
  -t TIMEOUT, --timeout=TIMEOUT
                        optional timeout for bruteforcing the 7+ characters of
                        a particular hash. If the timeout if reached,
                        <timeout> will be outputted as the password

  Suplementary executable locations:
    If your file locations differ from the default use these options

    -p PERL, --perlpath=PERL
                        path to perl [default: /usr/bin/perl]
    -j JOHNNETNTLM, --johnnetntlm=JOHNNETNTLM
                        path to John the Ripper's netntlm.pl from Jumbo Pack
                        [default: /usr/share/john/netntlm.pl]
    -r RCRACKI, --rcracki=RCRACKI
                        path to rcracki_mt [default: /usr/bin/rcracki_mt]
