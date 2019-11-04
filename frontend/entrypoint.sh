#!/usr/bin/env sh
bash
yarn global add create-react-app
create-react-app app
cd app
chown node:node -R .
chmod -R 777 .
yarn install
# uncomment the following line to upgrade all packages
# yarn upgrade --latest
yarn start
