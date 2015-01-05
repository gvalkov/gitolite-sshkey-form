use v5.12;
use strict;
use warnings;

use Test::More tests => 5;
use File::Slurp;
use File::Temp qw(tempfile tempdir);

use lib './t';
use util qw(sshkeygen);

use_ok 'Gitolite';
use Gitolite;


my $path = tempdir(CLEANUP => 1);
my $path2 = tempdir(CLEANUP => 1);
system "git init --bare $path";
system "git clone $path $path2";
mkdir "$path2/keydir";
system "touch $path2/keydir/.keep";
system "cd $path2; git add keydir/.keep";
system "cd $path2; git commit -m '' --allow-empty-message keydir/.keep";
system "cd $path2; git push origin HEAD";

my $tmpd = tempdir(CLEANUP => 1);
my $repo = Gitolite->new($tmpd, "file://$path/");
ok($repo);

my $joe1 = sshkeygen "$tmpd/keydir/joe\@1";
$repo->addkey('joe', $joe1);
$repo->addkey('joe', $joe1);

ok($repo->keyexists('joe', $joe1), 'keyexists');
ok(!$repo->keyexists('joe', 'asdf'), 'keyexists');

is_deeply([$repo->listkeys('joe')], [['joe', '0', $joe1], ['joe', '1', $joe1]] , 'git-listkeys');

$repo->dropkey('joe', '1');
# is_deeply([$repo->listkeys('joe')], [['joe', '0', $joe1]] , 'git-listkeys');
