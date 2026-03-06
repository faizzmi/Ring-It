"""
app/core/email.py
Async email service using Gmail SMTP (or any SMTP provider).
Uses Python's built-in smtplib wrapped in asyncio.run_in_executor
so it never blocks the event loop.

ENV vars required:
  SMTP_HOST       = smtp.gmail.com
  SMTP_PORT       = 587
  SMTP_USER       = yourapp@gmail.com
  SMTP_PASSWORD   = <Gmail App Password — NOT your real password>
  EMAIL_FROM_NAME = Ring-It Vault
  FRONTEND_URL    = https://yourapp.com   (for verification link)
"""
import asyncio
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import partial

from app.core.config import settings


# ── HTML email templates ──────────────────────────────────────────────────────

def _verification_html(full_name: str, verify_url: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Verify Your Vault</title>
</head>
<body style="margin:0;padding:0;background:#080808;font-family:'DM Sans',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#080808;padding:48px 20px;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0"
             style="background:#121214;border:1px solid rgba(224,224,224,0.08);
                    border-radius:12px;overflow:hidden;max-width:560px;width:100%;">

        <!-- Header bar -->
        <tr>
          <td style="background:rgba(128,0,32,0.15);border-bottom:1px solid rgba(128,0,32,0.3);
                     padding:20px 32px;text-align:left;">
            <span style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:3px;
                         color:rgba(224,224,224,0.5);text-transform:uppercase;">
              ● RING-IT VAULT
            </span>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:40px 32px;">
            <h1 style="font-size:26px;font-weight:800;letter-spacing:-0.03em;
                       color:#E0E0E0;margin:0 0 8px;">
              Verify Your Vault
            </h1>
            <p style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:2px;
                      color:#757575;text-transform:uppercase;margin:0 0 28px;">
              // EMAIL CONFIRMATION REQUIRED
            </p>
            <p style="font-size:14px;color:rgba(224,224,224,0.7);line-height:1.75;margin:0 0 12px;">
              Hi {full_name},
            </p>
            <p style="font-size:14px;color:rgba(224,224,224,0.7);line-height:1.75;margin:0 0 32px;">
              Your Ring-It vault has been created. Click the button below to verify your email
              address and unlock full access to your behavioral wealth system.
            </p>

            <!-- CTA Button -->
            <table cellpadding="0" cellspacing="0" style="margin:0 0 32px;">
              <tr>
                <td style="background:rgba(128,0,32,0.88);border:1px solid rgba(128,0,32,0.65);
                           border-radius:6px;box-shadow:0 4px 18px rgba(128,0,32,0.28);">
                  <a href="{verify_url}"
                     style="display:inline-block;padding:14px 32px;
                            font-family:'DM Mono',monospace;font-size:11px;font-weight:500;
                            letter-spacing:1.5px;text-transform:uppercase;
                            color:rgba(224,224,224,0.95);text-decoration:none;">
                    VERIFY EMAIL &rarr;
                  </a>
                </td>
              </tr>
            </table>

            <p style="font-size:11px;color:#757575;line-height:1.6;margin:0 0 8px;">
              Or copy this link into your browser:
            </p>
            <p style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(128,0,32,0.8);
                      word-break:break-all;margin:0 0 32px;">
              {verify_url}
            </p>

            <div style="border-top:1px solid rgba(224,224,224,0.06);padding-top:24px;">
              <p style="font-size:11px;color:#757575;line-height:1.6;margin:0;">
                This link expires in <strong style="color:rgba(224,224,224,0.5);">24 hours</strong>.
                If you did not create an account, you can safely ignore this email.
              </p>
            </div>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:rgba(8,8,8,0.5);border-top:1px solid rgba(224,224,224,0.06);
                     padding:20px 32px;text-align:center;">
            <span style="font-family:'DM Mono',monospace;font-size:8px;letter-spacing:2px;
                         color:#757575;text-transform:uppercase;">
              AES-256 · PDPA 2010 · BNM RMIT · NO ADS · NO DATA SELLING
            </span>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""


def _welcome_html(full_name: str, dashboard_url: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/><title>Welcome to Ring-It</title></head>
<body style="margin:0;padding:0;background:#080808;font-family:'DM Sans',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#080808;padding:48px 20px;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0"
             style="background:#121214;border:1px solid rgba(224,224,224,0.08);
                    border-radius:12px;overflow:hidden;max-width:560px;width:100%;">
        <tr>
          <td style="background:rgba(76,175,80,0.08);border-bottom:1px solid rgba(76,175,80,0.2);
                     padding:20px 32px;">
            <span style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:3px;
                         color:rgba(76,175,80,0.7);text-transform:uppercase;">
              ✓ VAULT ACTIVATED
            </span>
          </td>
        </tr>
        <tr>
          <td style="padding:40px 32px;">
            <h1 style="font-size:26px;font-weight:800;letter-spacing:-0.03em;color:#E0E0E0;margin:0 0 28px;">
              Your Vault Is Live.
            </h1>
            <p style="font-size:14px;color:rgba(224,224,224,0.7);line-height:1.75;margin:0 0 24px;">
              Welcome, {full_name}. Your behavioral wealth system is ready.
              Everything is encrypted, private, and built to last.
            </p>
            <table cellpadding="0" cellspacing="0" style="margin:0 0 32px;">
              <tr>
                <td style="background:rgba(128,0,32,0.88);border:1px solid rgba(128,0,32,0.65);border-radius:6px;">
                  <a href="{dashboard_url}"
                     style="display:inline-block;padding:14px 32px;
                            font-family:'DM Mono',monospace;font-size:11px;
                            letter-spacing:1.5px;text-transform:uppercase;
                            color:rgba(224,224,224,0.95);text-decoration:none;">
                    OPEN VAULT &rarr;
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="background:rgba(8,8,8,0.5);border-top:1px solid rgba(224,224,224,0.06);
                     padding:20px 32px;text-align:center;">
            <span style="font-family:'DM Mono',monospace;font-size:8px;letter-spacing:2px;
                         color:#757575;text-transform:uppercase;">
              AES-256 · PDPA 2010 · BNM RMIT · NO ADS · NO DATA SELLING
            </span>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
"""


# ── SMTP sender (runs in thread pool — non-blocking) ──────────────────────────

def _send_smtp_sync(to_email: str, subject: str, html_body: str) -> None:
    """Blocking SMTP send — called via run_in_executor."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.SMTP_USER}>"
    msg["To"] = to_email
    msg.attach(MIMEText(html_body, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.ehlo()
        server.starttls(context=context)
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.sendmail(settings.SMTP_USER, to_email, msg.as_string())


async def send_email(to_email: str, subject: str, html_body: str) -> None:
    """Non-blocking email send — wraps SMTP in thread pool."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        partial(_send_smtp_sync, to_email, subject, html_body),
    )


# ── Convenience senders ───────────────────────────────────────────────────────

async def send_verification_email(to_email: str, full_name: str, token: str) -> None:
    verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    await send_email(
        to_email=to_email,
        subject="[Ring-It] Verify your vault email",
        html_body=_verification_html(full_name, verify_url),
    )


async def send_welcome_email(to_email: str, full_name: str) -> None:
    dashboard_url = f"{settings.FRONTEND_URL}/dashboard"
    await send_email(
        to_email=to_email,
        subject="[Ring-It] Your vault is live",
        html_body=_welcome_html(full_name, dashboard_url),
    )

def _password_reset_html(full_name: str, reset_url: str) -> str:
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Reset Your Password</title>
</head>
<body style="margin:0;padding:0;background:#080808;font-family:'DM Sans',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#080808;padding:48px 20px;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0"
             style="background:#121214;border:1px solid rgba(224,224,224,0.08);
                    border-radius:12px;overflow:hidden;max-width:560px;width:100%;">
        <tr>
          <td style="background:rgba(128,0,32,0.15);border-bottom:1px solid rgba(128,0,32,0.3);
                     padding:20px 32px;text-align:left;">
            <span style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:3px;
                         color:rgba(224,224,224,0.5);text-transform:uppercase;">
              ● RING-IT VAULT
            </span>
          </td>
        </tr>
        <tr>
          <td style="padding:40px 32px;">
            <h1 style="font-size:26px;font-weight:800;letter-spacing:-0.03em;color:#E0E0E0;margin:0 0 8px;">
              Reset Your Password
            </h1>
            <p style="font-family:'DM Mono',monospace;font-size:9px;letter-spacing:2px;
                      color:#757575;text-transform:uppercase;margin:0 0 28px;">
              // PASSWORD RESET REQUEST
            </p>
            <p style="font-size:14px;color:rgba(224,224,224,0.7);line-height:1.75;margin:0 0 12px;">
              Hi {full_name},
            </p>
            <p style="font-size:14px;color:rgba(224,224,224,0.7);line-height:1.75;margin:0 0 32px;">
              We received a request to reset your vault password. Click the button below —
              this link expires in <strong style="color:rgba(224,224,224,0.5);">1 hour</strong>.
            </p>
            <table cellpadding="0" cellspacing="0" style="margin:0 0 32px;">
              <tr>
                <td style="background:rgba(128,0,32,0.88);border:1px solid rgba(128,0,32,0.65);
                           border-radius:6px;box-shadow:0 4px 18px rgba(128,0,32,0.28);">
                  <a href="{reset_url}"
                     style="display:inline-block;padding:14px 32px;
                            font-family:'DM Mono',monospace;font-size:11px;font-weight:500;
                            letter-spacing:1.5px;text-transform:uppercase;
                            color:rgba(224,224,224,0.95);text-decoration:none;">
                    RESET PASSWORD &rarr;
                  </a>
                </td>
              </tr>
            </table>
            <p style="font-size:11px;color:#757575;line-height:1.6;margin:0 0 8px;">
              Or copy this link into your browser:
            </p>
            <p style="font-family:'DM Mono',monospace;font-size:10px;color:rgba(128,0,32,0.8);
                      word-break:break-all;margin:0 0 32px;">
              {reset_url}
            </p>
            <div style="border-top:1px solid rgba(224,224,224,0.06);padding-top:24px;">
              <p style="font-size:11px;color:#757575;line-height:1.6;margin:0;">
                If you did not request a password reset, you can safely ignore this email.
                Your vault remains secure.
              </p>
            </div>
          </td>
        </tr>
        <tr>
          <td style="background:rgba(8,8,8,0.5);border-top:1px solid rgba(224,224,224,0.06);
                     padding:20px 32px;text-align:center;">
            <span style="font-family:'DM Mono',monospace;font-size:8px;letter-spacing:2px;
                         color:#757575;text-transform:uppercase;">
              AES-256 · PDPA 2010 · BNM RMIT · NO ADS · NO DATA SELLING
            </span>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>
"""

async def send_password_reset_email(to_email: str, full_name: str, token: str) -> None:
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    await send_email(
        to_email=to_email,
        subject="[Ring-It] Reset your vault password",
        html_body=_password_reset_html(full_name, reset_url),
    )
