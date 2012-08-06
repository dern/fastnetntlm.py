fastnetntlm.py
==============

Updates to Tim Medin's script. Originally from http://pauldotcom.com/wiki/index.php/Episode270

Usage: fastnetntlm.py [options] hash[or]hashfile

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -a RT_ALPHA, --alpha=RT_ALPHA
                        path to halflmchall_alpha-numeric rainbow tables
  -b RT_ALLSPACE, --all=RT_ALLSPACE
                        path to halflmchall_all-space rainbow tables
  -v, --verbose         don't print status messages to stdout
  -o OUTPUT, --output=OUTPUT
                        optional output file containing passwords
  -t TIMEOUT, --timeout=TIMEOUT
                        optional timeout for bruteforcing the 7+ characters of
                        a particular hash. :TIMEOUT: will be outputted as the
                        password

  Suplementary executable locations:
    If your file locations differ from the default use these options

    -p PERL, --perlpath=PERL
                        path to perl (default is /usr/bin/perl)
    -j JOHNNETNTLM, --johnnetntlm=JOHNNETNTLM
                        path to John the Ripper's netntlm.pl from Jumbo Pack
                        (default is /usr/share/john/netntlm.pl)
    -r RCRACKI, --rcracki=RCRACKI
                        path to rcracki_mt (default is /usr/bin/rcracki_mt)

