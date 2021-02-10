#!/bin/bash

CODE_REPO=ssh://git-codecommit.ap-northeast-1.amazonaws.com/v1/repos/pac-job
CODE_DIR=/usr/local/pac-job

git clone --config credential.helper='!aws --region ap-northeast-1 codecommit credential-helper $@' --config credential.UseHttpPath=true $CODE_REPO $CODE_DIR

sh /usr/local/pac-job/run.sh
