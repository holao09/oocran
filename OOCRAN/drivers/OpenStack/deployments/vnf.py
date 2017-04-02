from jinja2 import Template
from drivers.OpenStack.APIs.heat.heat import create_stack_vnf, delete_stack


def add_nfs(vnf):
    elements = ""
    num = 0

    for nf in vnf.nf.all():
        for library in nf.get_libraries_order():
            nf_template = Template(u'''\
nf_{{num}}:
    type: OS::Heat::SoftwareConfig
    properties:
      group: {{group}}
      config: |
        #!/bin/sh
        cd /home/{{user}}
        {{library}}

  ''')

            nf_template = nf_template.render(
                group=library.type,
                num=num,
                user=vnf.operator.name,
                library=library.script,
            )
            elements = elements + nf_template
            num += 1

    return [num, elements]


def nvf(vnf):
    elements = ""
    num = 0

    [nfs_num, nfs] = add_nfs(vnf)

    nvf = Template(u'''\
server{{num}}_init:
    type: OS::Heat::MultipartMime
    properties:
      parts:
      - config: {get_resource: user_config}
      - config: {get_resource: credentials}
{{nfs}}

  server{{num}}:
    type: OS::Nova::Server
    properties:
      name: {{name}}
      image: {{image}}
      flavor: {{flavor}}
      networks:
      - network: network
      user_data_format: RAW
      user_data:
         get_resource: server{{num}}_init

''')

    list_nfs = ""
    for nf in range(0, nfs_num):
        list_nfs += "      - config: {get_resource: nf_" + str(nf) + "}\n"

    nvf = nvf.render(
        name=vnf.name,
        image=vnf.image,
        net="network",
        flavor="small",
        num=num,
        nfs=list_nfs,
    )
    elements += nfs + nvf
    num += 1

    return elements


def create(vnf, vim):
    header = Template(u'''\
heat_template_version: 2014-10-16
description: {{description}}

parameters:
  NetID:
    type: string
    description: Network ID to use for the instance.
    default: net

resources:
  credentials:
    type: OS::Heat::CloudConfig
    properties:
      cloud_config:
        chpasswd:
          list: |
            {{user}}:{{password}}
          expire: False

  user_config:
    type: OS::Heat::CloudConfig
    properties:
      cloud_config:
        users:
        - default
        - name: {{user}}

  ''')
    header = header.render(
        description=vnf.description,
        user=vnf.operator.name,
        password=vnf.operator.password,
    )

    nfv = nvf(vnf)

    template = header + nfv
    print template
    create_stack_vnf(vnf, template, vim)


def delete_deploy(ns):
    delete_stack(ns, ns.scenario.vim)