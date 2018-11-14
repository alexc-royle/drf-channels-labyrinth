#!/usr/bin/env sh
bash
yarn global add create-react-app
create-react-app app
cd app
chown node:node -R .
yarn install
yarn start
