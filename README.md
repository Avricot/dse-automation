##Introduction
[Ansible Playbook](http://docs.ansible.com/playbooks.html) for Datastax Enterprise DSE.

Built for Redhat and Debian family

**Generics ansible playbooks. Must be customized for specifics use cases.**

**Full example in `install-dse.yml`.**


### Configuration:
Set your hosts ips in the `hosts` file, example: 

`test    ansible_ssh_user=root ansible_ssh_host=10.200.21.144   cassandra.datacenter=DC1  cassandra.rack=RAC1 cassandra.prefer_local=True`

Some vars must be set for dse install and opscenter:

```
  vars:
    dse_username: 'xxxxxx@mail.com'
    dse_password: 'xxxxxx'
    opscenter:
      #for opscenter agent: ip of the opscenter.
      interface: 'localhost'
```

### Roles available:
#### resmo.ntp
Install ntp server. 

Syntax:

 `- role: resmo.ntp`

#### common
Install common libs and java on the node (curl,vim,sysstat etc.)

Syntaxe:

```$xslt
  - role: common
    #must the the exact name of the extracted archived downloaded with java_download_url
    java_version: jdk1.8.0_111
    #where to download java from.
    java_download_url: 'http://download.oracle.com/otn-pub/java/jdk/8u111-b14/jdk-8u111-linux-x64.tar.gz'
```


#### os-tuning
Tune os with recommanded settings (see https://docs.datastax.com/en/landing_page/doc/landing_page/recommendedSettingsLinux.html)

Syntax:

```$xslt
  - role: os-tuning
    os:
      #Enable extra tuning conf. Should be used carefully.
      advanced_tuning: True
      #will execute a regexp to detect blocks (all blocks will be tuned as SSD !).
      autodetect_block: True
      #If autodetect_block = False, manually list SSD here.
      ssd_blocks: [] #["sda", "sdb"]
      ssd_scheduler: 'deadline'
      #If you have any HDD disks, set autodetect_block to False and list HDD drive here.
      hdd_blocks: [] #["sda", "sdb"]```
      hdd_scheduler: 'cfq'
```      
      
#### dse-install
Add repositories and install dse-full

Syntax:

```$xslt
  - role: dse-install
    spark:
      enabled: False
    install_agent: True
```      

      
#### dse-conf
Configure cassandra yam file

Note: using cassandra.yaml with ninja template might be easier in most case.


```$xslt
  #############################
  # change main cassandra.yaml file:
  - role: dse-conf
    cassandra:
      user: cassandra
      group: cassandra
      #Should be overridden for each node on the host file
      datacenter: DC1
      #Should be overridden for each node on the host file
      rack: RAC1

      #Change cassandra.yaml global configuration
      cassandra_yaml:
        path: '/etc/dse/cassandra/cassandra.yaml'
        #Lines are identified by key.
        #Set value to null to comment a line
        #You can add any line you want here
        conf:
          seeds: "localhost"
          cluster_name: 'TEST'
          listen_address: null
          listen_interface: 'eth0'
          rpc_address: null
          rpc_interface: 'eth0'
          data_file_directories: '\n   - /opt/cassandra/data/data'
          hints_directory: /opt/cassandra/data/hints
          saved_caches_directory: /opt/cassandra/data/saved_caches
          commitlog_directory: /opt/cassandra/commitlog

      cassandra_rackdc_properties:
        path: '/etc/dse/cassandra/cassandra_rackdc.properties'

      #Change jvm.options configuration
      jvm_options:
        path: '/etc/dse/cassandra/jvm.options'
        #None to comment the line
        conf:
          '-Xmx4G': 1
          '-Xms4G': 1
          '-XX:+UseParNewGC': None
```      

### Multi node NUMA
#### dse-add-node
start multiple instances in a single server. Multiple ip address must be set in the `host` file :

`test    ansible_ssh_user=root ansible_ssh_host=192.168.43.173   ip1=192.168.43.173  ip2=10.240.0.21     ip3=10.240.0.21     ip4=10.240.0.21     cassandra.datacenter=DC1  cassandra.rack=RAC1 cassandra.prefer_local=True`

```yaml
# create all instances
- {role: dse-add-node, instance_id: 1, ssd_id: 1, ip: "{{ ip1 }}", start-dse: false}
- {role: dse-add-node, instance_id: 2, ssd_id: 1, ip: "{{ ip2 }}", start-dse: false}
- {role: dse-add-node, instance_id: 3, ssd_id: 2, ip: "{{ ip3 }}", start-dse: false}
- {role: dse-add-node, instance_id: 4, ssd_id: 2, ip: "{{ ip4 }}", start-dse: false}

#############################
#change all instances configuration (if a changed after node creation)
#for multi instance, store cassandra conf in the group_var/all.yml folder and only override specific configuration here.
- {role: dse-conf, cassandra: {cassandra_yaml: {path: '/etc/dse-1/cassandra/cassandra.yaml'}}}
- {role: dse-conf, cassandra: {cassandra_yaml: {path: '/etc/dse-2/cassandra/cassandra.yaml'}}}
- {role: dse-conf, cassandra: {cassandra_yaml: {path: '/etc/dse-3/cassandra/cassandra.yaml'}}}
- {role: dse-conf, cassandra: {cassandra_yaml: {path: '/etc/dse-4/cassandra/cassandra.yaml'}}}
```