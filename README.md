Project Title
Cloud Security Alert Lamp: Real-Time S3 Public Access Monitoring & Web Alert Dashboard

Abstract / Overview
Accidental public exposure of Amazon S3 buckets is one of the most common cloud security vulnerabilities. The Cloud Security Alert Lamp is a serverless, real-time cloud security auditing application built on AWS. It continuously inspects the target S3 bucket (cloud-security-alert-lamp-ojas) for public access misconfigurations and displays a live visual "Alert Lamp" indicator on a responsive web dashboard hosted via AWS Lambda Function URL.

How It Works (Architecture)
Target Cloud Resource (Amazon S3): Monitors the S3 bucket cloud-security-alert-lamp-ojas (us-east-1) across all four S3 Public Access Block controls:

Block Public ACLs

Ignore Public ACLs

Block Public Policy

Restrict Public Buckets

Serverless Security Auditor (AWS Lambda): A Python 3.14 function using the AWS SDK (boto3) queries s3.get_public_access_block() to verify whether all four security flags are active.

Live Web Alert Dashboard (Lambda Function URL): Exposed via an HTTPS endpoint (Live Dashboard Link), the Lambda function renders an HTML/CSS/JavaScript web interface (Cache-Control: no-store) that acts as a virtual security lamp:

SAFE State (Green): Displayed when all four public-access protections are enabled.

SECURITY ALERT State (Flashing Red): Triggered immediately when one or more public-access protections are disabled or missing (NoSuchPublicAccessBlockConfiguration).

Automated Notifications (Amazon SNS): Dispatches alert notifications to subscribed administrators whenever a public exposure event is detected.

Technology Stack
Cloud Storage: Amazon S3

Serverless Compute & Hosting: AWS Lambda (Python 3.14) + Lambda Function URL

SDK & Libraries: boto3, json, datetime

Frontend: HTML5, CSS3, JavaScript (served dynamically by Lambda)

Alerting: Amazon SNS (Simple Notification Service)

Demonstration Workflow
Normal State: Open the Lambda Function URL in a browser—the virtual alert lamp shows green (SAFE).

Simulate Misconfiguration: Open Amazon S3, select cloud-security-alert-lamp-ojas, go to Permissions, and turn OFF Block all public access.

Live Detection: Refresh or let the dashboard poll—the virtual lamp immediately switches to a red SECURITY ALERT state highlighting the exact disabled security flags.

Remediation: Re-enable Block all public access in S3, and the dashboard automatically returns to SAFE.