from fabric.api import *

env.keepalive = True
env.hosts = ('173.255.249.6', )
env.user = 'wolf'
env.path = '/home/victor/Proyectos/jvacx.com'


def push():
    """Deploy current mas ter branch in the repo"""
    local('hg push jvacx')

def update(rev='default'):
    with cd(env.path):
        run("hg update %s -C " % rev)

def install():
    with cd(env.path):
      run('make install')

def deploy():
    push()
    update()
    install()