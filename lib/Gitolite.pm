package Gitolite;

use v5.12;
use strict;
use warnings;
use Util;

use File::Spec;
use File::Path;
use File::Slurp;
use Git::Repository;
use Try::Tiny;


sub new {
    my $cls = shift;
    my ($workdir, $url) = @_;

    my $self = bless {
        workdir => $workdir,
        url => $url,
        author => 'Gitolite Publickey Form <nobody@localhost>',
        commit_msg_add => 'Added public key: user "%s", fn "%s"',
        commit_msg_del => 'Removed public key: user "%s", fn "%s"',
    }, $cls;

    $self->{repo} = $self->setup($workdir, $url);
    system "ls $self->{workdir}";
    if (! -e "$self->{workdir}/keydir") {
        die "error: ${workdir}/keydir does not exist (is this a gitolite repository?)";
    }

    return $self;
}

sub setup {
    my ($self, $workdir, $url) = @_;
    my $repo;

    try {
        $repo = Git::Repository->new(work_tree => $workdir);
    } catch {
        $repo = 0;
    };

    if ($repo) {
        my $remote_url;
        my @lines = $repo->run('remote', 'show', 'origin', '-n');

        for (@lines) {
            $remote_url = $1 if /Fetch URL: (.*)/;
            last if $remote_url;
        }

        if ($remote_url eq $url) {
            return $repo;
        } else {
            say "removing workdir: $workdir";
            File::Path::remove_tree($workdir);
            Git::Repository->run(clone => $url, $workdir);
            return Git::Repository->new(work_tree => $workdir);
        }
    } else {
        File::Path::remove_tree($workdir);
        Git::Repository->run(clone => $url, $workdir);
        return Git::Repository->new(work_tree => $workdir);
    }
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

    my @lines = $self->{repo}->run('ls-files' => 'keydir');
    my @keys = grep /\.pub$/, @lines;
    @keys = map {"$self->{workdir}/$_"} @keys;
    map [Util::splitkey($_), $namesonly ? () : File::Slurp::read_file($_)], @keys;
}

sub addkey {
    my ($self, $user, $data) = @_;

    my @keys = map {$_->[1]} $self->listkeys($user);
    my $next = Util::nextinseq @keys;
    my $relpath = File::Spec->catfile('keydir', Util::joinkey($user, $next));
    my $path = $self->catpath($relpath);
    my $repo = $self->{repo};

    $repo->run(fetch => 'origin');
    $repo->run(reset => '--hard', 'origin/HEAD');

    open my $fh, '>', $path;
    print $fh $data;
    close $fh;

    $repo->run(add => $path);
    $repo->run(commit => $path,
               '--author', $self->{author},
               '-m', sprintf($self->{commit_msg_add}, $user, "$self->{workdir}/$relpath"));
    $repo->run(push => 'origin', 'HEAD');

    return $path;
}

sub dropkey {
    my ($self, $user, $machine) = @_;

    my $repo = $self->{repo};
    my $relpath = File::Spec->catfile('keydir', Util::joinkey($user, $machine));

    $repo->run(fetch => 'origin');
    $repo->run(reset => '--hard', 'origin/HEAD');
    $repo->run(rm => $relpath);
    $repo->run(commit =>  $relpath,
               '--author', $self->{author},
               '-m', sprintf($self->{commit_msg_del}, $user, $relpath));
    $repo->run(push => 'origin', 'HEAD');
}

1;
