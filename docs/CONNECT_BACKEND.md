# Connect NOVA's website to a model server

The website has an iPhone-friendly connection setting. Open the
[public NOVA site](https://woutswouts2004-sudo.github.io/Project-NOVA/),
select **About**, and find **Connect a real AI backend**.

Enter your server's HTTPS origin, save it, and tap **Test connection**.
The address is stored in your own browser, not published to GitHub.
Do not enter passwords or API keys into this field.

To run the included server, deploy the repository's `Dockerfile` on
a Docker-compatible cloud host. The `render.yaml` file is an optional
deployment template and is not proof of a live deployment.

Configure the server with secret environment variables:

- `NOVA_PUBLIC_CHAT=YES`
- `NOVA_API_BASE`: compatible model provider's HTTPS API base
- `NOVA_API_KEY`: provider secret, never put in the website
- `NOVA_MODEL`: provider model name
- `NOVA_ENABLE_EXTERNAL_MODEL=YES`
- `NOVA_ALLOWED_ORIGIN=https://woutswouts2004-sudo.github.io`

Check `https://YOUR-SERVER/health` for a JSON response with
`model_connected: true`. The website can then call `/v1/chat`.

**Limits:** The website is public, the API has basic rate limiting only,
and providers may charge for model use. The Docker image does not contain
a trained NOVA conversational model. It calls a separately configured
model service. Hosting availability and free tiers are provider-dependent.

NOVA cannot create accounts or assume legal account ownership without
provider support and the required authorized human setup. Once accounts
are established, delegated access can be designed with restricted
credentials and revocation.
