# -*- coding: utf-8 -*-
import click
import os
import requests
import shutil
from lektor.pluginsystem import Plugin
from lektor.publisher import Publisher, Command
from lektor.utils import slugify, bool_from_string
from werkzeug import urls


class NetlifyPublisher(Publisher):
    def publish(self, target_url, credentials=None, server_info=None, **extra):
        draft = '--draft' in click.get_current_context().args
        host = target_url.host

        if credentials and credentials.get('key'):
            access_token = credentials['key']
        elif server_info and server_info.extra.get('key'):
            access_token = server_info.extra['key']
        elif os.environ.get('LEKTOR_DEPLOY_KEY'):
            access_token = os.environ.get('LEKTOR_DEPLOY_KEY')
        else:
            raise RuntimeError(
                "Use lektor deploy --key <ACCESS_TOKEN>,"
                " see https://github.com/ajdavis/lektor-netlify/README.md")
        
        redirects_content = os.path.join(self.env.root_path, 'content', '_redirects')
        redirects_build = os.path.join(self.output_path, '_redirects')
        if os.path.isfile(redirects_content):
            shutil.copy2(redirects_content, redirects_build)

        sites_url = (
            'https://api.netlify.com/api/v1/sites?access_token=' +
            access_token)

        response = requests.get(
            sites_url,
            headers={'User-Agent': 'https://github.com/ajdavis/lektor-netlify'})

        response.raise_for_status()
        j = response.json()
        for site in j:
            site_url = urls.url_parse(unicode(site['url']))
            if site_url.host == host:
                site_id = site['site_id']
                break
        else:
            site_name = slugify(host).replace('.', '-')
            force_ssl = bool_from_string(server_info.extra.get('force_ssl'),
                                         default=False)

            print('Creating new Netlify site "%s" at %s' % (site_name, host))
            response = requests.post(sites_url, {
                'name': site_name,
                'custom_domain': host,
                'force_ssl': force_ssl})
            response.raise_for_status()
            site_id = response.json()['site_id']

        cmd = [
            'netlify',
            '-t', access_token,
            'deploy',
            '-s', site_id,
            '-p', self.output_path]

        if draft:
            yield "Deploying as draft"
            cmd.append('--draft')

        for line in Command(cmd):
            yield line


class NetlifyPlugin(Plugin):
    name = u'Netlify'
    description = u'Publishes your Lektor site with Netlify.'

    def on_setup_env(self, **extra):
        try:
            # Lektor 2.0+.
            self.env.add_publisher('netlify', NetlifyPublisher)
        except AttributeError:
            # Lektor 1.0.
            from lektor.publisher import publishers
            publishers['netlify'] = NetlifyPublisher
