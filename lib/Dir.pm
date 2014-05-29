package Dir;

use v5.12;
use strict;
use warnings;
use Util;

use File::Spec;
use File::Path;
use File::Slurp;

sub new {
    my $cls = shift;
    my ($workdir) = @_;

    my $self = bless {
        workdir => $workdir,
    }, $cls;

    if (! -e $workdir) {
        File::Path::make_path $workdir;
    } elsif (! -d $workdir) {
        die "$workdir is not a directory";
    }

    return $self;
}

sub catpath {
    my $self = shift;
    File::Spec->catfile($self->{workdir}, @_);
}

sub keyexists {
    my ($self, $user, $key) = @_;

    my @keys = $self->listkeys($user, 0);
    for (@keys) { return 1 if $_->[-1] eq $key; }
}

sub listkeys {
    my ($self, $user, $namesonly) = @_;

    my @keys = glob "$self->{workdir}/$user@*.pub";
    map [Util::splitkey($_), $namesonly ? () : File::Slurp::read_file($_)], @keys;
}

sub dropkey {
    my ($self, $user, $machine) = @_;
    my $path = $self->catpath(Util::joinkey($user, $machine));
    unlink($path);
}

sub addkey {
    my ($self, $user, $data) = @_;

    my @keys = map {$_->[1]} $self->listkeys($user);
    my $next = Util::nextinseq @keys;
    my $path = $self->catpath(Util::joinkey($user, $next));

    open my $fh, '>', $path;
    print $fh $data;
    close $fh;
    return $path;
}

1;
