import boto3
import json
from datetime import datetime, timezone

s3 = boto3.client("s3")
BUCKET_NAME = "cloud-security-alert-lamp-ojas"

def lambda_handler(event, context):
    try:
        response = s3.get_public_access_block(
            Bucket=BUCKET_NAME
        )
        config = response.get("PublicAccessBlockConfiguration", {})
    except s3.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
             config = {}
        else:
            raise e

    settings = {
        "Block Public ACLs": config.get("BlockPublicAcls", False),
        "Ignore Public ACLs": config.get("IgnorePublicAcls", False),
        "Block Public Policy": config.get("BlockPublicPolicy", False),
        "Restrict Public Buckets": config.get("RestrictPublicBuckets", False)
    }

    safe = all(settings.values())
    status = "SAFE" if safe else "SECURITY ALERT"

    message = (
        "All four public-access protections are enabled."
        if safe else
        "One or more public-access protections are disabled."
    )

    is_url = bool(event.get("requestContext", {}).get("http"))

    if not is_url:
        result = {
            "alert_status": status,
            "bucket": BUCKET_NAME,
            "message": message,
            "settings": settings
        }
        print(json.dumps(result))
        return result

    lamp_color = "#16a34a" if safe else "#dc2626"
    symbol = "✓" if safe else "!"
    checked_at = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    rows = ""
    for name, enabled in settings.items():
        label = "ENABLED" if enabled else "DISABLED"
        color = "#16a34a" if enabled else "#dc2626"
        rows += f"""
        <div class="setting">
          <span>{name}</span>
          <strong style="color:{color}">{label}</strong>
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta http-equiv="refresh" content="3"> <!-- THIS MAKES IT AUTO-REFRESH EVERY 3 SECONDS -->
      <title>Cloud Security Alert Lamp</title>
      <style>
        * {{ box-sizing: border-box; }}
        body {{
          margin: 0; padding: 30px 16px;
          font-family: Arial, sans-serif;
          background: #0f172a; color: #f8fafc;
        }}
        main {{ max-width: 650px; margin: auto; }}
        h1 {{ text-align: center; font-size: 27px; }}
        .subtitle {{
          text-align: center; color: #cbd5e1; margin-bottom: 28px;
        }}
        .panel {{
          background: #1e293b; border-radius: 18px;
          padding: 25px; margin: 18px 0;
          border: 1px solid #334155;
        }}
        .lamp {{
          width: 115px; height: 115px; border-radius: 50%;
          margin: 10px auto 20px; background: {lamp_color};
          display: flex; align-items: center; justify-content: center;
          font-size: 55px; font-weight: bold;
          box-shadow: 0 0 28px {lamp_color};
        }}
        h2 {{ text-align: center; color: {lamp_color}; }}
        .message {{ text-align: center; line-height: 1.6; }}
        .setting {{
          display: flex; justify-content: space-between;
          gap: 12px; padding: 14px 0;
          border-bottom: 1px solid #334155;
        }}
        .setting:last-child {{ border-bottom: none; }}
        button {{
          display: block; margin: 22px auto 8px;
          padding: 13px 22px; border: none;
          border-radius: 9px; font-size: 16px;
          font-weight: bold; cursor: pointer;
          background: #38bdf8; color: #082f49;
        }}
        .small {{ text-align: center; color: #94a3b8; font-size: 12px; }}
      </style>
    </head>
    <body>
      <main>
        <h1>☁️ CLOUD SECURITY ALERT LAMP</h1>
        <p class="subtitle">S3 Public Access Security Monitor</p>

        <section class="panel">
          <div class="lamp">{symbol}</div>
          <h2>{status}</h2>
          <p class="message">{message}</p>
        </section>

        <section class="panel">
          <h3>Bucket Security Details</h3>
          <p><strong>Bucket:</strong> {BUCKET_NAME}</p>
          <h3>Protection Settings</h3>
          {rows}
        </section>

        <p class="small">Live Monitoring Active - Auto-checking every 3 seconds...</p>
        <p class="small">Last checked: {checked_at}</p>
      </main>
    </body>
    </html>
    """

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html; charset=utf-8",
            "Cache-Control": "no-store"
        },
        "body": html
    }