# Infra

Infrastructure lives in azure and is managed by runiac and terraform.

- [Runiac](https://runiac.io)
- [Terraform](https://terraform.io)
- [Azure](https://portal.azure.com)

## Running Locally

### Developer local environment (ephemeral)

```bash
runiac deploy -a 8a8f04fc-cf3d-433f-972a-5ff0e8615f54 -e dev --local
```
The `--local` flag will create an instance of the dev environment (`-e`) specific to your machine.

```bash
runiac deploy -a 8a8f04fc-cf3d-433f-972a-5ff0e8615f54 -e dev --local --self-destroy
```

The `--self-destroy` will tear down the environment

> IMPORTANT: specify `--local` when tearing down local environment to avoid destroying real dev

### Verifying changes to be done to environment
```bash
runiac deploy -a 8a8f04fc-cf3d-433f-972a-5ff0e8615f54 -e dev --container optumopensource/runiac:v0.0.3-alpine-azure --dry-run
```