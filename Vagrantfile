# -*- mode: ruby -*-
# vi: set ft=ruby 

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.provider "virtualbox" do |vb| 
    vb.memory = "6000" 
    vb.cpus = "4"
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]    
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt update
    sudo apt install software-properties-common
    sudo apt-add-repository --yes --update ppa:ansible/ansible
    apt install -y ansible
  SHELL

  config.vm.provision "ansible_local" do |ansible|
    ansible.galaxy_role_file = 'requirements.yml'
    ansible.compatibility_mode = "2.0"
    ansible.limit = "local"
    ansible.inventory_path = "inventory.ini"
    ansible.playbook = "playbooks/setup.yml"
    ansible.skip_tags = "optional"
  end

end