use v5.12;
use strict;
use warnings;

use Test::More tests => 8;
use File::Slurp;
use File::Temp qw(tempfile tempdir);

use lib './t';
use util qw(sshkeygen);

use_ok 'Dir';
use Dir;

my $path = tempdir( CLEANUP => 1 );
my $repo = Dir->new($path);
ok(-d $repo->{workdir}, 'create workdir');

my $joe1 = sshkeygen "$path/joe\@1";
my $joe2 = sshkeygen "$path/joe\@2";
is_deeply([$repo->listkeys('joe')], [['joe', '1', $joe1], ['joe', '2', $joe2]] , 'dir-listkeys');

ok($repo->keyexists('joe', $joe1), 'keyexists');
ok(!$repo->keyexists('joe', 'asdf'), 'keyexists');

$repo->dropkey('joe', '1');
is_deeply([$repo->listkeys('joe')], [['joe', '2', $joe2]] , 'dir-dropkey');

$path = $repo->addkey('joe', 'zxcv');
is_deeply([$repo->listkeys('joe')], [['joe', '2', $joe2], ['joe', '3', 'zxcv']] , 'add-dropkey');
ok(read_file($path) eq 'zxcv', 'dir-addkey')
