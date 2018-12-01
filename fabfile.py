import os
from contextlib import contextmanager  
from fabric.api import cd, env, prefix, run, sudo, task, local

# Haricen Postgresql kurulacak

PROJECT_NAME = 'fastermenu'
PROJECT_ROOT = '/opt/%s' % PROJECT_NAME
VENV_DIR = os.path.join(PROJECT_ROOT, 'venv')
REPO = 'git@gitlab.com:fastermenu/fastermenu.git'

env.hosts = ['contact@35.198.165.200']
# Not needed because it've done on server side manually
# env.command_prefixes=["export PRODUCTION='true'",]



@contextmanager
def source_virtualenv():  
    with prefix('source ' + os.path.join(VENV_DIR, 'bin/activate')):
        yield




def restart():  
    sudo('supervisorctl reread')
    sudo('supervisorctl reload')
    sudo('service memcached restart')
    sudo('service nginx restart')


@task
def deploy():
    local('git add .')
    try:
        local("git commit -am 'deploy commit fabfile'")
    except:
        print('No Commit')
    local('git push origin master')
    with cd(PROJECT_ROOT):
        sudo('git pull origin master')
        with source_virtualenv():
            with prefix('export DJANGO_SETTINGS_MODULE={}.settings'.format(PROJECT_NAME)):
                sudo('pip install -r requirements.txt')
                sudo('python manage.py makemigrations')
                sudo('python manage.py migrate')
                sudo('python manage.py createsu') # can be delete
                sudo('python manage.py collectstatic --noinput')

    restart()


@task
def bootstrap():
    sudo('apt update')
    sudo('apt upgrade')
    sudo('apt install git supervisor nginx memcached postgresql python3-dev python-pip python-virtualenv')
    # run("export LC_ALL='en_US.UTF-8'")
    # run("export LC_CTYPE='en_US.UTF-8'")

    remove()

    sudo('mkdir -p {}'.format(PROJECT_ROOT))
    sudo('mkdir -p /root/logs/')
    sudo('touch /root/logs/gunicorn_supervisor.log')
    sudo('git clone {} {}'.format(REPO, PROJECT_ROOT))

    sudo('chmod +x /opt/{}/{}/conf/gunicorn'.format(PROJECT_NAME, PROJECT_NAME))

    with cd(PROJECT_ROOT):
        sudo('virtualenv -p python3 venv')
        # run('rm {}/bin/postactivate'.format(os.path.join(VENV_DIR)))
        sudo('ln -s {}/{}/conf/postactivate {}/bin/postactivate'.format(PROJECT_ROOT, PROJECT_NAME, os.path.join(VENV_DIR)))
        with source_virtualenv():
            with prefix('export DJANGO_SETTINGS_MODULE={}.settings'.format(PROJECT_NAME)):
                sudo('pip install -r requirements.txt')
                sudo('python manage.py makemigrations')
                sudo('python manage.py migrate')
                sudo('python manage.py createsu')
                sudo('python manage.py collectstatic --noinput')


    # Deploy web and app server configs
    sudo('ln -s {}/{}/conf/supervisor.conf /etc/supervisor/conf.d/supervisor.conf'.format(PROJECT_ROOT, PROJECT_NAME))
    sudo('ln -s {}/{}/conf/nginx.conf /etc/nginx/sites-enabled/{}.conf'.format(PROJECT_ROOT, PROJECT_NAME, PROJECT_NAME))

    restart()


@task
def remove():
    sudo('supervisorctl stop {}'.format(PROJECT_NAME))
    sudo('service nginx stop')
    sudo('rm -f /root/logs/*')
    sudo('rm -rf {}'.format(PROJECT_ROOT))
    sudo('rm -f /etc/supervisor/conf.d/supervisor.conf')
    sudo('rm -f /etc/nginx/sites-enabled/{}.conf'.format(PROJECT_NAME))
