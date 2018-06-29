import os
from contextlib import contextmanager  
from fabric.api import cd, env, prefix, run, sudo, task, local

# Haricen Postgresql kurulacak

PROJECT_NAME = 'fastermenu'
PROJECT_ROOT = '/opt/%s' % PROJECT_NAME
VENV_DIR = os.path.join(PROJECT_ROOT, 'venv')
REPO = 'https://kaaninan@github.com/kaaninan/%s.git' % PROJECT_NAME

env.hosts = ['root@46.101.151.145']



@contextmanager
def source_virtualenv():  
    with prefix('source ' + os.path.join(VENV_DIR, 'bin/activate')):
        yield


def clean():  
    """Cleans Python bytecode"""
    sudo('find . -name \'*.py?\' -exec rm -rf {} \;')



def restart():  
    sudo('supervisorctl reread')
    sudo('supervisorctl reload')
    sudo('service memcached restart')
    sudo('service nginx restart')


@task
def deploy():
    local('git add .')
    try:
        local("git commit -am 'deploy commit'")
    except:
        print('No Commit')
    local('git push origin master')
    with cd(PROJECT_ROOT):
        run('git pull origin master')
        with source_virtualenv():
            with prefix('export DJANGO_SETTINGS_MODULE={}.settings'.format(PROJECT_NAME)):
                # run('source venv/bin/activate && pip install -r requirements.txt')
                # run('source venv/bin/activate && python manage.py makemigrations')
                # run('python manage.py migrate')
                run('python manage.py collectstatic --noinput')
                # run("sed -i -e 's/DEBUG=True/DEBUG=False/g' {}/fastermenu/settings.py".format((PROJECT_ROOT)))

    restart()


@task
def bootstrap():
    run('apt update')
    run('apt install git supervisor nginx memcached postgresql python3-dev python-pip python-virtualenv')
    run("export LC_ALL='en_US.UTF-8'")
    run("export LC_CTYPE='en_US.UTF-8'")

    remove()

    run('mkdir -p {}'.format(PROJECT_ROOT))
    run('mkdir -p /root/logs/')
    run('touch /root/logs/gunicorn_supervisor.log')
    run('git clone {} {}'.format(REPO, PROJECT_ROOT))
    run('chmod +x /opt/{}/{}/conf/gunicorn'.format(PROJECT_NAME, PROJECT_NAME))

    with cd(PROJECT_ROOT):
        run('virtualenv -p python3 venv')
        with source_virtualenv():
            with prefix('export DJANGO_SETTINGS_MODULE={}.settings'.format(PROJECT_NAME)):
                run('source venv/bin/activate && pip install -r requirements.txt')
                run('python manage.py makemigrations')
                run('python manage.py migrate')
                run('python manage.py collectstatic --noinput')
                run("sed -i -e 's/DEBUG=True/DEBUG=False/g' {}/{}/settings.py".format((PROJECT_ROOT, PROJECT_NAME)))

    # chown()

    # Deploy web and app server configs
    run('ln -s {}/{}/conf/supervisor.conf /etc/supervisor/conf.d/supervisor.conf'.format(PROJECT_ROOT, PROJECT_NAME))
    run('ln -s {}/{}/conf/nginx.conf /etc/nginx/sites-enabled/{}.conf'.format(PROJECT_ROOT, PROJECT_NAME, PROJECT_NAME))

    restart()

@task
def remove():
    run('supervisorctl stop {}'.format(PROJECT_NAME))
    run('service nginx stop')
    run('rm -f /root/logs/*')
    run('rm -rf {}'.format(PROJECT_ROOT))
    run('rm -f /etc/supervisor/conf.d/supervisor.conf')
    run('rm -f /etc/nginx/sites-enabled/{}.conf'.format(PROJECT_NAME))
