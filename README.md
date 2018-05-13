# Lektor Netlify Publisher Plugin

Publish your [Lektor](https://www.getlektor.com/) site to [Netlify](https://www.netlify.com/).

## Installation

Install the `netlify` command-line program according to [the instructions on netlify.com](https://www.netlify.com/docs/cli).

Add lektor-netlify to your project from the command line:

```shell
lektor plugins add lektor-netlify
```

See [the Lektor documentation for more instructions on installing plugins](https://www.getlektor.com/docs/plugins/).

## Configuration

Configure a server in your `.lektorproject` file:

```ini
[servers.production]
name = Production
target = netlify://my-domain.com
```

## Access Token

Get a personal access token from Netlify's "applications" page:

* [Applications](https://app.netlify.com/applications)

You must use this access token each time you publish. **If your project file is private** you can save the token there. Do not commit this!

```ini
[servers.production]
name = Production
target = netlify://my-domain.com
key = ACCESS_TOKEN
```

Now deploy your site like:

```shell
lektor deploy production
```

Otherwise, pass the token on the command line:

```shell
lektor deploy production --key ACCESS_TOKEN    
```
