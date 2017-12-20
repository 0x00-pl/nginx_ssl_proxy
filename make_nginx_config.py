import os

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

def main(base_dir, localhost):
  path = gen_cert_chain(base_dir)
  template = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ssl_proxy.example')).read()
  conf = get_file(template, path, localhost)
  print(conf)

if __name__ == '__main__':
  main(os.getcwd(), 'http://localhost:8080')
