import * as path from "path";
import * as cdk from "@aws-cdk/core";
import * as lambda from "@aws-cdk/aws-lambda";
import * as lambdapython from "@aws-cdk/aws-lambda-python";
import { LambdaRestApi } from "@aws-cdk/aws-apigateway";
import { Duration, RemovalPolicy, RemoveTag } from "@aws-cdk/core";

export class LineMessengerStackLambda extends cdk.Stack {
  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    // 環境変数
    const phase = process.env.PHASE;

    super(scope, `${phase}-${id}`, props);

    ////////////////////////////
    // Python lambda
    ////////////////////////////

    // アプリケーションが依存するライブラリを載せたlayer
    const layerForApp = new lambdapython.PythonLayerVersion(
      this,
      "python-lambda-layer-for-app",
      {
        layerVersionName: "python-lambda-layer-for-app",
        entry: path.resolve(__dirname, "../lambda/layer/app"),
        compatibleRuntimes: [lambda.Runtime.PYTHON_3_7],
      }
    );

    // コード差分がない場合のエラー抑止のため
    const uniqueVersionId = `${new Date().getTime()}`;

    const lineMessengerFunction = new lambdapython.PythonFunction(
      this,
      "fn-line-messenger",
      {
        functionName: `${phase}-line-messenger`,
        description: `This lambda deployed at ${uniqueVersionId}`,
        runtime: lambda.Runtime.PYTHON_3_7,
        entry: path.resolve(__dirname, "../lambda/src/line_messenger"),
        index: "index.py",
        handler: "handler",
        layers: [layerForApp],
        timeout: Duration.seconds(300),
        memorySize: 512,
        environment: {
          LINE_CHANNEL_ACCESS_TOKEN:
            process.env.LINE_CHANNEL_ACCESS_TOKEN || "dummy",
          LINE_SEND_ID_1: process.env.LINE_SEND_ID_1 || "dummy",
          LINE_SEND_GROUP_ID_1: process.env.LINE_SEND_GROUP_ID_1 || "dummy",
        },
      }
    );
    cdk.Tags.of(lineMessengerFunction).add("runtime", "python");

    //+++++++++++++++++++++++++++++++++++
    // dev function version and alias
    //+++++++++++++++++++++++++++++++++++
    if (phase === "dev") {
      // development エイリアスに最新バージョンを指定
      const currentVersion = lineMessengerFunction.currentVersion;
      const development = new lambda.Alias(this, "DevelopmentAlias", {
        aliasName: "develop",
        version: currentVersion,
      });

      // lambdaのdevelopエイリアスを、apiGateway "dev" ステージに紐付け
      const devApi = new LambdaRestApi(this, "LineMessengerDevEndpoint", {
        handler: development,
        deployOptions: {
          stageName: "dev",
        },
        proxy: false,
      });
      // TODO: OpenAPI (Swagger) 対応
      devApi.root.addResource("line").addResource("message").addMethod("POST");
    }

    //+++++++++++++++++++++++++++++++++++
    // prd function version and alias
    //+++++++++++++++++++++++++++++++++++
    if (phase === "prd") {
      // バージョンはデプロイごとに発行するが、エイリアスの切り替えまではしない
      new lambda.Version(this, `version-line-messenger-${uniqueVersionId}`, {
        lambda: lineMessengerFunction,
        // prdは検証してから切り替えたいので、古いバージョンを残す
        removalPolicy: RemovalPolicy.RETAIN,
      });

      // エイリアスが紐づくバージョンは固定している
      // 動作に問題なければlive.shで目的のバージョンにエイリアスを切り替える
      const production = new lambda.Alias(this, "ProductionAlias", {
        aliasName: "prod",
        version: lambda.Version.fromVersionArn(
          this,
          "ProductionVersion",
          `${lineMessengerFunction.functionArn}:14` // 固定(live.shで切り替え)
        ),
      });

      // lambdaのprodエイリアスを、apiGateway "prd" ステージに紐付け
      // TODO: 1つのAPIでmulti stageを紐付けたかったがCDKでやり方が分からなかった
      const prdApi = new LambdaRestApi(this, "LineMessengerProdEndpoint", {
        handler: production,
        deployOptions: {
          stageName: "prd",
        },
        proxy: false,
      });
      // TODO: OpenAPI (Swagger) 対応
      prdApi.root.addResource("line").addResource("message").addMethod("POST");
    }
  }
}
