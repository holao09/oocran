"""
    Open Orchestrator Cloud Radio Access Network

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

from __future__ import absolute_import, unicode_literals
from .models import Pool, Channel
from ues.models import Ue
from bbus.models import Bbu
from celery import task
from django.utils import timezone
from drivers.Vagrant.APIs.main import vagrant_launch as Vagrant_create_deploy
from drivers.Vagrant.APIs.main import vagrant_destroy as Vagrant_delete_deploy


@task()
def celery_launch(id):
    pool = Pool.objects.get(id=id)

    pool.status = 'Working-launch'
    pool.save()

    bbus = Bbu.objects.filter(ns=pool)
    [bbu.assign_frequency() for bbu in bbus]
    channels = Channel.objects.filter(ns=pool)
    ues = Ue.objects.filter(ns=pool)

    Vagrant_create_deploy(ns=pool, bbus=bbus, channels=channels, ues=ues)

    print "Provision finished"

    pool.status = 'Running'
    pool.launch_time = timezone.now()
    pool.scenario.active_infras += 1
    pool.scenario.save()
    pool.save()
    print "NS running"


@task()
def celery_shut_down(id, action=None):
    pool = Pool.objects.get(id=id)
    pool.status = 'Working-shutdown'
    pool.save()

    pool.scenario.price += round(pool.cost(), 3)
    pool.scenario.save()
    pool.remove_frecuencies()

    Vagrant_delete_deploy(pool)

    pool.status = 'Shut Down'
    pool.save()
    print "NS shut down"
    if action != None:
        pool.scenario.active_infras -= 1
        pool.scenario.save()
        pool.delete()


########################################################


from schedulers.models import Scheduler
import datetime
from drivers.Vagrant.APIs.main import vagrant_ssh, vagrant_destroy_nvf, vagrant_launch_nvf


@task()
def ns():
    schedulers = Scheduler.objects.filter(type="ns")
    for scheduler in schedulers:
        if str(scheduler.time) == datetime.datetime.now().strftime('%H:%M:00'):
            if scheduler.action == "Launch":
                scheduler.scenario.active_infras += 1
                scheduler.scenario.save()
                celery_launch.delay(id=scheduler.ns.id)
                scheduler.ns.save()
                print scheduler.name + " launched!"
            elif scheduler.action == "Shut Down":
                scheduler.scenario.active_infras -= 1
                scheduler.scenario.save()
                celery_shut_down.delay(id=scheduler.ns.id)
                scheduler.ns.save()
                print scheduler.name + " shut down!"
            if scheduler.destroy is True:
                scheduler.delete()


@task()
def nvf():
    schedulers = Scheduler.objects.filter(type="nvf")
    for scheduler in schedulers:
        if str(scheduler.time) == datetime.datetime.now().strftime('%H:%M:00'):
            if scheduler.action == "Launch":
                for nvf in scheduler.nvfs.all():
                    vagrant_launch_nvf(nvf=nvf)
            elif scheduler.action == "Shut Down":
                for nvf in scheduler.nvfs.all():
                    vagrant_destroy_nvf(nvf=nvf)
            elif scheduler.action == "Reconfigure":
                for nvf in scheduler.nvfs.all():
                    vagrant_ssh(script=scheduler.script, nvf=nvf)
            if scheduler.destroy is True:
                scheduler.delete()
