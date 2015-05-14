import os, sys
import subprocess
from optparse import OptionParser

here = os.getcwd()
bootstrap_file_default = os.path.join(here, 'scripts/vagrant-bootstrap.sh')

parser = OptionParser()

parser.add_option('--bootstrap-file', type='string', action='store',
                  dest='bootstrap_file', default=bootstrap_file_default)
parser.add_option('--dist', type='string', action='store',
                  dest='dist', default='jessie')
parser.add_option('--arch', type='string', action='store',
                  dest='arch', default='')
parser.add_option('--proxy', type='string', action='store',
                  dest='proxy', default='')
parser.add_option('--chroot', type='string', action='store',
                  dest='chroot', default='')


opts, args = parser.parse_args(sys.argv[1:])
if not opts.chroot:
    opts.chroot = os.path.basename(args[0])
    

def check_requirements():
    if not os.path.isfile(opts.bootstrap_file):
        msg = "Please run this script from the project directory."
        raise RuntimeError, msg
        
    binaries = ['/usr/bin/rsync', '/usr/sbin/debootstrap',
                '/usr/bin/schroot']
    for b in binaries:
        if not os.path.isfile(b):
            basename = os.path.basename(b)
            raise RuntimeError, "Please run apt-get install %s" % basename


def make_root_filesystem(dest, dist=opts.dist):
    cmd = ['debootstrap', dist, dest]
    if opts.proxy:
        cmd = ['/usr/bin/env', 'http_proxy=%s' % opts.proxy] + cmd
    retval = subprocess.check_call(cmd)
    if opts.proxy:
        filename = os.path.join(dest, 'etc/apt/apt.conf.d/02proxy')
        with file(filename, 'w') as aconf:
            aconf.write('Acquire::http::Proxy "%s";\n' % opts.proxy)

def bootstrap_salt(dest):
    prefix = ['schroot', '-c', opts.chroot, '-u', 'root']
    if opts.proxy:
        prefix += ['/usr/bin/env', 'http_proxy=%s' % opts.proxy]
    cmd = prefix + ['bash', opts.bootstrap_file]
    subprocess.check_call(cmd)

def prepare_salt_directories(dest):
    destsrv = os.path.join(dest, 'srv/')
    if not os.path.isdir(destsrv):
        raise RuntimeError, "%s doesn't exist" % destsrv
    here = os.getcwd()
    salt_roots = os.path.join(here, 'salt/roots/')
    cmd = ['rsync', '-avHX', salt_roots, destsrv]
    subprocess.check_call(cmd)
    
def install_minion_config(dest):
    minion_config = os.path.join(here, 'salt/minion')
    destsaltdir = os.path.join(dest, 'etc/salt')
    if not os.path.isdir(destsaltdir):
        os.mkdir(destsaltdir)
    cmd = ['cp', minion_config, destsaltdir]
    subprocess.check_call(cmd)
    
def provision_webdev(dest):
    prefix = ['schroot', '-c', opts.chroot, '-u', 'root']
    #if opts.proxy:
    #    prefix += ['/usr/bin/env', 'http_proxy=%s' % opts.proxy]
    cmd = prefix + ['salt-call', 'state.highstate']
    subprocess.check_call(cmd)
    
def main(dest): 
    #if opts.proxy:
    #    os.environ['http_proxy'] = opts.proxy
    if os.getuid():
        raise RuntimeError, "This script needs root permissions."
    check_requirements()
    if not os.path.isdir(dest):
        make_root_filesystem(dest)
    if os.path.isdir(os.path.join(dest, 'debootstrap')):
        raise RuntimeError, "Try running debootstrap again"
    bootstrap_salt(dest)
    prepare_salt_directories(dest)
    install_minion_config(dest)
    provision_webdev(dest)
    
    
                     
    

            
if __name__ == '__main__':
    dest = args[0]
    main(dest)
    
    
    
    
