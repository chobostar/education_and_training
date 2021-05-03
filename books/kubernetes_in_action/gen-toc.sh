#!/bin/bash

set -e

cd "$(dirname "$0")"
wget https://raw.githubusercontent.com/ekalinin/github-markdown-toc/master/gh-md-toc
chmod a+x gh-md-toc
cat README.md | ./gh-md-toc -
rm gh-md-toc
