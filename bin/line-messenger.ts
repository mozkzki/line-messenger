#!/usr/bin/env node
import * as cdk from "@aws-cdk/core";
import { LineMessengerStackLambda as LineMessengerStackLambda } from "../lib/line-messenger-stack-lambda";

const app = new cdk.App();

new LineMessengerStackLambda(app, "LineMessengerStackLambda");
