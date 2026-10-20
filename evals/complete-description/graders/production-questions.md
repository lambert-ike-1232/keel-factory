---
# At least three of the five production topics appear in the reply. A regex can't
# count distinct topics, so the pattern lists the ten ways to pick three of five, each
# as three lookaheads. Flags: i (case), s (dot matches newline). The topics, in order:
#   deploy: deploy|hosting|hosted|self-host|vercel|netlify|fly[.]io|railway|heroku|render[.]com
#   auth: auth[^o]|authoriz|magic link|passkey|password|[^a-z]log[ -]?in[^a-z]|[^a-z]sign[ -]?in[^a-z]|sign-on|sign up
#   secrets: secret|credential|api key|env var|environment variable|[.]env[^a-z]|vault|key management
#   retention: retention|retain|backup|back[ -]up|purg|gdpr|account deletion|data export
#   observability: observab|monitor|logging[^ ]|[^a-z]logs[^a-z]|error tracking|error reporting|sentry|telemetry|uptime
# Change a topic by editing it in all six lines that use it. Scored in both arms.
type: regex
target: last_message
flags: is
pattern: "^(?:\
  (?=.*?(?:deploy|hosting|hosted|self-host|vercel|netlify|fly[.]io|railway|heroku|render[.]com))(?=.*?(?:auth[^o]|authoriz|magic link|passkey|password|[^a-z]log[ -]?in[^a-z]|[^a-z]sign[ -]?in[^a-z]|sign-on|sign up))(?=.*?(?:secret|credential|api key|env var|environment variable|[.]env[^a-z]|vault|key management))|\
  (?=.*?(?:deploy|hosting|hosted|self-host|vercel|netlify|fly[.]io|railway|heroku|render[.]com))(?=.*?(?:auth[^o]|authoriz|magic link|passkey|password|[^a-z]log[ -]?in[^a-z]|[^a-z]sign[ -]?in[^a-z]|sign-on|sign up))(?=.*?(?:retention|retain|backup|back[ -]up|purg|gdpr|account deletion|data export))|\
  (?=.*?(?:deploy|hosting|hosted|self-host|vercel|netlify|fly[.]io|railway|heroku|render[.]com))(?=.*?(?:auth[^o]|authoriz|magic link|passkey|password|[^a-z]log[ -]?in[^a-z]|[^a-z]sign[ -]?in[^a-z]|sign-on|sign up))(?=.*?(?:observab|monitor|logging[^ ]|[^a-z]logs[^a-z]|error tracking|error reporting|sentry|telemetry|uptime))|\
  (?=.*?(?:deploy|hosting|hosted|self-host|vercel|netlify|fly[.]io|railway|heroku|render[.]com))(?=.*?(?:secret|credential|api key|env var|environment variable|[.]env[^a-z]|vault|key management))(?=.*?(?:retention|retain|backup|back[ -]up|purg|gdpr|account deletion|data export))|\
  (?=.*?(?:deploy|hosting|hosted|self-host|vercel|netlify|fly[.]io|railway|heroku|render[.]com))(?=.*?(?:secret|credential|api key|env var|environment variable|[.]env[^a-z]|vault|key management))(?=.*?(?:observab|monitor|logging[^ ]|[^a-z]logs[^a-z]|error tracking|error reporting|sentry|telemetry|uptime))|\
  (?=.*?(?:deploy|hosting|hosted|self-host|vercel|netlify|fly[.]io|railway|heroku|render[.]com))(?=.*?(?:retention|retain|backup|back[ -]up|purg|gdpr|account deletion|data export))(?=.*?(?:observab|monitor|logging[^ ]|[^a-z]logs[^a-z]|error tracking|error reporting|sentry|telemetry|uptime))|\
  (?=.*?(?:auth[^o]|authoriz|magic link|passkey|password|[^a-z]log[ -]?in[^a-z]|[^a-z]sign[ -]?in[^a-z]|sign-on|sign up))(?=.*?(?:secret|credential|api key|env var|environment variable|[.]env[^a-z]|vault|key management))(?=.*?(?:retention|retain|backup|back[ -]up|purg|gdpr|account deletion|data export))|\
  (?=.*?(?:auth[^o]|authoriz|magic link|passkey|password|[^a-z]log[ -]?in[^a-z]|[^a-z]sign[ -]?in[^a-z]|sign-on|sign up))(?=.*?(?:secret|credential|api key|env var|environment variable|[.]env[^a-z]|vault|key management))(?=.*?(?:observab|monitor|logging[^ ]|[^a-z]logs[^a-z]|error tracking|error reporting|sentry|telemetry|uptime))|\
  (?=.*?(?:auth[^o]|authoriz|magic link|passkey|password|[^a-z]log[ -]?in[^a-z]|[^a-z]sign[ -]?in[^a-z]|sign-on|sign up))(?=.*?(?:retention|retain|backup|back[ -]up|purg|gdpr|account deletion|data export))(?=.*?(?:observab|monitor|logging[^ ]|[^a-z]logs[^a-z]|error tracking|error reporting|sentry|telemetry|uptime))|\
  (?=.*?(?:secret|credential|api key|env var|environment variable|[.]env[^a-z]|vault|key management))(?=.*?(?:retention|retain|backup|back[ -]up|purg|gdpr|account deletion|data export))(?=.*?(?:observab|monitor|logging[^ ]|[^a-z]logs[^a-z]|error tracking|error reporting|sentry|telemetry|uptime)))"
---
