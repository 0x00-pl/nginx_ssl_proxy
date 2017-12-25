import os
import json

cwd = os.path.dirname(os.path.realpath(__file__))

def get_file(template, cert_key_path, localhost, server_name='~^.*$'):
  template = template.replace('{{cert_chain.crt}}', cert_key_path[0])
  template = template.replace('{{private.key}}', cert_key_path[1])
  template = template.replace('{{localhost:port}}', localhost)
  template = template.replace('{{server_name}}', server_name)
  return template

def gen_cert_chain(base_dir):
  os.chdir(base_dir)
  os.system("paste -sd'\\n' certificate.crt ca_bundle.crt > cert_chain.crt")
  cwd = os.getcwd()
  path = [os.path.join(cwd, 'cert_chain.crt'), os.path.join(cwd, 'private.key')]
  return path

def main(base_dir, localhost, site_name):
  path = gen_cert_chain(base_dir)
  print(__file__)
  print(os.path.realpath(__file__))
  template = open(os.path.join(cwd, 'ssl_proxy.example')).read()
  conf = get_file(template, path, localhost, site_name)
  print(conf)

def load_config():
  dep_path = os.path.join(cwd, 'deployment_config')
  dep_conf_path = os.path.join(dep_path, 'ssl_proxy.json')
  j = {
    'ssl_path': os.path.join(dep_path, 'sslforfree'),
    'site_name': '~^.*$',
    'proxy_url': 'http://localhost:8080'
  }
  try:
    fj = json.load(open(dep_conf_path))
    j["ssl_path"] = fj.get("ssl_path", j["ssl_path"])
    j["site_name"] = fj.get("site_name", j["site_name"])
    j["proxy_url"] = fj.get("proxy_url", j["proxy_url"])
  except e:
    pass

  return j

if __name__ == '__main__':
  conf = load_config()
  main(conf["ssl_path"], conf["proxy_url"], conf["site_name"])
