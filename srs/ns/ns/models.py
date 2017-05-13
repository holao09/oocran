from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from vnfs.models import Vnf, Operator
from vims.models import Vim
from django.utils import timezone
from influxdb import InfluxDBClient
from OOCRAN.settings import INFLUXDB
from drivers.OpenStack.APIs.nova.nova import console
import paramiko


class Ns(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='opnfv/')
    status = models.CharField(max_length=120, default="Shut Down")
    price = models.FloatField(default=0)
    total = models.FloatField(default=0)
    vim_option = models.CharField(max_length=120, default="Near")
    vim = models.ForeignKey(Vim, on_delete=models.CASCADE, null=True, blank=True)
    launch_time = models.DateTimeField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_scenario(self):
        return self.area.name

    def create_influxdb_database(self):
        db = "ns_" + str(self.id)
        client = InfluxDBClient(**INFLUXDB['default'])
        print("Create database: " + db)
        client.create_database(db)
        print("Add grants")
        client.grant_privilege("all", db, self.operator.name)

    def delete_influxdb_database(self):
        db = "ns_" + str(self.id)
        client = InfluxDBClient(**INFLUXDB['default'])
        print("Delete database: " + db)
        client.drop_database(db)

    def cost(self):
        if self.status == "Running":
            n_time = timezone.now()
            l_time = self.launch_time
            s_now = n_time.year * 31536000 + n_time.month * 86400 * 30 + n_time.day * 86400 + n_time.hour * 3600 + n_time.minute * 60 + n_time.second
            s_launch = l_time.year * 31536000 + l_time.month * 86400 * 30 + l_time.day * 86400 + l_time.hour * 3600 + l_time.minute * 60 + l_time.second
            self.total += round((self.price / 3600) * (s_now - s_launch), 3)
            self.save()
            return self.total
        else:
            return self.total

    def get_absolut_url(self):
        return reverse("ns:detail", kwargs={"id": self.id})

    def active_shutdown(self):
        return True

    class Meta:
        ordering = ["-timestamp", "-update"]


class Nvf(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    ns = models.ForeignKey(Ns, on_delete=models.CASCADE)
    cpu = models.IntegerField(null=True, blank=True, default=1)
    ram = models.IntegerField(null=True, blank=True, default=1024)
    disk = models.IntegerField(null=True, blank=True, default=1)
    vnf = models.ForeignKey(Vnf, null=True, blank=True)
    flavor = models.CharField(max_length=120, default="small")
    mgmt_ip = models.CharField(max_length=120, blank=True, null=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.name

    def connect(self, command):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        client.connect(self.mgmt_ip, username=self.operator.name, password=self.operator.password)
        stdin, stdout, stderr = client.exec_command(command)
        for line in stdout:
            print line.strip('\n')
        client.close()

    def get_console(self):
        return console(self)['console']['url']