use strict;
use warnings;
use ExtUtils::MakeMaker;

# Normalize version strings like 6.30_02 to 6.3002,
# so that we can do numerical comparisons on it.
my $eumm_version = $ExtUtils::MakeMaker::VERSION;
$eumm_version =~ s/_//;

WriteMakefile(
    NAME                => 'gitolite_sshkey_form',
    AUTHOR              => q{Georgi Valkov <georgi.t.valkov@gmail.com>},
    VERSION_FROM        => 'webapp.pl',
    ABSTRACT            => 'Webapp for submitting ssh public keys to gitolite',
    ($eumm_version >= 6.3001
      ? ('LICENSE'=> 'perl')
      : ()),
    PL_FILES            => {},
    PREREQ_PM => {
        'Test::More'            => 0,
        'Test::Exception'       => 0,
        'YAML'                  => 0.90,
        'Dancer2'               => 0.14,
        'Git::Repository'       => 1.311,
        'Try::Tiny'             => 0.22,
        'IPC::System::Simple'   => 1.25,
        'MIME::Base64::URLSafe' => 0,
        'List::MoreUtils'       => 0,
    },
    dist                => { COMPRESS => 'gzip -9f', SUFFIX => 'gz' },
    clean               => { FILES    => 'gitolite_sshkey_form-*'   },
);
