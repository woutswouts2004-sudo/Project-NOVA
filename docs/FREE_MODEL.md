# First real model: Groq Free Plan

This is an **optional** provider recommendation, not an active connection.

Groq documents an OpenAI-compatible chat-completions API:
`https://api.groq.com/openai/v1`

Its Free Plan is documented as non-billable: exceeding the free rate
limit returns an HTTP 429 error rather than charging the account.
**Confirm your account is still on the Free Plan before use.**
Provider terms, model IDs and limits may change.

Sources:
- https://console.groq.com/docs/openai
- https://console.groq.com/docs/rate-limits
- https://community.groq.com/t/do-i-get-charged-for-anything-on-the-groq-free-plan/832

## Account step (must be completed by account holder)
1. Create or sign into a GroqCloud account at https://console.groq.com/.
2. Verify the account remains on the Free Plan.
3. Create a key at https://console.groq.com/keys.
4. Store the key in the future host's secret manager. Never paste it into a
   GitHub source file, public issue, screenshot, or chat message.
5. Check the provider's Models and Limits pages for a currently available
   free model, for example `openai/gpt-oss-20b` if still supported.

## Environment variables
```sh
NOVA_API_BASE=https://api.groq.com/openai/v1
NOVA_MODEL=openai/gpt-oss-20b
NOVA_API_KEY=<stored-in-secret-manager>
NOVA_ENABLE_EXTERNAL_MODEL=YES
```

Once a permitted runtime and secret store are configured, a test command is:
`python -m project_nova --ask "What would you like to explore?"`

If the model responds, the journal will record the interaction.
If rate-limited, the request fails; the program does not automatically
upgrade an account or retry without bounds.

## Important privacy tradeoff
Provider inference transmits the prompt and some journal history to
the model provider. Do not send sensitive personal information.
Review the provider's data processing and retention policies before
sending anything confidential.

## Hosting is separate
Groq supplies model inference, not a free always-on Python server for
this repository. Continuous operation still needs a host with
persistent storage and independent account controls.
