# Serverless profile-photo checker film: FACTS

Every claim on screen or in the narration, where it comes from, and what was checked (research stage, 2026-11-01).

**Sources**
- Repo `andyyaro/serverless-profile-photo-checker`, public, one commit: `fd8589e` (fd8589ece6986e28dca96c27255d842f56e18a3b, 2026-08-19, "Initial commit: serverless profile-photo checker"). Cloned read-only for the research. Files: `python/rekognition.py`, `interact.py`, `lambda.tf`, `apigw.tf`, `Dockerfile`, `requirements.txt`, `goodphoto.jpeg`, `badphoto.png`, `README.md`, `quotes-service/` (not this film).
- Andy's own notes on the internship (not public), for its name and dates only.
- AWS reference: "Analyzing images with an AWS Lambda function", Amazon Rekognition Custom Labels Developer Guide, https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/ex-lambda.html (code headers: "Copyright Amazon.com, Inc. or its affiliates", SPDX Apache-2.0).
- Local checks (no AWS call, no credentials; evidence in `research/`): `terraform validate`, `terraform graph`, the real handler run with botocore's Stubber in place of Rekognition (`research/harness/run_handler.py`), and the real `interact.py` run against a 127.0.0.1 stand-in for the stage (`research/harness/run_cli.py`).

**Tests:** the repo has none. README, "Scope": "no automated tests". The proof beat therefore uses the resource count and `terraform validate`, never a test count.

## Narration

| id | line | source | verified |
|---|---|---|---|
| v01 | One question: is this usable as a profile photo? | README: "answers one question: is this usable as a profile photo?" | verbatim idea |
| v02 | And with two people in frame, which face is it about? | README: "with two people in frame, 'the face' is ambiguous" | rhetorical, from the README |
| v03 | This is the serverless profile-photo checker. | repo name; README title "Serverless profile-photo checker" | yes |
| v04 | A small client encodes the photo and posts it to API Gateway. | `interact.py` (42 lines): `base64.b64encode(...)`, `payload = {"image": data}`, `requests.post(url, json=payload)`; the URL is the API Gateway stage (`apigw.tf` output `deployment_invoke_url`) | yes |
| v05 | The gateway hands it to a Lambda function. | `apigw.tf`: `aws_api_gateway_integration` type `AWS`, `uri = aws_lambda_function.terraform_lambda_func.invoke_arn`; `aws_lambda_permission` `AllowExecutionFromAPIGateway` | yes |
| v06 | It asks Amazon Rekognition to describe the faces it finds. | `rekognition.py` l.34: `rekognition.detect_faces(Image=image, Attributes=['ALL'])`; botocore model: FaceDetail has 17 attributes incl. Smile, EyesOpen | yes |
| v07 | Unless there is exactly one, it answers: please upload a picture with only one face. | `rekognition.py` l.37-39: `if len(...['FaceDetails']) != 1: raise ValueError('Please upload a picture with only one face')` -> statusCode 400 | yes; local run: 2 faces and 0 faces both give the 400 (research/handler-run.txt) |
| v08 | One face passes only if it's smiling and its eyes are open. | l.41-49: `if smile['Value'] == True and eyesOpen['Value'] == True: result = 'Good Profile Photo'` | yes; local run |
| v09 | Anything else comes back as a bad profile photo. | l.46: `result = 'Bad Profile Photo'` default, statusCode 200 | yes; local run: not smiling/eyes closed and smiling/eyes closed both give "Bad Profile Photo" |
| v10 | Its role allows three log actions and read-only Rekognition, nothing else. | `lambda.tf`: role `Detection_Lambda_Function_Role` has exactly two attachments: `aws_iam_policy_for_terraform_aws_lambda_role` (logs:CreateLogGroup, logs:CreateLogStream, logs:PutLogEvents on `arn:aws:logs:*:*:*`) and AWS-managed `AmazonRekognitionReadOnlyAccess` | yes (see caution 5) |
| v11 | Fourteen Terraform resources build all of it, and terraform validate passes. | `grep -c '^resource' lambda.tf apigw.tf` = 5 + 9 = 14 (plus 2 data sources); `terraform validate` -> "Success! The configuration is valid." (valid true, 0 errors, 0 warnings) | yes (versions below) |
| v12 | It builds on an AWS example, adding the one-face check and the photo rule. | README "Attribution": scaffolding follows AWS's published example; "The single-face guard and the Smile + EyesOpen classifier are mine." AWS page code matches the handler (docstring, base64 branch, both except blocks, logger lines) | yes (see caution 4) |
| v13 | Serverless profile-photo checker. | name | yes |

131 words, 13 lines.

## On screen

| item | value | source |
|---|---|---|
| stack | AWS Lambda · API Gateway · Amazon Rekognition | README title; repo description |
| internship chip | InternPass research internship · June to July 2025 | README ("June–July 2025"); the internship's commits run from Jun 19 to Jul 12, 2025 |
| client | interact.py; `python interact.py <url> <image>`; base64, requests.post | `interact.py` l.21-24, l.38 usage string |
| client packaging (optional) | Dockerfile python:3.9-slim, requests==2.26.0 | `Dockerfile`, `requirements.txt` |
| request | POST /friendly, JSON `{"image": "<base64>"}` | `apigw.tf` path_part "friendly", http_method POST; `interact.py` payload |
| request size | goodphoto.jpeg = 419,168 bytes = 558,892 base64 characters (badphoto.png 2,605,954 bytes = 3,474,608) | `base64 -i goodphoto.jpeg \| tr -d '\n' \| wc -c`; same count in the harness |
| API | REST API my-api, REGIONAL, authorization NONE, stage dev, us-east-1 | `apigw.tf`; `lambda.tf` provider region |
| permission | AllowExecutionFromAPIGateway, lambda:InvokeFunction, apigateway.amazonaws.com | `apigw.tf` aws_lambda_permission |
| Lambda | Detection_Lambda_Function, handler rekognition.lambda_handler, runtime python3.8 | `lambda.tf` |
| Rekognition call | detect_faces · Attributes ALL; returns FaceDetails | `rekognition.py` l.34-35; botocore model |
| guard chip | len(FaceDetails) != 1 | l.37 |
| rule chip | Smile and EyesOpen · Value true | l.41-48 |
| answers | 200 "Good Profile Photo"; 200 "Bad Profile Photo"; 400 ValueError "Please upload a picture with only one face" | l.46-79; research/handler-run.txt |
| real response JSON | `{"statusCode": 200, "body": "\"Good Profile Photo\""}`; `{"statusCode": 400, "body": {"Error": "ValueError", "ErrorMessage": "Please upload a picture with only one face"}}` | real handler, local run, Rekognition stubbed (research/handler-run.txt) |
| client output | `"Good Profile Photo"` (printed with its JSON quotes); `Error: 400` / `Message: {'Error': 'ValueError', ...}` | real interact.py against a local stand-in (research/cli-run.txt) |
| error log | "Error function <function ARN>: <message>" | l.67-68, l.78-79 (`logger.error`, `context.invoked_function_arn`) |
| role | Detection_Lambda_Function_Role, trust lambda.amazonaws.com (sts:AssumeRole) | `lambda.tf` |
| log actions | logs:CreateLogGroup · logs:CreateLogStream · logs:PutLogEvents | `lambda.tf` aws_iam_policy |
| managed policy | AmazonRekognitionReadOnlyAccess | `lambda.tf` data.aws_iam_policy + attachment |
| 14 resources | Function (5): aws_iam_role, aws_iam_policy, aws_iam_role_policy_attachment x2, aws_lambda_function. API (9): aws_api_gateway_rest_api, _resource, _method, _integration, _method_response, _integration_response, _deployment, _stage, aws_lambda_permission | grep of `^resource`; `terraform graph` (16 nodes = 14 resources + 2 data sources, research/terraform-graph.dot) |
| 163 lines | lambda.tf 74 + apigw.tf 89 | `wc -l` |
| validate | "Success! The configuration is valid." | research/terraform-validate.txt |
| redeploy (optional) | triggers redeployment = sha1(jsonencode([resource, method, integration ids])); create_before_destroy | `apigw.tf` aws_api_gateway_deployment |
| credit rows | "Handler and client scaffolding: AWS's Rekognition + Lambda example"; "Added: the one-face check and the Smile + EyesOpen rule" | README Attribution + the AWS page (handler and client.py) |
| fixtures | goodphoto.jpeg ("fixture that should pass"), badphoto.png ("fixture that should fail"), both 1024 x 1536; AI-generated (shirt text "AI GENERATED PIC") | README Contents; the images; sha256 37c3bd33... / 4fdb0ddd... |
| URL | github.com/andyyaro/serverless-profile-photo-checker | `gh repo view` (PUBLIC), HTTP 200 |

## Verification runs (2026-11-01)

- `terraform validate`: Terraform 1.13.3 darwin_arm64, hashicorp/aws 6.15.0, hashicorp/archive 2.8.1, on a scratch copy of `lambda.tf`, `apigw.tf`, `python/rekognition.py`. The repo pins no provider version; the scratch copy added an override file pinning aws 6.15.0 (`research/harness/zz_pin_override.tf`) so the provider already on disk could be used (its h1 hash matches the hash recorded when it was downloaded from the registry). Result: valid true, 0 errors, 0 warnings. No plan or apply, no credentials (they need AWS).
- Handler: `python/rekognition.py` loaded unchanged; botocore 1.43.123 Stubber answered `detect_faces` (and asserted the call was `Image={'Bytes': <the photo's bytes>}, Attributes=['ALL']`). 7 runs: smile+eyes open -> 200 Good; not smiling+eyes closed -> 200 Bad; smiling+eyes closed -> 200 Bad; 2 faces -> 400; 0 faces -> 400; no `image` key -> 400 "Invalid source. Only image base 64 encoded image bytes are supported."; a stubbed ClientError -> 400 "Couldn't analyze image. ...". These check the code's shapes only: the face attributes were supplied by the stub, so no Rekognition result on the fixtures is known or claimed.
- Client: `interact.py` unchanged, posting to a 127.0.0.1 stand-in that returns the handler's dict as the JSON body (what the type-AWS, non-proxy integration does with the default 200 response).

## Cautions for the build (README vs code)

1. The README's diagram says `POST /`; the code's resource is `/friendly`. The film uses `POST /friendly`.
2. The README's run command (`interact.py --image ... --url "$(terraform output -raw api_url)"`) does not match the code: `interact.py` takes positional `<url> <image>`, and the output is named `deployment_invoke_url`. Do not show the README command; if a command is shown, use `python interact.py <url> goodphoto.jpeg`.
3. The README's table calls the logs policy "inline"; it is a standalone `aws_iam_policy` plus an attachment, and the table leaves out `aws_api_gateway_method_response` and `aws_lambda_permission`. The total of 14 is right.
4. The README credits AWS for the handler scaffolding only. `interact.py` also follows AWS's `client.py` from the same page (argparse with `usage=argparse.SUPPRESS`, `analyze_image`, base64 payload, the `statusCode` branch, the "Error:/Message:" prints), changed from a boto3 Lambda invoke to an HTTP POST. The film credits "handler and client scaffolding".
5. The logs policy allows its 3 actions on `arn:aws:logs:*:*:*` (any log group), so the README's "least-privilege logging policy" and "writing its own logs" are a little generous. The film says "three log actions" and never "least-privilege" or "its own logs".
6. `runtime = "python3.8"` is in the code. The film never claims the stack is deployed or live today; showing "python3.8" on the Lambda card is optional.
7. The Terraform's naming (`terraform_lambda_func`, `zip_the_python_code`, `codedeploy_service_role_policy_attach`) looks tutorial-derived; the README claims the provisioning, not original authorship of every line. The film says "Fourteen Terraform resources build all of it" (true either way) and credits only the one-face check and the rule as added.
8. Rekognition was never called. No confidence values, no "Rekognition said" claims about the fixtures: they appear with the README's own words, "should pass" / "should fail", and the rule decides on screen.
9. `quotes-service/` and the RKE2 cluster are other internship work: not in this film.
10. The README uses em dashes in places; never copy README text with them onto the screen.
