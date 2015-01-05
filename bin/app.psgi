#!/usr/bin/env perl

use v5.12;
use strict;
use warnings;

use FindBin;
use lib "$FindBin::Bin/../lib";
use WebSshKeyForm;

WebSshKeyForm->to_app;
