use v5.12;
use strict;
use warnings;

use Test::More tests => 14;
use File::Slurp;
use File::Temp qw(tempfile tempdir);

use lib './t';
use util qw(sshkeygen);

use_ok 'Util';
use Util;

# Tests
is_deeply([Util::splitkey 'joe@1.pub'], ['joe', '1'], 'splitkey');
is_deeply([Util::splitkey 'joe@pc.pub'], ['joe', 'pc'], 'splitkey');
is_deeply([Util::splitkey 'joe.pub'], ['joe'], 'splitkey');

is(Util::joinkey('joe', '1'), 'joe@1.pub', 'joinkey');
is(Util::joinkey('joe', 1), 'joe@1.pub', 'joinkey');
is(Util::joinkey('joe'), 'joe.pub', 'joinkey');

is(Util::nextinseq(), 0, 'nextinseq');
is(Util::nextinseq(0, 1, 2), 3, 'nextinseq');
is(Util::nextinseq(0, 1, 3), 2, 'nextinseq');
is(Util::nextinseq(0, 'asdf', 3, 5), 1, 'nextinseq');
is(Util::nextinseq(0, 1, 'asdf', 2, '3', 5), 4, 'nextinseq');
is(Util::nextinseq('asdf', '3'), 4, 'nextinseq');

my (undef, $fn) = tempfile(); unlink $fn;
sshkeygen($fn, 1);
ok(Util::iskeyvalid(read_file "$fn.pub"), 'iskeyvalid');
unlink $fn;
