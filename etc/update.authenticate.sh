#!/bin/bash 
# set -u # is usually a good idea, but I got lazy with $faillog

# url to the web-sshkey-helper get-identity view
declare -r get_identity_url='http://<change me>/get-identity/'

# 1: will abort if the above url is unreachable
# 0: will continue if the above url is unreachable
declare -r flunk_on_curl_error=1

# where to log all authentication failures
declare -r faillog=""

declare -r refname=$1
declare -r oldrev=$2
declare -r newrev=$3

git_identity=$(curl -sf "${get_identity_url}/${GL_USER}")

if [[ $? -ne 0 ]]; then
    if [[ $flunk_on_curl_error -eq 0 ]]; then
        echo "error retrieving identity of ${GL_USER} ... continuing anyhow" >&2 && exit 0
    else
        echo "error retrieving identity of ${GL_USER} ... abort" >&2 && exit 1
    fi
fi

function logError () {
    exec >&2
    echo "unauthenticated commit by ${GL_USER} ... abort" | tee -a ${faillog}
    echo "  commit:    '${1}'" | tee -a ${faillog}
    echo "  committer: '${2}'" | tee -a ${faillog}
    echo "  culprit:   '${3}'" | tee -a ${faillog}
    [[ -f ${faillog} ]] && echo -e "  date:      '$(date)'\n" >> ${faillog}
}

for rev in $(git rev-list ${oldrev}..${newrev}); do
    committer=$(
    git cat-file commit ${rev} \
    | awk '/^committer/ {for (i=2; i<(NF-1); i++) {printf "%s ", $i} }')
    # please note the trailing whitespace that is left by the above call to awk

    # compare committer and git_identity stripped of whitespace 
    if [[ ${committer// /} != ${git_identity// /} ]]; then
        logError "${rev}" "${committer}" "${git_identity}"
        exit 1
    fi
done
