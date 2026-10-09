# Install NOVA from an iPhone (Oracle Always Free ARM)

These steps assume an authorized Oracle Cloud account and an Always
Free ARM instance running Ubuntu. Never share credentials, SSH private
keys, or payment details with NOVA or in GitHub issues.

1. Sign up at https://signup.oraclecloud.com and complete email,
   phone and payment verification as required.
2. In OCI Console choose **Compute > Instances > Create instance**.
   Choose Ubuntu ARM64, shape `VM.Standard.A1.Flex`, 2 OCPUs and
   12 GB RAM, and verify the **Always Free eligible** label. Select a
   public subnet with public IPv4. Oracle capacity may be unavailable.
3. For SSH, generate an Ed25519 key in an iOS SSH client such as
   Termius, paste its **public** key into the instance creation SSH
   field, and save the private key securely on your iPhone.
   Alternatively use OCI's generated key and import the downloaded
   private key into your SSH client. Never publish the private key.
4. After instance creation, note its public IPv4. Connect using
   your SSH app to that address, port 22, username `ubuntu`,
   and the matching SSH key. Ensure OCI network rules permit SSH
   from your IP; avoid opening SSH to the entire internet if possible.
5. In the SSH terminal, run:

```sh
curl -fsSL https://raw.githubusercontent.com/woutswouts2004-sudo/Project-NOVA/main/scripts/install_oracle_arm.sh -o install_nova.sh
less install_nova.sh
bash install_nova.sh
```

6. Verify with:

```sh
cd ~/Project-NOVA
sudo docker compose -f compose.live.yaml ps
sudo docker compose -f compose.live.yaml logs --tail=40 worker
curl http://127.0.0.1:8080/health
```

The first model download can take time. The chat API listens on VM
loopback only. **Do not open port 8080 directly to the public internet.**
A secure HTTPS reverse proxy or tunnel must be configured before
the GitHub Pages website can connect to this server.

This is a real continuously running process **while Oracle keeps the
VM available**, not a guarantee of uninterrupted uptime. Oracle may
reclaim idle Always Free instances. Model speed and RAM must be tested
on the actual instance. Cloud resources, SSH credentials, and public
HTTPS cannot be created by the installation script alone.
