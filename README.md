##Introduction
This is an [Ansible Playbook](http://docs.ansible.com/playbooks.html) you can point and shoot at any infrastructure you want to build a DataStax Enterprise cluster with Cassandra, Solr and Spark. The playbook will install, configure single and multiple clusters. Add more nodes and datacenters by simply including more hosts. There is an optional [OpsCenter](http://www.datastax.com/products/datastax-enterprise-visual-admin) Playbook included. The latest version of [DataStax Enterprise](http://www.datastax.com/what-we-offer/products-services/datastax-enterprise) will be installed.
The conf templates are for DSE version 5.0. Edit conf files if you update DSE version.

To build a DSE Cassandra cluster:

Add nodes to ```hosts```.

Edit ```dse-XXX.yml``` with your settings.

Run ```ansible-playbook -i hosts dse-XXX.yml```
