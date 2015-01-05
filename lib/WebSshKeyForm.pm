package WebSshKeyForm;

use v5.12;
use strict;
use warnings;

use MIME::Base64::URLSafe;

use Dancer2;
use Template;

use Util;
use Dir;
use Gitolite;

#-----------------------------------------------------------------------------
our $VERSION = "1.0";

#-----------------------------------------------------------------------------
# Configuration.
#-----------------------------------------------------------------------------
my $author_name       = config->{AUTHOR_NAME}  //= q{Gitolite Publickey Form};
my $author_email      = config->{AUTHOR_EMAIL} //= q{nobody@localhost};
my $admin_repo_url    = config->{ADMIN_REPO}   //= "";
my $admin_repo_branch = config->{BRANCH}       //= "master";
my $workdir           = config->{WORKDIR}      or die 'Please set WORKDIR in config.yml';

my $repo;


if ($admin_repo_url) {
    $repo = Gitolite->new($workdir, $admin_repo_url);
} else {
    $repo = Dir->new($workdir);
}

#-----------------------------------------------------------------------------
# Routes.
#-----------------------------------------------------------------------------
get '/' => sub {
    my $remote_user = request->user // 'joe';
    my @keys = $repo->listkeys($remote_user);

    for my $key (@keys) {
        $key->[1] = urlsafe_b64encode($key->[1]);
    }

    my %ctx = (
        remote_user => $remote_user,
        sshkeys => \@keys,
        enable_identities => 0,
    );

    template 'index.tt' => \%ctx, {layout => undef};
};

#-----------------------------------------------------------------------------
get '/log' => sub {
    return "";
};

#-----------------------------------------------------------------------------
post '/add' => sub {
    my $remote_user = request->user // 'joe';
    my $data = params->{'data'};

    if (!length $data) {
        status 400;
        return 'Empty public key';
    }

    if (!Util::iskeyvalid $data) {
        status 400;
        return "Invalid public key";
    }

    if ($repo->keyexists($remote_user, $data)) {
        my $keysub = substr($data, 0, 12) . '...' . substr($data, -12);
        info "key '$keysub' already exists for user: $remote_user";
        return;
    }

    info "adding public key for user: $remote_user";
    $repo->addkey($remote_user, $data);
    return;
};

#-----------------------------------------------------------------------------
post '/drop/:machine' => sub {
    my $remote_user = request->user // 'joe';

    my $machine = urlsafe_b64decode(params->{machine});
    info "removing public key for user: $remote_user";
    say $repo->dropkey($remote_user, $machine);

    return;
};

#-----------------------------------------------------------------------------
post '/set-identity' => sub {
    return "";
};

#-----------------------------------------------------------------------------
any ['get', 'post'] => '/get-identity/:alias' => sub {
    return "";
};

#-----------------------------------------------------------------------------
#dance;
1;
