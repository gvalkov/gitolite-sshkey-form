package Util;

use v5.12;
use strict;
use warnings;

use File::Temp qw(tempfile);
use IPC::System::Simple qw(run);

use File::Basename;
use Try::Tiny;


sub splitkey {
    split '@', (basename shift, '.pub');
}

sub joinkey {
    my ($name, $machine) = @_;
    return defined($machine) ? "$name\@$machine.pub" : "$name.pub";
}

sub nextinseq {
    my @seq = @_;
    my @onlyints = map { $_ =~ /^\d+$/ ? $_ + 0 : () } @seq;

    return 0 unless @onlyints;
    return $onlyints[0] + 1 if ((scalar @onlyints) == 1);

    my $index;
    while (my ($index, $el) = each @onlyints) {
        last if $index >= (scalar @onlyints)-1;
        if ( ($onlyints[$index+1] - $el) > 1 ) {
            return $el + 1;
        }
    }

    return $onlyints[$#onlyints] + 1;
}

sub iskeyvalid {
    my ($fh, $fn) = tempfile();

    print $fh shift; $fh->flush;
    system "ssh-keygen -l -f $fn >/dev/null 2>&1";

    return $? == 0;
}

1;
