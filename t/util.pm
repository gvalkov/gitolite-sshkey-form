use v5.12;
use strict;
use warnings;

use File::Slurp;

sub sshkeygen {
    my $path = shift;
    my $real = shift // 1;
    my $bits = shift // 768;

    # say "generating ssh public key: $path";

    if ($real) {
        system "ssh-keygen -q -b $bits -N '' -f $path";
    } else {
        my @chars = ('a'..'z', 'A'..'Z', '0'..'9');
        open my $fh, '>', "$path.pub";
        say $fh join('', map {@chars[rand @chars]} 1..shift);
        close $fh;
    }
    
    return read_file($path . '.pub');
}

1;
